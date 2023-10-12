from Crawler import Crawler
from bs4 import BeautifulSoup
import requests
from JobAd import JobAd
import csv
import time


crawl = Crawler(urls=['https://kariyer.net'])
start = time.time()
crawl.run()
url_list = crawl.get_urls_for_job_ads()



def gather_ads():
    ads_list = []
    for url in url_list:
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            ad_info = soup.findAll(name="script", attrs={"type":"text/javascript","data-n-head":"ssr"})
            ad_update_date = soup.find("div", {"class": "updated-date"}).getText()
            ad_content = soup.find("div", {"class": "job-detail-content"}).getText()
            ad_obj = JobAd(ad_info,ad_update_date, ad_content)
            ads_list.append(ad_obj)
        except AttributeError:
            continue
    return ads_list


listOfAds = gather_ads()

#creating a csv file
fields = ["Çalışma Şekli","Sektör","Firma","İlani Veren Firma","Pozisyon","İlan-ID","Lokasyon","İlan-Statüsü", "Detail-Aday", "İlan-Metni","Son-Güncelleme"]

with open("Kariyer.csv","w",newline='',encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(fields)

    for ad in listOfAds:
        csv_writer.writerows([ad.get_info()])

end = time.time()
print("It took",end - start)