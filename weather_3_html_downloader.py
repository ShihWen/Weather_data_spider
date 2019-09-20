import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class htmlDownloader():
    def __init__(self):
        self.result = []
    
    def html_downloader(self, url):
        r = requests.get(url)
        self.result.append(r.text)

    def run(self, url_list):
        print("Getting {} htmls...".format(len(url_list)))
        start = datetime.datetime.now()
        processes = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for url in url_list:
                processes.append(executor.submit(self.html_downloader, url))

        total_time = datetime.datetime.now() - start
        print('Runtime for html download: {}'.format(total_time))
