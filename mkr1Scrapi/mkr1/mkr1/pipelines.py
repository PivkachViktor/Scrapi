# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from mkr1.items import PlitaItem, ShopItem
class Mkr1Pipeline:
    def open_spider(self, spider):
        self.file = open('kitchen_appliances.txt', 'w', encoding='utf-8')
    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        if isinstance(item, PlitaItem):
            self.file.write(f"Plita Name: {item['name']}\n")
        elif isinstance(item, ShopItem):
            self.file.write(f"  Shop Name: {item['name']}, Price: {item['price']}\n")
        return item

