import os
from constants import Constants


def clean():
    os.remove(Constants.PLAYER_PICKLE_FILENAME)
    os.remove(Constants.ROSTER_PICKLE_FILENAME)


if __name__ == "__main__":
    clean()
