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
        self.visited_urls_path = "urls_visited.csv"
        self.visited_urls = set()
        self.load_visited_urls()
        self.urls_to_visit = urls

    def load_visited_urls(self):
        try:
            with open(self.visited_urls_path, "r", encoding="utf-8") as csv_reader:
                csv_reader = csv.reader(csv_reader, delimiter=',')
                for row in csv_reader:
                    if row:
                        self.visited_urls.add(row[0])
        except FileNotFoundError:
            logging.warning("No existing visited URLs file found.")

    def save_visited_url(self, url):
        with open(self.visited_urls_path, "a", encoding="utf-8", newline='') as csv_writer:
            csv_writer = csv.writer(csv_writer, dialect="excel")
            csv_writer.writerow([url])

    def download_url(self, url):
        if url is not None:
            return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        pony = soup.find_all('a')
        for link in pony:
            path = link.get("href")
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.urls_to_visit and url not in self.visited_urls and self.sanitize_to_visit_list(url):
            if url.__contains__("is-ilani") and any(a.isdigit() for a in url):
                self.urls_for_job_ads.append(url)

            self.urls_to_visit.append(url)

    def sanitize_to_visit_list(self, url):
        exclusion_list = ["apple", "google", "cimri", "instagram", "twitter", "facebook", "ik-blog",
                          "tercih", "pozisyonlar", "universite", "kariyer-rehberi", "bolumler",
                          "kariyer-kampuste", "kariyer-gunleri", "tercih-motoru"]
        for unwanted_url in exclusion_list:
            if url is None or unwanted_url in url:
                return False
        return True

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit and len(self.urls_for_job_ads) <= 5000:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling:{url}')
            try:
                self.crawl(url)
            except Exception as e:
                logging.exception(f'Failed to Crawl:{url} - {str(e)}')
            finally:
                self.save_visited_url(url)
        self.visited_urls.clear()  # Clear the set after the run

    def get_urls_for_job_ads(self):
        return self.urls_for_job_ads


