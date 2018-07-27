# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Lagou.items import LagouItem
from Lagou.common import get_md5
import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        #Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        #Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': ' ',#请输入cookie
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }



    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_job(self, response):
        item = LagouItem()
        item['title']=response.xpath('//div[@class="job-name"]/@title').extract_first()
        item['url'] = response.url
        item['url_object_id'] = get_md5(response.url)
        item['publish_time']=response.xpath("//*[@class='publish_time']/text()").extract_first()
        item['salary'] =response.xpath('//dd[@class="job_request"]/p/span[@class="salary"]/text()').extract_first()
        item['job_city'] = response.xpath("//*[@class='job_request']/p/span[2]/text()").extract_first()[1:-1]
        item['work_years']= response.xpath("//*[@class='job_request']/p/span[3]/text()").extract_first()[:-1]
        item['degree_need'] = response.xpath("//*[@class='job_request']/p/span[4]/text()").extract_first()[:-1]
        item['job_type']= response.xpath("//*[@class='job_request']/p/span[5]/text()").extract_first()
        item['job_advantage']= response.xpath("//dd[@class='job-advantage']/p/text()").extract_first()
        job_desc= response.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        item['job_desc'] = "".join(job_desc)
        job_addr =response.xpath('//div[@class="work_addr"]/a/text()').extract()[:-1]
        item['job_addr']="-".join(job_addr)
        item['company_name'] = response.xpath('//dl[@class="job_company"]/dt/a/img/@alt').extract_first()
        item['company_url'] = response.xpath("//dl[@class='job_company']//a[@rel='nofollow']/@href").extract_first()
        tags= response.xpath('//*[@class="job_request"]/ul/li/text()').extract()
        item['tags'] ="/".join(tags)
        item['crawl_time']=datetime.datetime.now()
        yield item

