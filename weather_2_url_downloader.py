import requests
from bs4 import BeautifulSoup
import urllib
import csv
import sys
import datetime
import time
import pandas as pd
import re

from concurrent.futures import ThreadPoolExecutor, as_completed

class urlDownloader():
    def __init__(self):
        self.result = []

    def date_creator(self, start_date, end_date):
        begin = datetime.date(int(start_date.split('-')[0]),
                              int(start_date.split('-')[1]),
                              int(start_date.split('-')[2]))
        end = datetime.date(int(end_date.split('-')[0]),
                            int(end_date.split('-')[1]),
                            int(end_date.split('-')[2]))

        numdays = end - begin

        if end < begin:
            print("\nDatetime error...\n")

        date_list = [begin + datetime.timedelta(days=x) for x in range(0, numdays.days)]
        date_inputs = [date.strftime('%Y-%m-%d') for date in date_list]
        return date_inputs


    def url_downloader(self, date, station_code, station_name):
        st_name_encoded = urllib.parse.quote(urllib.parse.quote(station_name))
        url = ("https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?"
                  "command=viewMain&"
                  "station={}&"
                  "stname={}&"
                  "datepicker={}".format(station_code, st_name_encoded, date))
        return url

    def run(self, start_date, end_date, station_reference):
        date_list = self.date_creator(start_date, end_date)
        for station_code, station_name in station_reference.items():
            for date in date_list:
                self.result.append(self.url_downloader(date, station_code, station_name))
