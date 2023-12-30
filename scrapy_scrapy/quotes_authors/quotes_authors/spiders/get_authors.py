import scrapy


class GetAuthorsSpider(scrapy.Spider):
    name = "get_authors"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "authors.json",
        "FEED_EXPORT_INDENT": 2,
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response): # noqa
        authors = response.xpath('//div[@class="quote"]/span[2]/a/@href').extract()
        for author in authors:
            yield scrapy.Request(url=response.urljoin(author), callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        fullname = response.css('div.author-details h3::text').get()
        born_date = response.css('p span.author-born-date::text').get()
        born_location = response.css('p span.author-born-location::text').get()
        description = response.css('div.author-description::text').get().strip()

        yield {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
        }
