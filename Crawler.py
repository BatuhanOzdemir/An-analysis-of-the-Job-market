import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
     level=logging.INFO)

class Crawler:
    def __init__(self, urls=[]):
        self.urls_for_job_ads = []
        self.visited_urls = open("urls_visited.csv","r+",newline='',encoding="utf-8")
        self.urls_to_visit = urls

    def download_url(self, url):
        if url is not None:
            return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        pony = soup.findAll('a')
        for link in pony:
            path = link.get("href")
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.urls_to_visit and self.in_csv(url) and self.sanitizeToVisitList(url):
            if url.__contains__("is-ilani")and any(a.isdigit() for a in url):
                self.urls_for_job_ads.append(url)

            self.urls_to_visit.append(url)

    def sanitizeToVisitList(self,url):
        exclusionList = ["apple","google","cimri","instagram","twitter","facebook","ik-blog",
                            "tercih","pozisyonlar","universite","kariyer-rehberi","bolumler",
                            "kariyer-kampuste","kariyer-gunleri","tercih-motoru",]
        for unwantedURL in exclusionList:
            if url is None or url.__contains__(unwantedURL):
                return False
        return True

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit and len(self.urls_for_job_ads) <= 100:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling:{url}')
            try:
                self.crawl(url)
            except:
                logging.exception(f'Failed to Crawl:{url}')
            finally:
                self.writeToCsv(url)
        self.visited_urls.close()

    def get_urls_for_job_ads(self):
        return self.urls_for_job_ads

    def writeToCsv(self, url):
        csv_writer = csv.writer(self.visited_urls)
        csv_writer.writerow(url,)

    def in_csv(self, url):
        csv_reader = csv.reader(self.visited_urls,delimiter=' ')
        for row in csv_reader:
            if row == url:
                return False
        return True
