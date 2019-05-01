"""
Date: 4/20/2019
Author: Raymond Pistoresi
Version: 1.01
Citation: This code is a modified version of the source 
https://github.com/shreyas707/Amazon-Review-Scraper/blob/master/amazon_review_scraper/amazon_review_scraper.py
"""
from requests import get
from random import randint
from bs4 import BeautifulSoup
import time
import urllib
import ssl
import pdb
import requests
import csv

class amazon_review_scraper:

    # Ignore SSL certificate errors
    ssl._create_default_https_context = ssl._create_unverified_context
    csv_data = []
    csv_head = ["ASIN", "Rating", "Title", "Verified Purchase", "Body"]

    def __init__(self, url, start_page, end_page, time_upper_limit):
        self.url = url
        self.set_url()
        self.start_page = int(start_page)
        self.end_page = int(end_page)
        self.time_upper_limit = time_upper_limit

    def set_sleep_timer(self):
        sleep_time = randint(0, int(self.time_upper_limit))
        print("\nSleeping for " + str(sleep_time) + " seconds.")
        time.sleep(sleep_time)

    def set_url(self):
        # removing pageNumber parameter if it exists in the url
        url = self.url.split("&pageNumber")
        if len(url) > 1:
            self.url = url[0]
        else :
            self.url = url

    def set_start_page(self, start_page):
        url = self.url + "&pageNumber=" + str(start_page)
        return url

    def build_rating(self, review):
        return str(review).split("<span class=\"a-icon-alt\">")[1].split("</span>")[0].split(" ")[0]

    def build_title(self, review):
        return str(review).split("data-hook=\"review-title\"")[1].split("<span")[1].split(">")[1].split("</span")[0]

    def build_date(self, review):
        return str(review).split("data-hook=\"review-date\">")[1].split("</span>")[0]

    def build_verified_purchase(self, review):
        # Yes = purchased, No = not purchased
        try: 
            str(review).split("data-hook=\"avp-badge\">")[1].split("</span>")[0]
            return "Yes"
        except:
            return "No"

    def build_body(self, review):
        body = str(review).split("data-hook=\"review-body\">")[1].split("</span>")[0]
        body = body.replace("<br>", ".").replace("<br/>", ".").replace("</br>", ".").strip()
        body = body.split(">")[-1]
        return body

    def build_votes(self, review):
        try :
            votes = str(review).split("data-hook=\"helpful-vote-statement\"")[1].split(">")[1].split("<")[0].strip().split()
            if votes[0] == "One" :
                return "1"
            else :
                return votes[0]
        except :
            return "0"

    def scrape(self, asin):
        start_page = self.start_page
        end_page = self.end_page

        if end_page < start_page:
            print("Start page cannot be greater than end page. Please try again.")
            exit()

        self.csv_data.append(self.csv_head)

        print('scrapping loop')
        while start_page <= end_page :
            try:
                url = self.set_start_page(start_page)
            except:
                print("URL entered is wrong. Please try again with the right URL.")
                exit()

            # Sleep because Amazon might block your IP if there are too many requests every second
            self.set_sleep_timer()

            print("Scraping page " + str(start_page) + ".")

            # Amazon blocks requests that don't come from browser. Hence need to mention user-agent
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
            headers = {'User-Agent' : user_agent}

            values = {}

            data = urllib.parse.urlencode(values).encode('utf-8')
            req = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(req)
            html = response.read()

            # soup = BeautifulSoup(cleaned_response, 'lxml')
            soup = BeautifulSoup(html, 'lxml')

            # reviews = soup.find_all("div", attrs={"class": "a-section review"})
            reviews = soup.find_all("div", class_="a-section review aok-relative")

            for review in reviews :

                csv_body = []

                # ASIN Number
                csv_body.append(asin)

                # Star Rating
                rating = self.build_rating(review)
                csv_body.append(rating)

                # Title
                title = self.build_title(review)
                csv_body.append(title)

                # Verified Purchase
                verified_purchase = self.build_verified_purchase(review)
                csv_body.append(verified_purchase)

                # Body
                body = self.build_body(review)
                csv_body.append(body)

                self.csv_data.append(csv_body)

            start_page += 1

    def write_csv(self, file_name):
        print("\nWriting to file.\n")

        with open((file_name + '.csv'), 'w') as csv_file :
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(self.csv_data)

if __name__ == "__main__":
    products = [
        { "asin": 'B000IYSAIW', "url": 'https://www.amazon.com/Bergan-Turbo-Scratcher-Colors-vary/product-reviews/B000IYSAIW/ref=cm_cr_arp_d_paging_btm_next_7?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1' },
        { "asin": 'B009R3SFBC', "url": 'https://www.amazon.com/Cat-Amazing-Interactive-Puzzle-Feeder/product-reviews/B009R3SFBC/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1' },
        { "asin": 'B072WCZQ4V', "url": 'https://www.amazon.com/Friends-Forever-Interactive-Cat-Laser/product-reviews/B072WCZQ4V/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1' },
        { "asin": 'B06WP7F8YC', "url": 'https://www.amazon.com/SmartyKat-Hot-Pursuit-Concealed-Motion/product-reviews/B06WP7F8YC/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1' },
        { "asin": 'B00TTU9RAQ', "url": 'https://www.amazon.com/HEXBUG-nano-Robotic-Cat-Toy/product-reviews/B00TTU9RAQ/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1' }
    ]
    for p in products:
        ars = amazon_review_scraper(p["url"],1,100,3)
        ars.scrape(p["asin"])
        ars.write_csv("reviews_" + p["asin"])
