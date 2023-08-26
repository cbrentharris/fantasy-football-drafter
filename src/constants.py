import os


class Constants:
    _current_dir = os.path.dirname(__file__)
    RESOURCES_DIR = os.path.join(_current_dir, 'resources')
    PLAYER_PICKLE_FILENAME = os.path.join(RESOURCES_DIR, 'players.pickle')
    ROSTER_PICKLE_FILENAME = os.path.join(RESOURCES_DIR, 'roster.pickle')
    ROSTERS_PICKLE_FILENAME = os.path.join(RESOURCES_DIR, 'rosters.pickle')
    PROJECTED_PLAYER_STATS_FILENAME = os.path.join(RESOURCES_DIR, 'projected_player_stats.json')
    KEEPERS_FILENAME = os.path.join(RESOURCES_DIR, 'keepers.json')
