import scrapy
import requests

from hashlib import md5

from scrapy.loader import ItemLoader

from github import settings
from github.items import GithubItem


class FetchProjectSpider(scrapy.Spider):
    name    = 'fetch-project'

    def __init__(self, *args, **kwargs):
        super(FetchProjectSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        fetch_url   = "{base_url}fetch/project/".format(base_url=settings.SERVER_URL)
        res         = requests.get(fetch_url, headers=settings.SERVER_HEADER)
        data        = res.json()['results']
        self.cache_info = dict()

        for row in data:
            key = md5(row['url']).hexdigest()
            self.cache_info.update(
                {
                    key: {
                        'url': row['url'],
                        'category': row['category']
                    }
                }
            )
            yield scrapy.Request(row['url'], self.parse)

    def parse(self, response):
        key     = md5(response.url).hexdigest()
        info    = self.cache_info.pop(key)

        item    = ItemLoader(item=GithubItem(), response=response)

        item.add_css('author', 'h1.public >span.author >a')
        item.add_css('name', 'h1.public >strong >a')
        item.add_css('desc', 'div.repository-meta-content')
        if response.css('article.markdown-body').extract_first():
            item.add_css('readme', 'article.markdown-body')
        else:
            item.add_css('readme', 'div.plain')

        item.add_value('github_url', response.url)
        item.add_value('category', info['category'])

        return item.load_item()