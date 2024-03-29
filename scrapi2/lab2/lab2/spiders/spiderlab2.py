import scrapy
import json
import csv
from scrapy.exporters import XmlItemExporter

class CusuSpider(scrapy.Spider):
    name = "spiderlab2"
    allowed_domains = ['cusu.edu.ua']
    start_urls = ['https://www.cusu.edu.ua/ua/']
    item_scraped_count = []

    def parse(self, response):
        # Отримання списку факультетів
        faculties = response.css('ul.sp-dropdown-items')[2].css('li')
        for faculty in faculties:
            faculty_name = faculty.css('a::text').get()
            faculty_url = faculty.css('a::attr(href)').get()
            yield scrapy.Request(url=response.urljoin(faculty_url), callback=self.parse_faculty, meta={'faculty_name': faculty_name})

    def parse_faculty(self, response):
        faculty_name = response.meta['faculty_name']
        # Отримання списку кафедр
        departments = response.css('a.accordeonck')
        for department in departments:
            department_name = department.css('::text').get()
            if 'Кафедра' in department_name:
                item = {
                    'faculty': faculty_name,
                    'department': department_name
                }
                self.item_scraped_count.append(item)
                yield item

    def closed(self, reason):
        # Збереження даних у JSON, XML та CSV форматах
        json_data = []
        xml_data = []
        csv_data = [['Faculty', 'Department']]

        for item in self.item_scraped_count:
            json_data.append(dict(item))
            xml_data.append(item)
            csv_data.append([item['faculty'], item['department']])

        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        with open('data.xml', 'wb') as xml_file:
            exporter = XmlItemExporter(xml_file)
            exporter.start_exporting()
            for item in xml_data:
                exporter.export_item(item)
            exporter.finish_exporting()

        with open('data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)
