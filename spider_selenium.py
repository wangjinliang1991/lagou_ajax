import re
import time

from selenium import webdriver
from lxml import etree


class LagouSpider(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'
        self.positions = []

    def run(self):
        self.driver.get(self.url)
        source = self.driver.page_source
        self.parse_list_page(source)

    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self,url):
        self.driver.get(url)
        source = self.driver.page_source

    def parse_detail_page(self,source):
        html = etree.HTML(source)
        position_name = html.xpath('//span[@class="name"]/text()')[0]
        job_request_spans = html.xpath('//dd[@class="job_request"]//span')
        salary = job_request_spans[0].xpath('.//text()')[0].strip()
        city = job_request_spans[1].xpath('.//text()')[0].strip()
        city = re.sub(r"[\s/]", "", city)
        work_years = job_request_spans[2].xpath('.//text()')[0].strip()
        work_years = re.sub(r"[\s/]", "", work_years)
        education = job_request_spans[3].xpath('.//text()')[0].strip()
        education = re.sub(r"[\s/]", "", education)
        desc = "".join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
        position = {
            'name': position_name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'desc': desc
        }
        self.positions.append(position)


if __name__ == '__main__':
    spider =LagouSpider()
    spider.run()