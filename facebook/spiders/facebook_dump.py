import scrapy
import base64
from scrapy_splash import SplashRequest

class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['facebook.com']
    start_urls = ['https://www.facebook.com/']
    url = 'https://www.facebook.com/'
    render_script = '''
        function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:wait(10))

        splash:set_viewport_full()

        local search_input = splash:select('input[name=email]')   
        search_input:send_text("email")
        local search_input = splash:select('input[name=pass]')
        search_input:send_text("password")
        assert(splash:wait(5))
        local submit_button = splash:select('input[name=login]')
        submit_button:click()

        assert(splash:wait(10))

        return {
            html = splash:html(),
            png = splash:png(),
        }
      end
    '''

    def start_requests(self):
        yield SplashRequest(
            self.url,
            self.parse,
            endpoint='execute',
            args={
                'wait': 5,
                'lua_source': self.render_script,
            },
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        )

    def parse(self, response):
        yield response
