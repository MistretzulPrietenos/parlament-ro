# -*- coding: utf-8 -*-

from prlmro.items import SenatorItem, SenatorLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader.processors import TakeFirst, MapCompose, Join




class RomanianParlimentSpider(CrawlSpider):
	name = "prlmro_spider"
	allowed_domains = ["cdep.ro"]
	start_urls = (
	   'http://www.cdep.ro/pls/parlam/structura.de?leg=2012',
    )
    
	rules = (
		Rule(
			LinkExtractor(
				allow=('structura\.mp\?(.*)idm=(170|165|410|411|156|412)(.*)', )
			), callback='parse_item'),
	)
	
	def parse_cv_page(self, response):
		#xpath = Selector(response)
		item = response.meta['item']
		
		loader = SenatorLoader(item=item, response=response)
		
		#print xpath.xpath(u'//*[text()="Studii şi specializări"]/following-sibling::ul')
		loader.add_xpath('studii', u'//*[text()="Studii şi specializări"]/following-sibling::ul', TakeFirst())
		
		yield loader.load_item()
	
	def parse_item(self, response):
		#xpath = Selector(response)
		loader = SenatorLoader(item=SenatorItem(), response=response)
		
		loader.add_value('url', response.url)
		loader.add_xpath('nume', '//td[@class="headline"]/text()', TakeFirst(), re='(.+?)\s*,|(.*)')
		loader.add_xpath('data_nastere', '//td[@class="menuoff"]/text()')
		loader.add_xpath('rol','//table[1]/tr[1]/td[1]/b/text()')
		loader.add_xpath('circ_nr', '//table[1]/tr[2]/td[2]/text()', re=u'electorală nr\.(.*)')
		loader.add_xpath('circ', '//table[1]/tr[2]/td[2]/a[starts-with(@href,"structura")]/text()', TakeFirst())
		loader.add_xpath('circ_colegiu', '//table[1]/tr[2]/td[2]/text()', re='uninominal nr\.(.*)')
		loader.add_xpath('data_stop_mdt', '//table[1]/tr[2]/td[2]/text()', re=u'data încetarii mandatului:\s*(.*\d)')
		loader.add_xpath('motiv_stop_mdt', '//table[1]/tr[2]/td[2]/text()', re=u'data încetarii mandatului:\s*\d+.*\d\d\d\d\s*\-*\s*(.*)\s*\-*\s*')
		
		loader.add_xpath('fmt_politica', u'//*[text()="Formaţiunea politică:"]/parent::td/parent::tr/following-sibling::tr/td/table/tr/td/table/tr')		
		loader.add_xpath('grp_parlamentar', u'//*[text()="Grupul parlamentar:"]/parent::td/parent::tr/following-sibling::tr/td/table/tr')
		loader.add_xpath('comisii_permanente', u'//*[text()="Comisii permanente"]/parent::td/parent::tr/following-sibling::tr/td/a')
		loader.add_xpath('comisii_speciale', u'//*[text()="Comisii speciale comune"]/parent::td/parent::tr/following-sibling::tr/td/a')
		loader.add_xpath('activitate_politica', u'//*[text()="Activitatea parlamentara în cifre:"]/parent::td/parent::tr/following-sibling::tr/td/table/tr')
		
		itm =  loader.load_item()
		cv_url = response.url + '&pag=0&idl=1'
		yield Request(cv_url, meta={'item': itm}, callback=self.parse_cv_page)
		
		

