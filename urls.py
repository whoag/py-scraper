import datetime

from bs4 import BeautifulSoup
import requests
from lxml import html
import csv
import requests
from time import sleep
import re
import argparse
import sys
import pandas as pd
import time as t
import sys
import numpy as np
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
df = pd.read_csv('url_yelp_new.csv')
urls = df['URL'].tolist()
iteration_from = 60
iteration_end = len(urls)

review_data = []
final_data = []
biz_urls = []


def res_scraper(url):
    try:
        driver.get(url)
    except:
        return
    t.sleep(3)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    soup2 = BeautifulSoup(page, 'html.parser')
    info_scraped = []
    # retrieve the total page number
    final_tag = ''
    final_address = ''
    #
    # info_scraped['restaurant_name'] = None
    # info_scraped['restaurant_address'] = None
    # info_scraped['ratings'] = None
    # info_scraped['phone_number'] = None
    # info_scraped['restaurant_website'] = None

    # retrieve restaurant name
    try:
        name = soup.find('h1').text
        info_scraped.append(name)
    except:
        info_scraped.append("null")

    # retrieve address and append road, city, zip code to one string
    try:
        addresses = soup.find('address').find('p').find_all('span', {'class': 'raw__09f24__T4Ezm'})
        addresses2 = soup.find('address').find('p', {'class': 'css-1k57hak'}).find_all('span',
                                                                                       {'class': 'raw__09f24__T4Ezm'})

        for address in addresses:
            final_address += address.text + ','
        for address in addresses2:
            final_address += address.text + ','
        baddress = final_address
        info_scraped.append(baddress)
    except:
        info_scraped.append("null")

    # retrieve the average rating of each restaurant
    try:
        ratings = soup.find('div', {'aria-label': re.compile(' star rating')})['aria-label']
        info_scraped.append(ratings)
    except:
        info_scraped.append("null")
    try:

        phone = soup.find_all('p', {'class': 'css-1h7ysrc', 'data-font-weight': 'semibold'})[16].text
        info_scraped.append(phone)
    except:
        info_scraped.append("null")
    try:

        site = soup.find_all('p', {'class': 'css-1h7ysrc'})[15].find('a').text
        info_scraped.append(site)
        biz_urls.append(site)
    except:
        info_scraped.append("null")

    final_data.append(info_scraped)

    return final_data


def run(urlList):
    count = len(urlList)
    for i in range(10):
        resreview = res_scraper(urlList[i])
        review_data.append(resreview)
        i = i + 1
        print(i)

    df = pd.DataFrame(final_data)
    df1 = pd.DataFrame(biz_urls)
    # review_all = pd.concat(df)
    df.to_csv("test.csv", encoding='utf-8-sig', header=['Name', 'Address', 'Rating', 'Phone', 'Website'])
    df1.to_csv("biz_sites.csv", encoding='utf-8-sig', header=['URL'])
    driver.quit()


run(urls)
