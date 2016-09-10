# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from springer.items import SpringerBookItem
import time

class BookSpider(CrawlSpider):
    subject = 'Physics'
    name = "book"
    allowed_domains = ["link.springer.com"]
    start_urls = (
        'http://link.springer.com/search?facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&date-facet-mode=between&facet-start-year=2000&previous-start-year=2000&facet-end-year=2003&previous-end-year=2008',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Physics%22&previous-end-year=2008&facet-content-type=%22Chapter%22&previous-start-year=2000&facet-start-year=2000&sortOrder=oldestFirst&facet-end-year=2003',
'http://link.springer.com/search?facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2004&previous-start-year=2004&facet-end-year=2006&previous-end-year=2005',
'http://link.springer.com/search?facet-end-year=2006&date-facet-mode=between&facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&sortOrder=newestFirst&previous-end-year=2005&previous-start-year=2004&facet-start-year=2004',
'http://link.springer.com/search?sortOrder=newestFirst&facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&date-facet-mode=between&facet-start-year=2007&previous-start-year=2004&facet-end-year=2008&previous-end-year=2006',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Physics%22&facet-start-year=2007&facet-content-type=%22Chapter%22&previous-start-year=2004&sortOrder=oldestFirst&previous-end-year=2006&facet-end-year=2008',
'http://link.springer.com/search?facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2009&previous-start-year=2007&facet-end-year=2010&previous-end-year=2008',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Physics%22&previous-end-year=2008&facet-content-type=%22Chapter%22&sortOrder=newestFirst&facet-start-year=2009&previous-start-year=2007&facet-end-year=2010',
'http://link.springer.com/search?sortOrder=newestFirst&facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&date-facet-mode=between&facet-start-year=2011&previous-start-year=2011&facet-end-year=2013&previous-end-year=2011',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&previous-start-year=2011&facet-start-year=2011&sortOrder=oldestFirst&previous-end-year=2011&facet-end-year=2013',
'http://link.springer.com/search?facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2014&previous-start-year=2011&facet-end-year=2015&previous-end-year=2013',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Physics%22&facet-end-year=2015&facet-start-year=2014&previous-end-year=2013&facet-content-type=%22Chapter%22&previous-start-year=2011&sortOrder=newestFirst',
'http://link.springer.com/search?sortOrder=newestFirst&facet-discipline=%22Physics%22&facet-content-type=%22Chapter%22&date-facet-mode=between&facet-start-year=2016&previous-start-year=2014&facet-end-year=2016&previous-end-year=2015'
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
        loader.add_value('subject',self.subject)
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