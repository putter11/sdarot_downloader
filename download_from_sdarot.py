from selenium import webdriver
import requests
import time
import re
from tqdm import tqdm
import os
import pandas as pd


EXCEL_PATH = "/home/putter/Videos/series.xlsx"


class SdarotDownloader(object):

    COOKIE_NAME = "Sdarot"
    URL_REG = 'videojs_html5_api.*src="//(.*)uid='
    BLOCK_SIZE = 1024
    URL = 'https://sdarot.world/watch/{}/season/{}/episode/{}'
    PATH = "/home/putter/Videos"
    FILE_NAME = "{} season {} episode {}"
    SERIES_NAME_INDEX = 0
    SERIES_NUMBER_INDEX = 1
    SEASONS_INDEX = 2
    EPISODES_INDEX = 3

    def __init__(self, driver, series_name, series_number, episodes="1", seasons="1"):
        self.driver = driver
        self.series_name = series_name
        self.series_number = series_number
        self.episodes = self._parse_episode_season(episodes)
        self.seasons = self._parse_episode_season(seasons)
        self._handle_dir()
        self._download()
    
    def _handle_dir(self):
        self.dir = os.path.join(self.PATH, self.series_name)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def _download(self):
        for season in self.seasons:
            for episode in self.episodes:
                self.url = self.URL.format(self.series_number, season, episode)
                self.file_path = os.path.join(self.dir, self.FILE_NAME.format(self.series_name, season, episode))
                if self._handle_page():
                    self._find_url()
                else:
                    print "episode doesn't exist"

    def _handle_page(self):
        self.driver.get(self.url)
        if self.driver.current_url != self.url:
            return 0
        time.sleep(40)
        self.cookie = {self.COOKIE_NAME:self.driver.get_cookie(self.COOKIE_NAME)['value']}
        self.page_content = self.driver.page_source
        return 1
   
    def _find_url(self):
        video_url = re.findall(self.URL_REG, self.page_content)
        if video_url:
            self.video_url =  "https://" + video_url[0].replace("amp;", "")
            print "found_url"
            self._download_video()

        else:
            print "video not found"
       
    def _download_video(self):
        print "started downloading"
        video = requests.get(self.video_url, cookies=self.cookie, stream=True)
        total = int(video.headers.get('content-length', 0))
        t = tqdm(total=total, unit="iB", unit_scale=True)
        with open(self.file_path, "wb") as w:
            for data in video.iter_content(self.BLOCK_SIZE):
                w.write(data)
                t.update(len(data))
    
    def _parse_episode_season(self, to_parse):
        return range(int(to_parse.split('-')[0]), int(to_parse.split('-')[1]) + 1) if to_parse.count('-') else to_parse



def open_excel(path):
    excel = pd.read_excel(path)
    return [list(i) for i in excel] 


def main():
    dri = webdriver.Firefox()
    print "opened driver"
    series_number = "4497"
    series_list = open_excel(EXCEL_PATH)
    #for i in series_list:
        #SdarotDownloader(driver=dri) 
    SdarotDownloader(driver=dri, series_number=series_number, series_name="backugan", episodes="10-15")
    dri.close()

if __name__ == "__main__":
    main()

