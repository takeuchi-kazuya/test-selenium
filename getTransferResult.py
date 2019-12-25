#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Debug
# from pprint import pprint

'''
    @param departure {string}: departure station
    @param arrival {string}: arrival station
'''

siteUrl = "https://transit.yahoo.co.jp/"
departure = "東京"
arrival = "新宿"

print(departure + "駅から" + arrival + "駅への直近の電車を調べます...")

# Create option
options = Options()
# Add option headless
options.add_argument('--headless')
# Path to ChromeDriver and create webdriver
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.get(siteUrl)
driver.find_element_by_id("sfrom").send_keys(unicode(departure, 'utf-8'))
driver.find_element_by_id("sto").send_keys(unicode(arrival, 'utf-8'))
driver.find_element_by_id("searchModuleSubmit").click()

soup = BeautifulSoup(driver.page_source, "html.parser")
line = soup.select("#route01 .transport div")[0].text
time = soup.select(".routeSummary li.time")[0].select("span")[0].text

# Show results
print(line)
print(time)

driver.close()
