import scrapy

class QuoteSpiderSpider(scrapy.Spider):
    name = "quote_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            author_page = quote.css("span a::attr(href)").get()
            author_url = response.urljoin(author_page)

            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
                "author_url": author_url,
            }

            yield response.follow(author_page, self.parse_author)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_name = response.css("h3.author-title::text").get().strip()
        author_birthdate = response.css("span.author-born-date::text").get()
        author_born_location = response.css("span.author-born-location::text").get().strip()
        author_description = response.css("div.author-description::text").get().strip()

        yield {
            "author": author_name,
            "birthdate": author_birthdate,
            "born_location": author_born_location,
            "description": author_description,
        }
