import requests
from bs4 import BeautifulSoup


class Session(requests.Session):

    def __init__(self):
        super().__init__()
        self.https_proxies = self.__class__.get_proxies(proxy_type='https')
        self.http_proxies = self.__class__.get_proxies(proxy_type='http')
        self.sample_header= { #TODO: Add a header randomiser
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/68.0.3440.106 Safari/537.36'
        }
        self.proxies = self.get_new_proxies()

    @staticmethod
    def get_proxies(
            proxy_type='https',
            https_file='https_proxies.txt',
            http_file='http_proxies.txt'):
        r"""Get a proxy from a file depending on the type

        :param proxy_type: The type of proxy (http, https)
        :param https_file: The file path of the https proxy file
        :param http_file:  The file path of the http proxy file
        :rtype: generator containing the proxy
        """
        if proxy_type=='https':
            with open(https_file, 'r') as f:
                for proxy in f:
                    ip, port = proxy.strip().split('\t')
                    yield f'{ip}:{port}'
        if proxy_type=='http':
            with open(http_file, 'r') as f:
                for proxy in f:
                    ip, port = proxy.strip().split('\t')
                    yield f'{ip}:{port}'
        else:
            raise Exception('Incorect Type.')

    def get_new_proxies(self):
        r"""Creates a new proxy dictionary from the
        generators

        :rtype dict containing https and http proxy
        """
        prox = {
            'https': next(self.https_proxies),
            'http': next(self.http_proxies)
        }
        self.proxies = prox

    def get(self, url,**kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        headers = kwargs.pop('headers', None) or self.sample_header
        proxies = kwargs.pop('proxies', None) or self.proxies

        return super().get(
            url=url,
            headers=headers,
            proxies=proxies,
            **kwargs
        )


def test():
    """ Checks if the proxies are working by going to a website
    and checking what ip i have.
    """
    def get_ipv4(soup):
        elem = soup.find('div', {'id': 'ipv4'})
        return elem.text.strip()

    def get_ipv6(soup):
        elem = soup.find('div', {'id': 'ipv6'})
        return elem.text.strip()

    url = 'https://whatismyipaddress.com/'
    with Session() as s:
        resp = s.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        ipv4 = get_ipv4(soup)
        ipv6 = get_ipv6(soup)

        print('\nTesting Proxies:')
        print(s.proxies)
        print(f'ipv4: {ipv4}')
        print(f'ipv6: {ipv6}')

if __name__ == "__main__":
    test()





