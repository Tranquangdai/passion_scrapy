import argparse

from scrapy.crawler import CrawlerProcess
from engine.beauty_spider import Passion
from models.passion_mysql import LinkPage, Category
from utils import utils

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--type', type=str, default='category',
                        help='Get different type for homepage')

    args = parser.parse_args()
    Passion.parse = getattr(Passion, 'get_' + args.type)

    if args.type == 'category':
        Passion.start_urls = ['https://passion.cuongdc.co/']

    elif args.type == 'link_page':
        Passion.start_urls = utils.list_link_in_model(Category)

    elif args.type == 'link_product':
        Passion.start_urls = utils.list_link_in_model(LinkPage)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(Passion)
    process.start()
