import scrapy
from scrapy.crawler import CrawlerProcess

from medium.spiders.posts import PostsSpider


def main():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "post.json": {"format": "json"},
            },
        }
    )

    process.crawl(PostsSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
