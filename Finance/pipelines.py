# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import re

# class FinancePipeline(object):
#     def process_item(self, item, spider):
#         return item

class FinancePipeline(FilesPipeline):
    """
    下载文件
    """
    def get_media_requests(self, item,info):
        pdf_url = item["pdf_url"]

        if not pdf_url  is None:

            yield scrapy.Request(pdf_url,meta={"item":item})

    def file_path(self,request,response=None,info=None):
        """文件重命名"""
        item = request.meta['item']
        # 文件名称。
        image_guid = item['title'] +".pdf"
        return image_guid

