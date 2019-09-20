# Weather_data_spider
Get hourly data from [weather stations](https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp) in Taiwan

The spider of weather data is consist of 4 parts:
- weather_1_station_collector.py: Downlaod station data such as id and name for generating url, and create station table.
- weather_2_url_downloader.py: Generate url using station name, id and date provided
- weather_3_html_downloader.py: Download html from given url.
- weather_4_html_processor.py: Extract data from html and save as csv file.

How to use it:
1. Select stations by typing the city: ex. 台北市
 - if there are multiple cities separate them by comma ",". ex. 台北市,基隆市,新北市
2. Type begin date in YYYY-MM-DD format. ex. 2018-01-01
3. Type end date in YYYY-MM-DD format. ex. 2018-01-01
  - Note: end date won't be included, if you type 2018-01-01 as begin date and 2018-01-03 as end date, the spider will search 2018-01-01 and 2018-01-02 only. 


Web page:


|Home Page|Data Page|
| ------------- |:-------------:|
|![](https://github.com/ShihWen/Weather_data_spider/blob/master/image/weather_web_1.png)|![](https://github.com/ShihWen/Weather_data_spider/blob/master/image/weather_web_2.png)|

Output:


|Station Data|Weather Data|
| ------------- |:-------------:|
|![](https://github.com/ShihWen/Weather_data_spider/blob/master/image/station_data.png)|![](https://github.com/ShihWen/Weather_data_spider/blob/master/image/weather_data.png)|
