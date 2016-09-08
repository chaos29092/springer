# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from springer.items import SpringerItem
import time



class ArticleSpider(CrawlSpider):
    subject = ''
    name = "article"
    allowed_domains = ["link.springer.com"]
    start_urls = (
        'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Chemistry%22&date-facet-mode=between&facet-start-year=2011&previous-start-year=2012&facet-end-year=2011&previous-end-year=2012',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            'springer.pipelines.MongoArticlePipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/search/page/[0-9]*.*'), restrict_xpaths=("//a[@title='next']")),follow=True),
        Rule(LinkExtractor(allow=('/article/.*'),restrict_xpaths=('//a[@class="title"]')),follow=True, callback='parse_item')
    )
    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        loader = ItemLoader(SpringerItem(),response)
        loader.add_xpath('title','//h1/text()')
        loader.add_xpath('first_online','//dd[@class="article-dates__first-online"]/time/text()')
        loader.add_xpath('doi','//p[@class="article-doi"]/text()')
        loader.add_xpath('cite_this','//dd[@id="citethis-text"]/text()')
        loader.add_xpath('journal_title','//span[@class="JournalTitle"]/text()')
        loader.add_xpath('citation_year','//span[@class="ArticleCitation_Year"]/time/text()')
        loader.add_xpath('citation_volume','//span[@class="ArticleCitation_Volume"]/text()')
        loader.add_xpath('citation_issue','//a[@class="ArticleCitation_Issue"]/text()')
        loader.add_xpath('citation_pages','//span[@class="ArticleCitation_Pages"]/text()')
        loader.add_xpath('views','//span[@class="article-metrics__views"]/text()')
        loader.add_xpath('abstract','//p[@id="Par1"]/text()')
        loader.add_value('url',response.url)
        loader.add_value('crawl_date', time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        loader.add_value('subject',self.subject)


        for sel in response.xpath('//ul[@data-component="SpringerLink-Authors"]/li'):
            name = sel.xpath('span[@data-role="author__name"]/text()').extract_first()
            email = sel.xpath('div/div/div/a[@itemprop="email"]/@href').extract_first()
            if email:
                email = email[7:]
            department = sel.xpath('div/ul/li[@itemprop="affiliation"]/*/text()').extract()
            loader.add_value('authors',{'name':name,'email':email,'department':department,})

        return loader.load_item()
