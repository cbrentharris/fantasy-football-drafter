import requests
import re
from bs4 import BeautifulSoup


class DataCrawler:
    ROOT_URL = "https://www.pro-football-reference.com/"
    ROOT = "https://www.pro-football-reference.com/years/2022/games.htm"
    BOX_SCORE_PATTERN = r'/boxscores/[0-9a-zA-Z]+\.htm'

    def crawl(self):
        root_response = requests.get(self.ROOT)
        if root_response.status_code == 200:
            box_score_links = self.find_all_box_score_links(root_response.text)
            # for box_score_link in box_score_links:
            #     self.load_player_stats_from_box_score_link(box_score_link)
            self.load_player_stats_from_box_score_link(next(box_score_links))
            #print(next(box_score_links))

    def find_all_box_score_links(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        boxscore_tds = soup.select('td[data-stat="boxscore_word"]')
        for td in boxscore_tds:
            links = td.find_all('a', href=True)
            for link in links:
                yield link['href']

    def load_player_stats_from_box_score_link(self, box_score_link):
        response = requests.get(self.ROOT_URL + box_score_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_offense = soup.find(id="player_offense")
        player_stats = player_offense.find_all('tr')
        for stat in player_stats:
            names = stat.select('th[data-stat="player"][data-append-csv]')
            if not names:
                continue
            name = names[0]
            team = stat.select('td[data-stat="team"]')[0]
            pass_yards = stat.select('td[data-stat="pass_yds"]')[0]
            pass_td = stat.select('td[data-stat="pass_td"]')[0]
            pass_int = stat.select('td[data-stat="pass_int"]')[0]
            print(name.text, team.text, pass_yards.text, pass_td.text, pass_int.text)

