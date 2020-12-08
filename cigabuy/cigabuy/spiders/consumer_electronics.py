# -*- coding: utf-8 -*-
import scrapy


class ConsumerElectronicsSpider(scrapy.Spider):
    name = 'consumer_electronics'
    allowed_domains = ['www.cigabuy.com']
    # we can comment 'start_urls' as we have defined start_requests()
    #start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    # spoof request headers
    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html' , callback=self.parse,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58'
        })

    def parse(self, response):
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            yield {
                'title': product.xpath(".//div/a[@class='p_box_title']/text()").get(),
                # the product urls are relative urls, so we need to join with domain name
                'url': response.urljoin(product.xpath(".//div/a[@class='p_box_title']/@href").get()),
                'discounted_price': product.xpath(".//div/div[@class='p_box_price']/span[1]/text()").get(),
                'original_price': product.xpath(".//div/div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }
        # ping next page url            
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        # if there is next page available, then again call parse() method to scrape it
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58'
            }) # change request headers using 'headers'
