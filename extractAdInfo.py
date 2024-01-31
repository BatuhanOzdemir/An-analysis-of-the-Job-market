from Crawler import Crawler
from bs4 import BeautifulSoup
from JobAd import JobAd
import xlsxwriter
import requests
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
            ad_info = soup.findAll(name="script", attrs={"type": "text/javascript", "data-n-head": "ssr"})
            ad_update_date = soup.find("div", {"class": "updated-date"}).getText()
            ad_content = soup.find("div", {"class": "job-detail-content"}).getText()
            ad_obj = JobAd(ad_info, ad_update_date, ad_content)
            ads_list.append(ad_obj)
        except AttributeError:  # Sometimes the information like update date is missing which is causing an Attribute error.
            continue
    return ads_list

listOfAds = gather_ads()

# Creating an Excel file
fields = ["Çalışma Şekli", "Sektör", "Firma", "İlani Veren Firma", "Pozisyon", "İlan-ID", "Lokasyon",
          "İlan-Statüsü", "Detail-Aday", "İlan-Metni", "Son-Güncelleme"]

workbook = xlsxwriter.Workbook("Kariyer.xlsx")
worksheet = workbook.add_worksheet()

# Write header row
for col, field in enumerate(fields):
    worksheet.write(0, col, field)

# Write data rows
for row, ad in enumerate(listOfAds, start=1):
    info_list = ad.get_info()
    for col, data in enumerate(info_list):
        worksheet.write(row, col, data)

workbook.close()

end = time.time()
print("It took", end - start)
