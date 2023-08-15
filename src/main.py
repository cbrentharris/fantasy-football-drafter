from models.models import PlayerStats, Player, Roster
import os
import json


def start_draft(transformed_players):
    roster = Roster()
    while True:
        print("")
        transformed_players = [player for player in transformed_players if roster.has_spot(player)]
        transformed_players = sorted([player for player in transformed_players],
                                     key=lambda player: (player.net_additional_score(roster), player.overall_score()),
                                     reverse=True)
        print("Top 10:")
        for player in transformed_players[:10]:
            print(player.name, player.position, format(player.net_additional_score(roster), ".2f"),
                  format(player.overall_score(), ".2f"))
        user_input = input("Enter action(draft or lost) and player name:")
        action, first_name, last_name = user_input.split(" ")
        player_name = first_name + " " + last_name
        if action == "draft":
            player_to_draft = [player for player in transformed_players if player.name == player_name]
            if len(player_to_draft) == 0:
                print("Could not find " + player_name + " please try again")
                continue
            roster.draft(player_to_draft[0])
            transformed_players = [player for player in transformed_players if player.name != player_name]
        elif action == "lost":
            transformed_players = [player for player in transformed_players if player.name != player_name]
        else:
            print("Could not understand action " + action + " please try again")


def main():
    current_dir = os.path.dirname(__file__)
    resources_dir = os.path.join(current_dir, 'resources')
    player_stats_file_name = os.path.join(resources_dir, 'projected_player_stats.json')
    players = {}
    with open(player_stats_file_name, 'r') as player_stats_file:
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

    transformed_players = sorted([player for key, player in players.items()], key=lambda player: player.overall_score())
    start_draft(transformed_players)
    for player in transformed_players:
        print(player.name, player.overall_score(), len(player.stats))


if __name__ == "__main__":
    main()
