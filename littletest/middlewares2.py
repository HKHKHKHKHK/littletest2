import json
import logging
from scrapy import signals
import requests
import time
from twisted.internet import defer
from twisted.internet.defer import DeferredLock
import requests
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


class ProxyMiddleware():
    def __init__(self, proxy_url, uri):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.EXCEPTIONS_TO_RETRY = (
            defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError,
            ConnectionLost, TCPTimedOutError, ResponseFailed, IOError, TunnelError)


    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri

    def process_exception(self, request,  spider, exception):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            print('=============================Got exception: %s' % (exception))
            try:
                response = requests.get('http://132.232.182.231:5000/random')
                if response.status_code == 200:
                    proxy = response.text
                    if proxy:
                        uri = 'https://{proxy}'.format(proxy=proxy)
                        self.logger.debug('使用备用代理 ' + proxy)
                        request.meta['proxy'] = uri
            except requests.ConnectionError:
                return False

            return request


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')

        )
