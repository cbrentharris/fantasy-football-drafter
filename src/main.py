from models import Draft


def start_draft():
    draft = Draft()
    while True:
        draft.print_summary()
        user_input = input("Enter action(draft or lost) and player name:")
        action, first_name, last_name = user_input.split(" ")
        player_name = first_name + " " + last_name
        if action == "draft":
            draft.select(player_name)
        elif action == "lost":
            draft.lose(player_name)
        else:
            print("Could not understand action " + action + " please try again")
        draft.save()


def main():
    start_draft()


if __name__ == "__main__":
    main()
