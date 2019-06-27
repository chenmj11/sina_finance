# -*- coding: utf-8 -*-
import scrapy
from Finance.items import FinanceItem

class FinanceSpider(scrapy.Spider):
    name = 'finance'
    allowed_domains = ['finance.sina.com.cn', 'vip.stock.finance.sina.com.cn','file.finance.sina.com.cn','file.finance.sina.com.cn/211.154.219.97:9494']
    start_urls = ['https://finance.sina.com.cn/realstock/company/sh600271/nc.shtml']


    def parse(self, response):
        item = FinanceItem()
        # 获取年报、半年报、一季报、三季报的url
        node_list = response.xpath("//*[@id='louver']/div[7]/div[2]/ul/li")

        for node in node_list:
           item['url'] = node.xpath("./a/@href").extract_first()
           yield scrapy.Request(url=item['url'], meta={"position_item": item}, callback=self.parse_position)
           # yield item


    def parse_position(self,response):
        """
        获取每篇文章url
        """
        item = response.meta["position_item"]
        base_url = "http://vip.stock.finance.sina.com.cn"
        report_url_list = response.xpath("//div[@class='datelist']/ul/a")
        # print(report_url_list)
        for report_url in report_url_list:
            item['report_url'] = base_url + report_url.xpath("./@href").extract_first()
            # print(item['report_url'],item["title"])
            yield scrapy.Request(url=item['report_url'], meta={"pdf_item": item}, callback=self.parse_pdf)
            # yield item


    def parse_pdf(self, response):
        """
        获取pdf的url 
        """
        item = response.meta["pdf_item"]
        item["title"] = response.xpath("//*[@id='allbulletin']/thead/tr/th/text()").extract_first()[:-4]
        item["pdf_url"] = response.xpath("//*[@id='allbulletin']/thead/tr/th/font/a/@href").extract_first()
        # print(item["pdf_url"])
        yield item