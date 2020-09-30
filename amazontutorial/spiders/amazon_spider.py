import scrapy
from ..items import AmazontutorialItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?k=web+scraping+with+python&i=stripbooks&crid=1QOXPKOK9P1QS&sprefix=webscraping+%2Caps%2C232&ref=nb_sb_ss_sc_2_12'
    ]

    def parse(self, response):
        # create items to store data we scrape
        items = AmazontutorialItem()

        product_name = response.css('.a-text-normal.a-color-base').css('::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
        product_price = response.css('.a-size-base.a-text-normal .a-price-fraction , .a-size-base.a-text-normal .a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

    # clean up author and price list
        product_author = [name.strip() for name in product_author]
        product_price = [price for price in product_price if price != '.']
        new_list = []
        for i in range(0, len(product_price)-2, 2):
            new_price = product_price[i]+'.'+product_price[i+1]
            new_price = float(new_price)
            new_list.append(new_price)
        product_price = new_list

        #print("product name: ", product_name)
        # print("product author: ", product_author)
        # print("product price: ", product_price)
        # print("product imagelink: ", product_imagelink)

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items

        # FOLLOW - if you want to follow all links
        next_page = response.css('li.a-last a::attr(href)').get()

        if next_page :
            yield response.follow(next_page, callback=self.parse)

        # FOLLOW - use pagination
        # next_page = f'https://www.amazon.com/s?k=webscraping&i=stripbooks&page={AmazonSpider.page_number}'
        # if AmazonSpider.page_number <= 2:
        #     AmazonSpider.page_number +=1
        #     yield response.follow(next_page, callback=self.parse)