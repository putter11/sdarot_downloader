from selenium import webdriver
import requests
import time
import re
from tqdm import tqdm
import os
import pandas as pd
import glob
import argparse


class SdarotDownloader(object):
    """
    Downloads a siries episodes from sdarot.tv.
    """

    COOKIE_NAME = "Sdarot"
    URL_REG = 'videojs_html5_api.*src="//(.*)uid='
    BLOCK_SIZE = 1024
    URL = 'https://sdarot.world/watch/{}/season/{}/episode/{}.mp4'
    FILE_NAME = "{} season {} episode {}"
    SERIES_NAME_INDEX = 0
    SERIES_NUMBER_INDEX = 1
    SEASONS_INDEX = 2
    EPISODES_INDEX = 3

    def __init__(self, driver, series_list, path):
        self.driver = driver
        self.path = path
        self.series_name = str(series_list[self.SERIES_NAME_INDEX])
        self.series_number = str(series_list[self.SERIES_NUMBER_INDEX])
        self.seasons = self._parse_episode_season(str(series_list[self.SEASONS_INDEX]))
        self.episodes = self._parse_episode_season(str(series_list[self.EPISODES_INDEX]))
        self._handle_dir()
        self._download()
    
    def _handle_dir(self):
        """
        Checks if dedicated dir for the series exists and if not creates one.
        """
        self.dir = os.path.join(self.path, self.series_name)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def _download(self):
        """
        Starts the procecing and downloading of every episode.
        """
        for season in self.seasons:
            for episode in self.episodes:
                self.url = self.URL.format(self.series_number, season, episode)
                print self.url
                self.file_path = os.path.join(self.dir, self.FILE_NAME.format(self.series_name, season, episode))
                if self._handle_page():
                    self._find_url()
                else:
                    print "episode doesn't exist"

    def _handle_page(self):
        """
        Opens the episode page in sdarot.
        """
        self.driver.get(self.url)
        if self.driver.current_url != self.url:
            return 0
        time.sleep(40)
        self.cookie = {self.COOKIE_NAME:self.driver.get_cookie(self.COOKIE_NAME)['value']}
        self.page_content = self.driver.page_source
        return 1
   
    def _find_url(self):
        """
        Finds the url of the video in the sdarot server.
        """
        video_url = re.findall(self.URL_REG, self.page_content)
        if video_url:
            self.video_url =  "https://" + video_url[0].replace("amp;", "")
            print "found_url"
            self._download_video()
        else:
            print "video not found"
       
    def _download_video(self):
        """
        Donloads the video.
        """
        print "started downloading"
        video = requests.get(self.video_url, cookies=self.cookie, stream=True)
        total = int(video.headers.get('content-length', 0))
        t = tqdm(total=total, unit="iB", unit_scale=True)
        with open(self.file_path, "wb") as w:
            for data in video.iter_content(self.BLOCK_SIZE):
                w.write(data)
                t.update(len(data))
    
    def _parse_episode_season(self, to_parse):
        """
        Parses to a list the seasons and episoded given in the excel.
        """
        return range(int(to_parse.split('-')[0]), int(to_parse.split('-')[1]) + 1) if to_parse.count('-') else [to_parse]



def open_excel(path):
    """
    Opens the excel file.
    """
    excel = pd.read_excel(path, )
    return [list(i) for i in excel.values] 


def parser_handler():
    """
    Handels the arguments given in the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", dest="excel_path", help="The path of the excel file the script reads from. If not given the program will search for excels in the current folder")
    parser.add_argument("-v", dest="video_path", default='.', help="The path where the files will be saved. If not given the program will save the files in the current folder")
    return parser.parse_args()


def check_arguments(args):
    """
    Checks that the arguments given are all valid.
    """
    if args.excel_path:
        excel_path = args.excel_path
        if not os.path.isfile(excel_path):
            print "I couldn't find the Excel file you entered"
            return 0
    else:
        excel_path = glob.glob("*.xls*")
        if not excel_path:
            print "No excel file found in folder" 
            return 0
        excel_path = excel_path[0]
    if not os.path.isdir(args.video_path):
        print "I couldn't find the folder path you entered"
        return 0
    return excel_path, args.video_path


def main():
    args = check_arguments(parser_handler())
    if not args:
        return 0
    excel_path, video_path = args
    dri = webdriver.Firefox()
    series_list = open_excel(excel_path)
    print "opened driver"
    for i in series_list:
        SdarotDownloader(driver=dri, series_list = i, path=video_path)
    dri.close()

if __name__ == "__main__":
    main()

