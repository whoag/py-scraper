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

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
links_with_text = []
def parse_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    t.sleep(3)
    for a in soup.find_all('a', href=True, class_='css-1422juy'):
        if a.text:
            links_with_text.append(a['href'])

# save only business URL
def clean_urls(links_with_text):
    info_scraped = {}
    final_city_links = []
    for link in links_with_text:
        if link[0:5] == "/biz/":
            print(link)
            final_city_links.append("https://www.yelp.com" + link)
    print(final_city_links)
    return final_city_links


# main function takes in list of page numbers as input and scraps it
def main():
    count = [10,20,30,40,50]
    for m in count:
        yelp_url = "https://www.yelp.com/search?cflt=restaurants&find_loc=Detroit%2C+MI&sortby=rating&start=" + str(m)
        print(m)
        parse_url(yelp_url)
    final_links = clean_urls(links_with_text)
    df = pd.DataFrame({'URL': final_links})
    df.to_csv("url_yelp_new.csv")


if __name__ == "__main__":
    main()
