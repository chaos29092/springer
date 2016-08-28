# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from springer.items import SpringerBookItem

class BookSpider(CrawlSpider):
    name = "book"
    allowed_domains = ["link.springer.com"]
    start_urls = (
        'http://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&facet-start-year=2010&previous-start-year=2009&facet-end-year=2016&previous-end-year=2016',
        'http://link.springer.com/search?facet-start-year=2010&facet-discipline=%22Chemistry%22&facet-end-year=2016&previous-start-year=2009&facet-content-type=%22Chapter%22&previous-end-year=2016&sortOrder=oldestFirst',
        'http://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&facet-start-year=2005&previous-start-year=2004&facet-end-year=2009&previous-end-year=2009',
        'http://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&previous-end-year=2009&previous-start-year=2004&sortOrder=oldestFirst&facet-start-year=2005&facet-end-year=2009',
        'http://link.springer.com/search?facet-end-year=2004&previous-end-year=2004&facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&facet-start-year=2000&sortOrder=oldestFirst&previous-start-year=1999',
        'http://link.springer.com/search?facet-end-year=2004&previous-end-year=2004&facet-discipline=%22Chemistry%22&facet-content-type=%22Chapter%22&facet-start-year=2000&sortOrder=newestFirst&previous-start-year=1999',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            'springer.pipelines.MongoChemistryBookPipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/search\？.*')),follow=False),
        Rule(LinkExtractor(allow=('/search/page/[0-9]*.*'), restrict_xpaths=("//a[@title='next']")),follow=True),
        Rule(LinkExtractor(allow=('/chapter/.*'),restrict_xpaths=('//a[@class="title"]')),follow=True, callback='parse_item')
    )

    def parse_item(self, response):
        loader = ItemLoader(SpringerBookItem(),response)
        loader.add_xpath('title','string(//h1)')
        loader.add_xpath('book_title','//p[@class="BookTitle"]/a/text()')
        loader.add_xpath('first_online','//span[@class="version-date"]/time/text()')
        loader.add_xpath('doi','//dd[@id="abstract-about-book-chapter-doi"]/text()')
        loader.add_xpath('copyright_year','//dd[@id="dt-abstract-about-book-chapter-copyright-year"]/text()')
        loader.add_xpath('copyright_holder','//dd[@id="abstract-about-book-copyright-holder"]/text()')
        loader.add_xpath('publisher','//dd[@id="abstract-about-publisher"]/text()')
        loader.add_xpath('series_issn','//dd[@id="abstract-about-book-series-print-issn"]/text()')
        loader.add_xpath('series_volume','//dd[@id="abstract-about-book-series-volume"]/text()')
        loader.add_xpath('pages','//dd[@id="abstract-about-book-chapter-page-ranges"]/text()')
        loader.add_xpath('abstract','//p[@id="Par1"]/text()')
        loader.add_value('url',response.url)

        for sel in response.xpath('//ul[@class="authors"]/li'):
            name = sel.xpath('a[@class="person"]/text()').extract_first()
            email = sel.xpath('a[@class="envelope"]/@title').extract_first()
            loader.add_value('authors',{'name':name,'email':email})

        for sel in response.xpath('//ul[@class="author-affiliations"]/li'):
            affiliation = sel.xpath('span[@class="affiliation"]/text()').extract_first()
            loader.add_value('affiliation',affiliation)

        return loader.load_item()