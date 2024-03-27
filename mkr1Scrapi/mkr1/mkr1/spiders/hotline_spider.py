import scrapy
from mkr1.items import PlitaItem, ShopItem

class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.ua"]
    start_urls = ["https://hotline.ua/ua/bt/kuhonnye-plity-i-poverhnosti"]

    def parse(self, response):
        plita_as = response.css('div.list-item a.item-title')
        for plita_a in plita_as:
            plita_name = plita_a.css('::text').get()
            plita_link = plita_a.css('::attr(href)').get()
            plita_link = f"https://hotline.ua{plita_link}"
            yield PlitaItem(
                name = plita_name,
                url = plita_link,
            )
            yield scrapy.Request(
                url = plita_link,
                callback= self.shops_parse,
                meta={
                    "plita_name": plita_name
                }
            )

    def shops_parse(self,response):
        shop_items = response.css('div.list__item')
        if len(shop_items) > 10:
            for shop_item in shop_items:
                shop_name = shop_item.css('a.shop__title::text').get()
                shop_price = shop_item.css('span.price__value::text').get()
                yield ShopItem(
                    name = shop_name,
                    price = shop_price,
                    plita = response.meta.get('plita_name')
                )
