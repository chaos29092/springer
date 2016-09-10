# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from springer.items import SpringerItem
import time



class ArticleSpider(CrawlSpider):
    subject = 'Medicine'
    name = "article"
    allowed_domains = ["link.springer.com"]
    start_urls = (
        'http://link.springer.com/search?facet-discipline=%22Medicine%22&facet-content-type=%22Article%22&date-facet-mode=between&facet-start-year=2000&previous-start-year=1832&facet-end-year=2000&previous-end-year=2017',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2001&previous-start-year=2000&facet-end-year=2001&previous-end-year=2000',
'http://link.springer.com/search?date-facet-mode=between&facet-end-year=2001&previous-start-year=2000&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&facet-start-year=2001&previous-end-year=2000&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2002&previous-start-year=2001&facet-end-year=2002&previous-end-year=2001',
'http://link.springer.com/search?date-facet-mode=between&previous-end-year=2001&sortOrder=newestFirst&facet-discipline=%22Medicine%22&previous-start-year=2001&facet-end-year=2002&facet-content-type=%22Article%22&facet-start-year=2002',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2003&previous-start-year=2002&facet-end-year=2003&previous-end-year=2002',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2004&previous-start-year=2003&facet-end-year=2004&previous-end-year=2003',
'http://link.springer.com/search?date-facet-mode=between&facet-end-year=2004&previous-start-year=2003&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&previous-end-year=2003&facet-content-type=%22Article%22&facet-start-year=2004',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2005&previous-start-year=2004&facet-end-year=2005&previous-end-year=2004',
'http://link.springer.com/search?date-facet-mode=between&previous-end-year=2004&facet-end-year=2005&sortOrder=newestFirst&facet-discipline=%22Medicine%22&previous-start-year=2004&facet-start-year=2005&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2006&previous-start-year=2005&facet-end-year=2006&previous-end-year=2005',
'http://link.springer.com/search?facet-end-year=2006&date-facet-mode=between&previous-start-year=2005&facet-start-year=2006&previous-end-year=2005&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2007&previous-start-year=2006&facet-end-year=2007&previous-end-year=2006',
'http://link.springer.com/search?date-facet-mode=between&facet-start-year=2007&sortOrder=newestFirst&facet-discipline=%22Medicine%22&facet-end-year=2007&previous-end-year=2006&previous-start-year=2006&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2008&previous-start-year=2007&facet-end-year=2008&previous-end-year=2007',
'http://link.springer.com/search?date-facet-mode=between&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&previous-start-year=2007&facet-end-year=2008&facet-start-year=2008&previous-end-year=2007&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2009&previous-start-year=2008&facet-end-year=2009&previous-end-year=2008',
'http://link.springer.com/search?date-facet-mode=between&previous-end-year=2008&sortOrder=newestFirst&previous-start-year=2008&facet-discipline=%22Medicine%22&facet-start-year=2009&facet-end-year=2009&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2010&previous-start-year=2009&facet-end-year=2010&previous-end-year=2009',
'http://link.springer.com/search?date-facet-mode=between&facet-start-year=2010&previous-start-year=2009&facet-discipline=%22Medicine%22&previous-end-year=2009&sortOrder=oldestFirst&facet-end-year=2010&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2011&previous-start-year=2010&facet-end-year=2011&previous-end-year=2010',
'http://link.springer.com/search?date-facet-mode=between&previous-start-year=2010&facet-end-year=2011&sortOrder=newestFirst&facet-start-year=2011&facet-discipline=%22Medicine%22&facet-content-type=%22Article%22&previous-end-year=2010',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2012&previous-start-year=2011&facet-end-year=2012&previous-end-year=2011',
'http://link.springer.com/search?facet-end-year=2012&date-facet-mode=between&previous-start-year=2011&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&previous-end-year=2011&facet-start-year=2012&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2013&previous-start-year=2012&facet-end-year=2013&previous-end-year=2012',
'http://link.springer.com/search?date-facet-mode=between&previous-end-year=2012&sortOrder=newestFirst&facet-discipline=%22Medicine%22&previous-start-year=2012&facet-end-year=2013&facet-start-year=2013&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2014&previous-start-year=2013&facet-end-year=2014&previous-end-year=2013',
'http://link.springer.com/search?date-facet-mode=between&facet-start-year=2014&previous-end-year=2013&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&facet-end-year=2014&facet-content-type=%22Article%22&previous-start-year=2013',
'http://link.springer.com/search?facet-content-type=%22Article%22&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&date-facet-mode=between&facet-start-year=2015&previous-start-year=2014&facet-end-year=2015&previous-end-year=2014',
'http://link.springer.com/search?date-facet-mode=between&facet-end-year=2015&previous-start-year=2014&sortOrder=newestFirst&facet-discipline=%22Medicine%22&previous-end-year=2014&facet-start-year=2015&facet-content-type=%22Article%22',
'http://link.springer.com/search?facet-content-type=%22Article%22&sortOrder=newestFirst&facet-discipline=%22Medicine%22&date-facet-mode=between&facet-start-year=2016&previous-start-year=2015&facet-end-year=2016&previous-end-year=2015',
'http://link.springer.com/search?date-facet-mode=between&previous-end-year=2015&previous-start-year=2015&facet-end-year=2016&facet-discipline=%22Medicine%22&sortOrder=oldestFirst&facet-start-year=2016&facet-content-type=%22Article%22',
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

    def parse_item(self, response):
        loader = ItemLoader(SpringerItem(),response)
        loader.add_value('subject',self.subject)
        loader.add_xpath('title','//h1/text()')
        loader.add_xpath('first_online','//meta[@name="citation_online_date"]/@content')
        loader.add_xpath('doi','//meta[@name="citation_doi"]/@content')
        loader.add_xpath('citation_publisher','//meta[@name="citation_publisher"]/@content')
        loader.add_xpath('citation_language','//meta[@name="citation_language"]/@content')
        loader.add_xpath('citation_firstpage','//meta[@name="citation_firstpage"]/@content')
        loader.add_xpath('citation_lastpage','//meta[@name="citation_lastpage"]/@content')

        loader.add_xpath('journal_title','//meta[@name="citation_journal_title"]/@content')
        loader.add_xpath('citation_journal_abbrev','//meta[@name="citation_journal_abbrev"]/@content')

        loader.add_xpath('citation_year','//span[@class="ArticleCitation_Year"]/time/text()')
        loader.add_xpath('citation_volume','//span[@class="ArticleCitation_Volume"]/text()')
        loader.add_xpath('citation_issue','//a[@class="ArticleCitation_Issue"]/text()')
        loader.add_xpath('views','//span[@class="article-metrics__views"]/text()')
        loader.add_xpath('abstract','//p[@id="Par1"]/text()')
        loader.add_value('url',response.url)
        loader.add_value('crawl_date', time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

        for sel in response.xpath('//meta[@name="citation_author_institution"]/@content').extract():
            loader.add_value('institution',sel)

        for sel in response.xpath('//ul[@data-component="SpringerLink-Authors"]/li'):
            name = sel.xpath('span[@data-role="author__name"]/text()').extract_first()
            email = sel.xpath('div/div/div/a[@itemprop="email"]/@href').extract_first()
            if email:
                email = email[7:]
            department = sel.xpath('div/ul/li[@itemprop="affiliation"]/*/text()').extract()
            loader.add_value('authors',{'name':name,'email':email,'department':department,})

        return loader.load_item()
