from enum import Enum, auto


class Team(Enum):
    CARDINALS = auto()
    FALCONS = auto()
    RAVENS = auto()
    BILLS = auto()
    PANTHERS = auto()
    BEARS = auto()
    BENGALS = auto()
    BROWNS = auto()
    COWBOYS = auto()
    BRONCOS = auto()
    LIONS = auto()
    PACKERS = auto()
    TEXANS = auto()
    COLTS = auto()
    JAGUARS = auto()
    CHIEFS = auto()
    RAIDERS = auto()
    CHARGERS = auto()
    RAMS = auto()
    DOLPHINS = auto()
    VIKINGS = auto()
    PATRIOTS = auto()
    SAINTS = auto()
    GIANTS = auto()
    JETS = auto()
    EAGLES = auto()
    STEELERS = auto()
    NINERS = auto()
    SEAHAWKS = auto()
    BUCCANEERS = auto()
    TITANTS = auto()
    COMMANDERS = auto()


class RunningBack:
    class RunningBackPerformance:
        def __init__(self, yards: int, touchdowns: int, fumbles: int, team: Team):
            self.yards = yards
            self.touchdowns = touchdowns
            self.fumbles = fumbles
            self.team = team

        def score(self):
            return (self.yards / 30) + self.touchdowns * 3 - self.fumbles

    def __init__(self, performances: list[RunningBackPerformance], bye: int):
        self.performances = performances
        self.bye = bye

    def projected_score(self):
        return sum(map(lambda p: p.score(), self.performances))


class QuarterBack:
    class QuarterbackPerformance:
        def __init__(self, interceptions: int, passing_yards: int, passing_touchdowns: int, rushing_touchdowns: int,
                     rushing_yards: int, fumbles: int, ):
            self.interceptions = interceptions
            self.passing_yards = passing_yards
            self.passing_touchdowns = passing_touchdowns
            self.rushing_touchdowns = rushing_touchdowns
            self.rushing_yards = rushing_yards
            self.fumbles = fumbles

        def score(self):
            return self.passing_touchdowns * 3 + (
                    self.passing_yards / 50) - self.interceptions + self.rushing_touchdowns * 3 + (
                           self.rushing_yards / 30) - self.fumbles

    def __init__(self, performances: list[QuarterbackPerformance], bye: int):
        self.performances = performances
        self.bye = bye

    def projected_score(self):
        return sum(map(lambda p: p.score(), self.performances))

    def score_against(self, team):
        pass


class Receiver:
    def __init__(self, receiving_yards: int, receiving_touchdowns: int, fumbles: int, bye: int):
        self.receiving_yards = receiving_yards
        self.receiving_touchdowns = receiving_touchdowns
        self.fumbles = fumbles
        self.bye = bye

    def projected_score(self):
        return (self.receiving_yards / 30) + self.receiving_touchdowns * 3 - self.fumbles

    def is_good_complement(self, other):
        pass
