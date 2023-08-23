from constants import Constants
from models import Player
import json
from prettytable import PrettyTable


def main():
    players = list(sorted(Player.load().values(), key=lambda p: p.overall_score(), reverse=True))
    keeper_table = PrettyTable()
    keeper_table.field_names = ["Name", "Overall Score", "Round", "Rank"]
    with open(Constants.KEEPERS_FILENAME, 'r') as keepers_file:
        keepers = json.load(keepers_file)
        for keeper in keepers:
            player = [p for p in players if p.name == keeper["name"]][0]
            positions = [p for p in players if p.position == player.position]
            rank = [(idx, p) for idx, p in enumerate(positions) if p.name == player.name][0][0] + 1
            keeper_table.add_row([player.name, format(player.overall_score(), ".2f"), keeper["round"], rank])
    print(keeper_table)


if __name__ == "__main__":
    main()
