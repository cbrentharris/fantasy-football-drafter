import json
import pickle

from prettytable import PrettyTable

from constants import Constants


class PlayerStats:
    """
    This class represents the statistics a player had (or is predicted to have) in a given game. This is to
    allow for dynamic allocation of additional roster adds wherein a player might not have the best predicted
    score, but is a good roster fit due to byes etc.
    """

    def __init__(self, passing_yards: str, passing_td: str, interceptions: str, rushing_yards: str, rushing_td: str,
                 fumbles: str, receiving_yards: str, receiving_td: str):
        self.passing_yards = self.parse(passing_yards)
        self.passing_td = self.parse(passing_td)
        self.interceptions = self.parse(interceptions)
        self.rushing_yards = self.parse(rushing_yards)
        self.rushing_td = self.parse(rushing_td)
        self.receiving_yards = self.parse(receiving_yards)
        self.receiving_td = self.parse(receiving_td)
        self.fumbles = self.parse(fumbles)

    def score(self) -> float:
        return self.passing_td * 3 + (
                self.passing_yards / 50) - self.interceptions + self.rushing_td * 3 + (
                       self.rushing_yards / 30) - self.fumbles + self.receiving_td * 3 + (self.receiving_yards / 30)

    @staticmethod
    def parse(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            return 0.0


class Player:
    """
    This class represents an offensive player and their projected stats per week. Used to optimize
    drafted players that complement an existing draft very well.
    """

    def __init__(self, stats: dict[int, PlayerStats], name: str, position: str):
        self.stats = stats
        self.name = name
        self.position = position

    def overall_score(self) -> float:
        return sum(map(lambda stat: stat.score(), self.stats.values()))

    @staticmethod
    def load():
        players = {}
        with open(Constants.PROJECTED_PLAYER_STATS_FILENAME, 'r') as player_stats_file:
            player_stats = json.load(player_stats_file)
            for week, stats in player_stats.items():
                for stat in stats:
                    if stat['player_name'] not in players:
                        players[stat['player_name']] = Player({}, stat['player_name'], stat['player_position'])
                    players[stat['player_name']].stats[week] = PlayerStats(passing_yards=stat['passing_yards'],
                                                                           passing_td=stat['passing_tds'],
                                                                           interceptions=stat['interceptions'],
                                                                           rushing_yards=stat['rushing_yards'],
                                                                           rushing_td=stat['rushing_tds'],
                                                                           receiving_yards=stat['receiving_yards'],
                                                                           receiving_td=stat['receiving_tds'],
                                                                           fumbles=stat['fumbles'])
        return players


class Position:
    RECEIVERS = ["WR", "TE"]

    def __init__(self, position: str, players: list[Player], max_players: int, starting_players: int):
        self.posision = position
        self.players = players
        self.max_players = max_players
        self.starting_players = starting_players

    def has_spot(self) -> bool:
        return len(self.players) < self.max_players

    def has_starting_spot(self) -> bool:
        return len(self.players) < self.starting_players

    def matching_players(self, player: Player) -> list[Player]:
        if player.position in self.RECEIVERS and self.posision in self.RECEIVERS:
            return self.players
        if player.position == self.posision:
            return self.players
        return []


class Roster:
    def __init__(self):
        self.positions = {}
        receivers = []
        self.positions["QB"] = Position("QB", [], 3, 1)
        self.positions["RB"] = Position("RB", [], 10, 2)
        self.positions["WR"] = Position("WR", receivers, 11, 3)
        self.positions["TE"] = Position("TE", receivers, 11, 3)

        self.all_players = []

    def add(self, player: Player) -> None:
        self.positions[player.position].players.append(player)
        self.all_players.append(player)

    def has_spot(self, player: Player) -> bool:
        position = self.positions[player.position]
        return position.has_spot()

    def has_starting_spot(self, player: Player) -> bool:
        position = self.positions[player.position]
        return position.has_starting_spot()

    def matching_players(self, player: Player) -> list[Player]:
        return [p for position in self.positions.values() for p in position.matching_players(player)]

    def starting_positions(self, player: Player) -> int:
        return self.positions[player.position].starting_players

    def net_additional_score(self, player: Player) -> float:
        if not self.has_spot(player):
            return 0.0

        if self.has_starting_spot(player):
            return player.overall_score()

        matching_players = self.matching_players(player)
        current_weekly_maxes = map(lambda p: {w: s.score() for w, s in p.stats.items()},
                                   matching_players)

        def merge_dicts(dicts):
            merged_dict = {}
            for d in dicts:
                for key, value in d.items():
                    merged_dict[key] = merged_dict.get(key, []) + [value]
            return merged_dict

        current_weekly_merged = merge_dicts(list(current_weekly_maxes))

        total_delta = 0.0
        for week, stat in player.stats.items():
            weekly_maxes = sorted(current_weekly_merged[week], reverse=True)[:self.starting_positions(player)]
            weekly_max = sum(weekly_maxes)
            weekly_score = stat.score()
            with_weekly = sum(sorted(weekly_maxes + [weekly_score], reverse=True)[:self.starting_positions(player)])
            delta = with_weekly - weekly_max
            if delta > 0.0:
                total_delta += delta
        return total_delta

    def save(self):
        with open(Constants.ROSTER_PICKLE_FILENAME, 'wb') as roster_pickle_file:
            pickle.dump(self, roster_pickle_file)

    @staticmethod
    def load():
        try:
            with open(Constants.ROSTER_PICKLE_FILENAME, 'rb') as roster_pickle_file:
                return pickle.load(roster_pickle_file)

        except Exception as e:
            print(e)
            return Roster()


class Draft:

    def __init__(self):
        self.roster = Roster.load()
        self.available_players = sorted(self.load_players(), key=lambda player: (
            self.roster.net_additional_score(player), player.overall_score()), reverse=True)

    @staticmethod
    def load_players() -> list[Player]:
        try:
            with open(Constants.PLAYER_PICKLE_FILENAME, 'rb') as player_pickle_file:
                return pickle.load(player_pickle_file)

        except Exception as e:
            print(e)
            return Player.load().values()

    def save(self) -> None:
        with open(Constants.ROSTER_PICKLE_FILENAME, 'wb') as roster_pickle_file:
            pickle.dump(self.roster, roster_pickle_file)
        with open(Constants.PLAYER_PICKLE_FILENAME, 'wb') as player_pickle_file:
            pickle.dump([p for p in self.available_players], player_pickle_file)

    def find(self, player_name: str):
        player_found = None
        for player in self.available_players:
            if player_name == player.name:
                player_found = player
        return player_found

    def select(self, player_name: str) -> None:
        player_to_add = self.find(player_name)
        if player_to_add is None:
            print("Could not find player " + player_name + " please try again.")
            return

        self.roster.add(player_to_add)
        self.remove_player_from_available_list(player_to_add)

    def lose(self, player_name):
        player_lost = self.find(player_name)
        if player_lost is None:
            print("Could not find player " + player_name + " please try again.")
            return
        self.remove_player_from_available_list(player_lost)

    def remove_player_from_available_list(self, player):
        without_player = [p for p in self.available_players if p.name != player.name]
        self.available_players = sorted(without_player,
                                        key=lambda p: (self.roster.net_additional_score(p), p.overall_score()),
                                        reverse=True)

    def print_summary(self):
        available_table = PrettyTable()
        available_table.field_names = ["Name", "Position", "Net Additional Score", "Overall Score"]
        available_table.float_format = ".2"

        roster_table = PrettyTable()
        roster_table.field_names = ["Name", "Position Drafted"]

        for index, player in enumerate(self.roster.all_players):
            roster_table.add_row([player.name, index + 1])

        top_count = 7
        top = self.available_players[:top_count]
        top_qb = list(filter(lambda p: p.position == "QB", self.available_players))[:top_count]
        top_rb = list(filter(lambda p: p.position == "RB", self.available_players))[:top_count]
        top_receiver = list(filter(lambda p: p.position == "WR" or p.position == "TE", self.available_players))[:top_count]
        self.add_players(available_table, top_qb)
        self.add_players(available_table, top_rb)
        self.add_players(available_table, top_receiver)
        self.add_players(available_table, top)
        print("Roster:")
        print(roster_table)
        print("")
        print("Available Players:")
        print(available_table)

    def add_players(self, table: PrettyTable, players: list[Player]):
        for player in players:
            last_player = player.name == players[-1].name
            table.add_row(
                [player.name, player.position, self.roster.net_additional_score(player), player.overall_score()],
                divider=last_player)
