# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from springer.items import SpringerBookItem
import time

class BookSpider(CrawlSpider):
    name = "book"
    allowed_domains = ["link.springer.com"]
    start_urls = (
        'http://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&facet-start-year=2010&previous-start-year=2009&facet-end-year=2016&previous-end-year=2016',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            'springer.pipelines.MongoBookPipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/search/page/[0-9]*.*'), restrict_xpaths=("//a[@title='next']")),follow=True),
        Rule(LinkExtractor(allow=('/chapter/.*'),restrict_xpaths=('//a[@class="title"]')),follow=True, callback='parse_item')
    )


    def parse_item(self, response):
        loader = ItemLoader(SpringerBookItem(),response)
        loader.add_xpath('title','string(//h1)')
        loader.add_xpath('citation_publisher','//meta[@name="citation_publisher"]/@content')
        loader.add_xpath('citation_firstpage','//meta[@name="citation_firstpage"]/@content')
        loader.add_xpath('citation_lastpage','//meta[@name="citation_lastpage"]/@content')
        loader.add_xpath('doi','//meta[@name="citation_doi"]/@content')
        loader.add_xpath('citation_language','//meta[@name="citation_language"]/@content')
        loader.add_xpath('citation_inbook_title','//meta[@name="citation_inbook_title"]/@content')
        loader.add_xpath('citation_publication_date','//meta[@name="citation_publication_date"]/@content')

        loader.add_xpath('abstract','//p[@id="Par1"]/text()')
        loader.add_value('url',response.url)
        loader.add_value('crawl_date', time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

        for sel in response.xpath('//meta[@name="citation_author_institution"]/@content').extract():
            loader.add_value('institution',sel)

        for sel in response.xpath('//ul[@class="authors"]/li'):
            name = sel.xpath('a[@class="person"]/text()').extract_first()
            email = sel.xpath('a[@class="envelope"]/@title').extract_first()
            loader.add_value('authors',{'name':name,'email':email})


        return loader.load_item()