import scrapy
from scrapy.selector import Selector 
from scrapy_selenium import SeleniumRequest
from shutil import which
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'
    
    def start_requests(self):
        yield SeleniumRequest(url='https://duckduckgo.com', wait_time = 3, screenshot=True, callback=self.parse)

    def parse(self, response):
        # img = response.meta['screenshot']

    #     with open('screenshot.png', "wb") as f:
            # f.write(img)

        driver = response.meta['driver']
        search_input = driver.find_element_by_id('search_form_input_homepage')
        search_input.send_keys('hello world')
        
    
        # driver.save_screenshot('After search.png')
        search_input.send_keys(Keys.ENTER)
        
        '''
        the reason why we do html here is because this page is different to initial page respone we first got in start_request, we need to find elements and xpath on the new webpage
        html which the results of our search "hello world" therefore we make the variable html which holds the driver.page_source 
        '''

        html = driver.page_source
        response_obj = Selector(text=html)
        # driver.save_screenshot('results.png')
        # links = response_obj.xpath('//a[@class="result__a"]') my way
        # '//div[@class="result__extras__url"]'
        # 'URL': link.xpath('.//@href').get() my way
        links = response_obj.xpath('//a[@class="result__a"]')
        for link in links:
            yield{
                'URL': link.xpath('.//@href').get()
            }