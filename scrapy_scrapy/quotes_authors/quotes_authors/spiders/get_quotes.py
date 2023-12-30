import scrapy


class GetQuotesSpider(scrapy.Spider):
    name = "get_quotes"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "quotes.json",
        "FEED_EXPORT_INDENT": 2,
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):  # noqa
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
