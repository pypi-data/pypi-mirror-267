from typing import Union
import random

class Proxy:
    proxy_hosts = [
    {
        "hostname": "syd.socks.ipvanish.com",
        "city": "Sydney",
        "countryCode": "AU",
        "country": "Australia"
    },
    {
        "hostname": "tor.socks.ipvanish.com",
        "city": "Toronto",
        "countryCode": "CA",
        "country": "Canada"
    },
    {
        "hostname": "par.socks.ipvanish.com",
        "city": "Paris",
        "countryCode": "FR",
        "country": "France"
    },
    {
        "hostname": "fra.socks.ipvanish.com",
        "city": "Frankfurt",
        "countryCode": "DE",
        "country": "Germany"
    },
    {
        "hostname": "lin.socks.ipvanish.com",
        "city": "Milan",
        "countryCode": "IT",
        "country": "Italy"
    },
    {
        "hostname": "nrt.socks.ipvanish.com",
        "city": "Tokyo",
        "countryCode": "JP",
        "country": "Japan"
    },
    {
        "hostname": "ams.socks.ipvanish.com",
        "city": "Amsterdam",
        "countryCode": "NL",
        "country": "Netherlands"
    },
    {
        "hostname": "waw.socks.ipvanish.com",
        "city": "Warsaw",
        "countryCode": "PL",
        "country": "Poland"
    },
    {
        "hostname": "lis.socks.ipvanish.com",
        "city": "Lisbon",
        "countryCode": "PT",
        "country": "Portugal"
    },
    {
        "hostname": "sin.socks.ipvanish.com",
        "city": "Singapore",
        "countryCode": "SG",
        "country": "Singapore"
    },
    {
        "hostname": "mad.socks.ipvanish.com",
        "city": "Madrid",
        "countryCode": "ES",
        "country": "Spain"
    },
    {
        "hostname": "sto.socks.ipvanish.com",
        "city": "Stockholm",
        "countryCode": "SE",
        "country": "Sweden"
    },
    {
        "hostname": "lon.socks.ipvanish.com",
        "city": "London",
        "countryCode": "UK",
        "country": "United Kingdom"
    },
    {
        "hostname": "atl.socks.ipvanish.com",
        "city": "Atlanta",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "chi.socks.ipvanish.com",
        "city": "Chicago",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "dal.socks.ipvanish.com",
        "city": "Dallas",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "den.socks.ipvanish.com",
        "city": "Denver",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "iad.socks.ipvanish.com",
        "city": "Ashburn",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "lax.socks.ipvanish.com",
        "city": "Los Angeles",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "mia.socks.ipvanish.com",
        "city": "Miami",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "nyc.socks.ipvanish.com",
        "city": "New York",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "phx.socks.ipvanish.com",
        "city": "Phoenix",
        "countryCode": "US",
        "country": "United States"
    },
    {
        "hostname": "sea.socks.ipvanish.com",
        "city": "Seattle",
        "countryCode": "US",
        "country": "United States"
    }
    ]
    port = 1080
    _type = 'SOCKS5'

    @staticmethod
    def get_proxy(username: str, password: str, cc: Union[str, None] = None, city: Union[str, None] = None) -> dict:
        """Get ipvanish proxy by specifying the username and password 
        either by specifying the countrycode or selected randomly

        Args:
            username (str): username of ipvanish prox
            password (str): password of ipvanish proxy
            cc (Union[str, None], optional): Country code if available. Defaults to None.
            city (Union[str, None], optional): City name if available. Defaults to None.

        Returns:
            dict: it returns proxy dictionary. if cc is available or it returns random proxy from list
        """
        host = None
        if cc:
            cc = cc.upper()
            host = filter(lambda i: i['countryCode'] == cc, Proxy.proxy_hosts)
            if host:
                host = list(host)
                if city:
                    host_city = filter(lambda i: i['city'].upper() == city.upper(), host)
                    if host_city:
                        host = list(host_city)[0]['hostname']
                    else:
                        host = random.choice(host)['hostname']
                    
                else:
                    host = random.choice(host)['hostname']
        if not cc:
            host = random.choice(Proxy.proxy_hosts)['hostname']
        proxy = dict(http=f'socks5://{username}:{password}@{host}:1080',
               https=f'socks5://{username}:{password}@{host}:1080')
        
        return proxy
