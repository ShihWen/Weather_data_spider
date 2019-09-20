from weather_1_station_collector import stationCollector
from weather_2_url_downloader import urlDownloader
from weather_3_html_downloader import htmlDownloader
from weather_4_html_processor import htmlExtractor
import datetime

class weatherSpider():
    def __init__(self):
        self.station_info = stationCollector('台北市','新北市','基隆市')
        self.begin_date = input("Please type begin date of data (ex. '2019-01-01'):")
        self.end_date = input("Please type end date (not included) of data (ex. '2019-01-10'):")
        self.url_downloader = urlDownloader()
        self.html_downloader = htmlDownloader()
        self.html_processor = htmlExtractor()

    def run(self):
        start = datetime.datetime.now()
        self.station_info.run(save_df=False)
        self.url_downloader.run(self.begin_date,
                                self.end_date,
                                self.station_info.dict_for_urlDownloader)
        self.html_downloader.run(self.url_downloader.result)
        self.html_processor.run(self.html_downloader.result)

        total_time = datetime.datetime.now() - start
        print('\nRuntime for Whole process : {}'.format(total_time))

if __name__ == "__main__":
    obj = weatherSpider()
    obj.run()
