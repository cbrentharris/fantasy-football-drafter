import os
from constants import Constants


def clean():
    for f in [
        Constants.ROSTERS_PICKLE_FILENAME,
        Constants.PLAYER_PICKLE_FILENAME
    ]:
        try:
            os.remove(f)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    clean()
