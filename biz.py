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
        name = soup.find('div', {'class': 'fn, org'}).text
        info_scraped.append(name)
    except:
        info_scraped.append("null")

    # retrieve address and append road, city, zip code to one string
    try:
        street = soup.find_all('div', {'class': 'adr'}).find('span', {'class': 'street-address'}).text
        city = soup.find_all('div', {'class': 'adr'}).find('span', {'class': 'street-address'}).text
        info_scraped.append(street + city)
    except:
        info_scraped.append("null")

    # # retrieve the average rating of each restaurant
    # try:
    #     ratings = soup.find('div', {'aria-label': re.compile(' star rating')})['aria-label']
    #     info_scraped.append(ratings)
    # except:
    #     info_scraped.append("null")
    try:

        phone = soup.find_all('div', {'class': 'tel'}).text
        info_scraped.append(phone)
    except:
        info_scraped.append("null")
    # try:
    #
    #     site = soup.find_all('p', {'class': 'css-1h7ysrc'})[15].find('a').text
    #     info_scraped.append(site)
    # except:
    #     info_scraped.append("null")

    final_data.append(info_scraped)
    driver.refresh()
    # driver.find_element("Show More").click()
    return final_data


def run():
    for i in range(5):
        resreview = res_scraper("https://us-business.info/directory/detroit-mi/restaurants/")
        review_data.append(resreview)
        i = i + 1
        print(i)

    df = pd.DataFrame(final_data)
    # review_all = pd.concat(df)
    df.to_csv("test.csv", encoding='utf-8-sig', header=['Name', 'Address', 'Phone'])
    driver.quit()


run()
