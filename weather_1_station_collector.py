import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


class stationCollector():
    def __init__(self, *args):
        self.root_dict = {'台北市':'466910','新北市':'466880','台中市':'467490',
                          '台南市':'467410','高雄市':'467440','基隆市':'466940',
                          '桃園市':'467050','新竹市':'C0D570','新竹縣':'467571',
                          '苗栗縣':'C0E420','南投縣':'467550','彰化縣':'C0G620',
                          '雲林縣':'C0F9Q0','嘉義縣':'467530','嘉義市':'467480',
                          '屏東縣':'467590','宜蘭縣':'467060','花蓮縣':'466990',
                          '台東縣':'467540','澎湖縣':'467300','金門縣':'467110',
                          '連江縣':'467990'}
        self.root_id = []
        for city in args:
            if city in self.root_dict.keys():
                self.root_id.append(self.root_dict[city])
            else:
                print("{} not in the dictionary")

        self.url_root = []
        self.id_for_form_data = []
        self.station_list = []

        self.station_raw = []
        self.station_final = []
        self.dict_for_urlDownloader = {}
        self.df = None

    def root_url_generator(self):
        for root_id in self.root_id:
            self.url_root.append('https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?'
                                  'command=viewMain&'
                                  'station={}&'
                                  'stname=%25E6%259D%25BF%25E6%25A9%258B&'
                                  'datepicker=2019-07-01'.format(root_id))

    def station_id_generator(self):
        for url in self.url_root:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            station_id = [x.text.split('_')[0] for x in soup.select('select#selectStno option')]

            for id_ in station_id:
                self.id_for_form_data.append(id_)

    def station_downloader_single(self, id_):
        url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/QueryDataController.do?command=doQueryStation'
        form_data = {'station_no': id_}
        r = requests.post(url, data=form_data)
        self.station_raw.append(r.text)

    def station_downloader_multi(self):
        print("Getting {} station data...".format(len(self.id_for_form_data)))
        start = datetime.datetime.now()
        processes = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for id_ in self.id_for_form_data:
                processes.append(executor.submit(self.station_downloader_single, id_))

        total_time = datetime.datetime.now() - start
        print('Runtime for station download: {}'.format(total_time))

    def station_refined(self):
        for station in self.station_raw:
            station = station.strip().split('|')
            station[4] = station[4].replace('m','')
            self.station_final.append(station)

    def to_df(self, save_df):
        print("Generating Dataframe...")
        st_header = ['st_name','st_code','long','lat','alt','city'
                     ,'addr','owner','type','Eng_name','code',
                     'established','end']

        self.df = pd.DataFrame(self.station_final,columns=st_header).drop(['addr','code'],axis=1)
        if save_df == True:
            self.df.to_csv('station_info.csv',encoding='utf-8',index=False)

    def dict_for_url_downloader(self):
        for item in self.station_final:
            self.dict_for_urlDownloader[item[1]] = item[0]

    def run(self, save_df):
        self.root_url_generator()
        self.station_id_generator()
        self.station_downloader_multi()
        self.station_refined()
        self.dict_for_url_downloader()
        self.to_df(save_df)
