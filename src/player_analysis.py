from models import Player
from prettytable import PrettyTable


def main():
    players = list(sorted(Player.load().values(), key=lambda p: p.overall_score(), reverse=True))
    player_table = PrettyTable()
    player_table.field_names = ["Name", "Overall Score", "Rank"]
    for idx, player in enumerate(players):
        player_table.add_row([player.name, player.overall_score(), idx])
    print(player_table)


if __name__ == "__main__":
    main()
