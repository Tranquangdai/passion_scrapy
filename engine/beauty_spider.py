import scrapy
from models.passion_mysql import LinkProduct, Category, LinkPage
from utils import utils


class Passion(scrapy.Spider):

    allowed_domain = ['https://passion.cuongdc.co/']
    name = 'passion'
    start_urls = None

    def list_inserted_url_hash(self, model):
        inserted_url_hash = [i.url_hash for i in model.select(model.url_hash).execute()]
        return inserted_url_hash

    def get_link_product(self, response):
        inserted_url_hash = self.list_inserted_url_hash(LinkProduct)

        titles = response.xpath("//article[@class='post']//a/@title").extract()
        link_and_image = utils.split_list_by_product(response.xpath("//article[@class='post']//a/@href").extract())
        for i in range(len(titles)):
            title = utils.preprocessing_text(titles[i])
            link = link_and_image[i][0]
            name = link.split('/')[-1].split('.')[0]
            category = utils.parse_category_from_product_link(response.url)
            image = [response.urljoin(img) for img in link_and_image[i][1:]]
            row = {'title': title, 'link': link, 'image': image, 'name': name, 'category': category}
            row = self.add_more_info(row)
            if not row['url_hash'] in inserted_url_hash:
                LinkProduct.insert(row).execute()

    def add_more_info(self, row):
        if isinstance(row, dict):
            row['updated_at'] = utils.get_current_datetime()
            if 'link' in row:
                row['url_hash'] = utils.hash_url(row['link'])
            return row

    def get_category(self, response):
        category = response.xpath("//ul[@id='menu-topbar-menu']/li/a/text()").extract()
        link = response.xpath("//ul[@id='menu-topbar-menu']/li/a/@href").extract()
        for k, v in zip(category, link):
            if k == 'Home' or k == '♥ Việt Nam' or k == 'XKCN':
                continue
            else:
                row = {'category': k, 'link': v}
                row = self.add_more_info(row)
                Category.insert(row).execute()

    def get_link_page(self, response):
        inserted_url_hash = self.list_inserted_url_hash(LinkPage)
        row_ = self.add_more_info({'link': response.url})
        if not row_['url_hash'] in inserted_url_hash:
            LinkPage.insert(self.add_more_info(row_)).execute()

        next_page = response.xpath("//a[@class='blog-pager-older-link']/@href").extract_first()
        row = self.add_more_info({'link': next_page})
        if not row['url_hash'] in inserted_url_hash:
            LinkPage.insert(self.add_more_info({'link': next_page})).execute()
        yield scrapy.Request(next_page, callback=self.parse)
