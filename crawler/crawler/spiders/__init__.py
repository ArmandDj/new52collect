# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import json

from crawler.items import ComicItem, CharacterItem
from scrapy.http import Request

class Spider(scrapy.Spider):
	name = "spider"
	start_urls = [
		"http://www.comicbookdb.com/imprint.php?ID=1040"
	]

	download_delay = 0.25

	# parse start page, follow links to series pages
	def parse(self, response):
		self.crawler.stats.set_value('pages_crawled', 0)
		links = response.xpath('//table[@width="100%"]/tr/td/a[contains(@href, "title.php")]/@href').extract()

		for link in links:
			url = 'http://www.comicbookdb.com/' + link
			yield Request(url, callback=self.parseSeries)

	# parse series page, follow links to individual issue pages
	def parseSeries(self, response):
		links = list(set(response.xpath('//table/tr/td/a[contains(@href, "issue.php")]/@href').extract()))
		for link in links:
			url = 'http://www.comicbookdb.com/' + link
			yield Request(url, callback=self.parseIssue)

	# parse issue page, store all relevant data and yield to be saved in json file
	def parseIssue(self, response):
		# only collect data for numbered issues (exclude TPBs)
		if response.xpath('//span[@class = "page_headline"]/text()').extract()[0].replace(" - ","").replace("#", "").isdigit():
			comic = ComicItem()
			comic['series'] = response.xpath('//span[@class = "page_headline"]/a/text()').extract()[0]
			comic['issue_num'] = int(response.xpath('//span[@class = "page_headline"]/text()').extract()[0].replace(" - #",""))
			title = response.xpath('//span[@class = "page_subheadline test"]/text()').extract()
			if len(title) > 0:
				comic['title'] = title[0]
			else:
				comic['title'] = ''
			comic['writer'] = response.xpath('//a[@class="test"][contains(@href, "creator.php")]/text()').extract()[0]
			comic['penciller'] = response.xpath('//a[@class="test"][contains(@href, "creator.php")]/text()').extract()[1]
			comic['cover'] = response.xpath('//img[contains(@src, "comic_graphics")]/@src').extract()[0]
			comic['characters'] = response.xpath('//tr/td[@width="49%"]/a[contains(@href, "character.php")]/text()').extract()
			comic['cover_price'] = float([i for i in response.xpath('//text()').extract() if "US $ " in i][0].replace("US $ ", ""))

			# with open(str(self.crawler.stats.get_value('pages_crawled')) + '.txt', 'wb') as f:
			# 	f.write(json.dumps(comic))

			yield comic

			self.crawler.stats.inc_value('pages_crawled')