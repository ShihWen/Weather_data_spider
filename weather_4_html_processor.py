from bs4 import BeautifulSoup
import pandas as pd
import re
import sys


class htmlExtractor():
    def __init__(self):
        self.result = []
        self.header = None
        self.df = None

    def html_extractor(self, html):
        #Data Source
        soup = BeautifulSoup(html, 'lxml')
        station = soup.select('div#hea_t table tr td')[1].text.strip().split(':')[1]
        #data_date = soup.select('div#hea_t table tr td')[-4].text.split(':')[1]
        data_date = soup.find('div',{'id':'hea_t'}).find('td',text=re.compile('觀測時間')).text.split(':')[1]


        if self.header == None:
            self.table_header(soup)

        #Content
        row_len = len(soup.select('table#MyTable tbody tr'))
        for i in range(3,row_len):
            row = soup.select('table#MyTable tbody tr')[i].text.strip().replace('\xa0','').split('\n')
            row.insert(0,data_date)
            row.insert(1,station.split('_')[0])
            row.insert(2,station.split('_')[1])
            self.result.append(row)

    def cleaning(self):
        for item in self.result:
            for i in range(len(item)):
                if item[i] == '...' or item[i] == '/' or item[i] == 'X' or item[i] == 'T':
                    item[i] = '0'
                if item[i] == 'V':
                    item[i] = -1

    def table_header(self, soup):
        header = soup.select('table#MyTable tbody tr.second_tr')[0].text.strip().split('\n')
        header.insert(0,'觀測日期')
        header.insert(1,'測站名')
        header.insert(2,'測站代號')
        self.header = header

    def run(self, html_list):
        count = 0
        for html in html_list:
            sys.stdout.write('\rProcessed {} html...'.format(count))
            self.html_extractor(html)
            count += 1
        self.cleaning()
        self.df = pd.DataFrame(self.result,columns=self.header).to_csv('weather_data.csv',index=False)
