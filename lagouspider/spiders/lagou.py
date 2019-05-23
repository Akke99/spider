# -*- coding: utf-8 -*-
import scrapy
from lagouspider.items import LagouspiderItem
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com/']
    start_urls = ['https://www.lagou.com/jobs/list_Python?px=default&gj=3年及以下&city=上海#filterBox']

    def parse(self, response):
        job_list = response.xpath("//div[@id='s_position_list']/ul[@class='item_con_list']/li")
        print(len(job_list))
        for row in job_list:
            jobname = row.xpath("div/div[@class='position']/div[@class='p_top']/a/h3/text()").extract()[0]
            jobsalary = row.xpath("div/div[@class='position']/div[@class='p_bot']/div/span/text()").extract()[0]
            jobcompany = row.xpath("div/div[@class='company']/div[@class='company_name']/a/text()").extract()[0]
            jobdetail = row.xpath("div[@class='list_item_top']/div[@class='position']/div[@class='p_bot']/div/text()").extract()[0]
            jobtreatment = row.xpath("div[@class='list_item_bot']/div[@class='li_b_r']/text()").extract()[0]
            item = LagouspiderItem()
            print(jobname,jobsalary,jobcompany)
            item["jobname"] = jobname
            item["jobsalary"] = jobsalary
            item["jobcompany"] = jobcompany
            item["jobdetail"] = jobdetail
            item["jobtreatment"] = jobtreatment

            yield item
        yield scrapy.Request(response.url, )

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('lagou')
    process.start()