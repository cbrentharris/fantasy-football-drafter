import requests
from bs4 import BeautifulSoup
import os
import json
import time


class DataCrawler:
    ROOT_URL = ""
    ROOT = ""
    PROJECTION_URL = ""

    def crawl_project_stats(self) -> None:
        week_data = {}
        for week in range(1, 19):
            projection_response = requests.get(self.PROJECTION_URL.format(stat_week=week))
            player_stats = self.load_player_stats_from_projection(projection_response.text)
            week_data[week] = list(player_stats)
            print("Loaded data for week: " + str(week))
            time.sleep(10)
        self.save_player_stats(week_data)

    def crawl_historical_stats(self):
        root_response = requests.get(self.ROOT)
        if root_response.status_code == 200:
            box_score_links = self.find_all_box_score_links(root_response.text)
            self.load_player_stats_from_box_score_link(next(box_score_links))

    @staticmethod
    def find_all_box_score_links(text):
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
            name = names[0].text
            team = stat.select('td[data-stat="team"]')[0].text
            pass_yards = int(stat.select('td[data-stat="pass_yds"]')[0].text)
            pass_td = int(stat.select('td[data-stat="pass_td"]')[0].text)
            pass_int = int(stat.select('td[data-stat="pass_int"]')[0].text)
            rush_yards = int(stat.select('td[data-stat="rush_yds"]')[0].text)
            rush_td = int(stat.select('td[data-stat="rush_td"]')[0].text)
            receiving_yards = int(stat.select('td[data-stat="rec_yds"]')[0].text)
            receiving_td = int(stat.select('td[data-stat="rec_td"]')[0].text)
            fumbles_lost = int(stat.select('td[data-stat="fumbles_lost"]')[0].text)
            print(name, team, pass_yards, pass_td, pass_int, rush_yards, rush_td, fumbles_lost, receiving_yards,
                  receiving_td)

    @staticmethod
    def load_player_stats_from_projection(text):
        soup = BeautifulSoup(text, 'html.parser')
        tbody = soup.find('tbody')
        if not tbody:
            raise Exception("Couldn't find table body to parse players")
        players = tbody.find_all('tr')
        for player in players:
            player_name = player.find('a', {'class': 'playerName'}).text
            player_position = player.find('em').text.split(" - ")[0]
            passing_yards = player.find('td', {'class': 'stat_5'}).text
            passing_tds = player.find('td', {'class': 'stat_6'}).text
            interceptions = player.find('td', {'class': 'stat_7'}).text
            rushing_yards = player.find('td', {'class': 'stat_14'}).text
            rushing_tds = player.find('td', {'class': 'stat_15'}).text
            receiving_yards = player.find('td', {'class': 'stat_21'}).text
            receiving_tds = player.find('td', {'class': 'stat_22'}).text
            fumbles = player.find('td', {'class': 'stat_30'}).text
            yield {"player_name": player_name, "passing_yards": passing_yards, "passing_tds": passing_tds,
                   "interceptions": interceptions, "rushing_yards": rushing_yards, "rushing_tds": rushing_tds,
                   "receiving_yards": receiving_yards, "receiving_tds": receiving_tds, "fumbles": fumbles,
                   "player_position": player_position}

    @staticmethod
    def save_player_stats(player_stats: list[dict]):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        resources_dir = os.path.join(parent_dir, 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        player_stats_file_name = os.path.join(resources_dir, 'projected_player_stats.json')
        with open(player_stats_file_name, 'w') as player_stats_file:
            json.dump(player_stats, player_stats_file)
