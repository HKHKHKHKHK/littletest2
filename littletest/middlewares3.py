from scrapy import signals
import random
import logging
import scrapy
from scrapy import log
import time
from twisted.internet import defer
from twisted.internet.defer import DeferredLock
import requests
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class ProxyMiddleWare(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = 'http://54.255.234.23:8000/random'
        self.download_timeout = 30
        self.lock = DeferredLock()
        self.RETRY_HTTP_CODES = [302,301,500, 503, 504, 400, 408,403]
        self.EXCEPTIONS_TO_RETRY = (
        defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError,
        ConnectionLost, TCPTimedOutError, ResponseFailed, IOError, TunnelError)

    def process_request(self, request, spider):
        if not 'proxy' in request.meta:
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理1 ' + uri)
            request.meta['proxy'] = uri

    def process_response(self, request, response, spider):
        if response.status in self.RETRY_HTTP_CODES  or 'captcha' in response.url:
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理2 ' + uri)
                request.meta['proxy'] = uri
                return request
        return response


    def process_exception(self, request,  spider, exception):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理2 ' + uri)
                request.meta['proxy'] = uri
            return request

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False



class UserAgentMiddleWare(object):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    ]

    def process_request(self, request, spider):
        UserAgent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = UserAgent
