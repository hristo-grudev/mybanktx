import scrapy

from scrapy.loader import ItemLoader

from ..items import MybanktxItem
from itemloaders.processors import TakeFirst


class MybanktxSpider(scrapy.Spider):
	name = 'mybanktx'
	start_urls = ['https://www.mybanktx.com/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@class="button"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h1 | ancestor::span[@class="date"] | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=MybanktxItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
