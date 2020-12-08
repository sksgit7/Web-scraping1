# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest # req to send request using splash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which

class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['http://www.livecoin.net/en/']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        chrome_path= which('chromedriver')

        driver = webdriver.Chrome(executable_path=chrome_path, options= chrome_options)
        driver.set_window_size(1920, 8000)
        driver.get("https://www.livecoin.net/en")

        ltc_tab= driver.find_elements_by_class_name('filterPanelItem___2z5Gb ')[2]
        ltc_tab.click()

        self.html= driver.page_source # we will send it to parse()
        driver.close()

    def parse(self, response):
        resp= Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }
