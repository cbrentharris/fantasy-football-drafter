from models import Draft


def start_draft():
    draft = Draft(12, my_position=4)
    while True:
        draft.print_summary()
        player_name = input("Enter player name:")
        draft.select(player_name)
        draft.save()


def main():
    start_draft()


if __name__ == "__main__":
    main()
