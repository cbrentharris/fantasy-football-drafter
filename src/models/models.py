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
    def __init__(self, stats: dict[int, PlayerStats], name: str, position: str):
        self.stats = stats
        self.name = name
        self.position = position

    def overall_score(self) -> float:
        return sum(map(lambda stat: stat.score(), self.stats.values()))

    def net_additional_score(self, roster) -> float:
        if not roster.has_spot(self):
            return 0.0

        if roster.has_starting_spot(self):
            return self.overall_score()

        matching_players = roster.matching_players(self)
        current_weekly_maxes = map(lambda player: {w: s.score() for w, s in player.stats.items()},
                                   matching_players)

        def merge_dicts(dicts):
            merged_dict = {}
            for d in dicts:
                for key, value in d.items():
                    merged_dict[key] = merged_dict.get(key, []) + [value]
            return merged_dict

        current_weekly_merged = merge_dicts(list(current_weekly_maxes))

        total_delta = 0.0
        for week, stat in self.stats.items():
            weekly_maxes = sorted(current_weekly_merged[week], reverse=True)[:roster.starting_positions(self)]
            weekly_max = sum(weekly_maxes)
            weekly_score = stat.score()
            with_weekly = sum(sorted(weekly_maxes + [weekly_score], reverse=True)[:roster.starting_positions(self)])
            delta = with_weekly - weekly_max
            if delta > 0.0:
                total_delta += delta
        return total_delta


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

    def draft(self, player: Player) -> None:
        self.positions[player.position].players.append(player)

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
