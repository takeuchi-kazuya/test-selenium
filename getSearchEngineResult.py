#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Debug
# from pprint import pprint

'''
    @param browser {string}: target search engine
    @param query {string}: search keyword
'''

# browser = 'google'
browser = 'yahoo'
query = 'Python'

# Create option
options = Options()
# Add option headless
options.add_argument('--headless')
# Path to ChromeDriver and create webdriver
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

if browser == 'google':
    driver.get("https://www.google.co.jp")
    assert 'Google' in driver.title
    input_elem = driver.find_element_by_name('q')

if browser == 'yahoo':
    driver.get("https://www.yahoo.co.jp")
    assert 'Yahoo' in driver.title
    input_elem = driver.find_element_by_name('p')


input_elem.clear()
input_elem.send_keys(query)
input_elem.send_keys(Keys.RETURN)

# Wait for an appropriate time to wait for screen change
time.sleep(2)

# Check for title is `query`
assert query in driver.title
assert "No results found." not in driver.page_source

# Take a Screenshot
driver.save_screenshot('cap.png')

# Show results
if browser == 'google':
    for a in driver.find_elements_by_css_selector('.g .rc .r > a:first-child'):
        print(a.get_attribute('href'))

    for b in driver.find_elements_by_css_selector('.g .rc .r > a:first-child h3'):
        print(b.text)

if browser == 'yahoo':
    for a in driver.find_elements_by_css_selector('.w .hd a'):
        print(a.get_attribute('href'))
        print(a.text)

# result write to CSV file
columns = ["name", "url"]
df2 = pd.DataFrame(columns=columns)

if browser == 'google':
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find("div", {"id":"search"})
    tags = soup.find_all("div", {"class":"g"})
    for tag in tags:
        name = tag.a.h3.text
        url = tag.a.get('href')
        se = pd.Series([name, url], columns)
        df2 = df2.append(se, columns)

if browser == 'yahoo':
    for a in driver.find_elements_by_css_selector('.w .hd a'):
        name = a.text
        url = a.get_attribute('href')
        se = pd.Series([name, url], columns)
        df2 = df2.append(se, columns)

filename = "result.csv"
df2.to_csv(filename, encoding = 'utf-8-sig')

driver.close()
