# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    #start_urls = ['http://quotes.toscrape.com/js/']

    script='''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
        '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse,
                        endpoint='execute',args={'lua_source':self.script})
    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            yield{
                'text': quotes.xpath(".//span[@class='text']/text()").get(),
                'author':quotes.xpath(".//small[@class='author']/text()").get(),
                'tags':quotes.xpath(".//div[@class='tags']/a/text()").getall()

            }
        next_page= response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            abs_url=f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=abs_url, callback=self.parse, endpoint='execute',
                                args={'lua_source':self.script})
