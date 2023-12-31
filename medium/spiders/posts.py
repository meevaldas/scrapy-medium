import scrapy
from selenium import webdriver
import time
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from medium.items import MediumItem


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = ["medium.com"]
    start_urls = ["https://www.medium.com/"]

    def parse(self, r):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(self.start_urls[0])
        driver.implicitly_wait(5)
        i = 1
        num_scrolls = 10
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True and i <= num_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            response = driver.page_source
            selector = Selector(text=response)
            containers = selector.xpath("//section//div[@class='al dc']")
            for c in containers:
                item = ItemLoader(item=MediumItem(), response=response, selector=c)
                item.add_xpath("title", ".//h2/text()")
                item.add_xpath("excerpt", ".//h3/text()")
                item.add_xpath("link", ".//a[h2]/@href")
                yield item.load_item()
            i = i + 1
        driver.quit()
