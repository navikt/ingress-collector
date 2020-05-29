import urllib3
from urllib import request
import sys
import os
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


http = urllib3.PoolManager()


def remove_no_proxy_domain(domain):
    no_proxy = os.environ.get('NO_PROXY', '')
    list_of_domains = no_proxy.split(",")
    if domain in list_of_domains:
        list_of_domains.remove(domain)
        domains = ",".join(list_of_domains)
        os.environ['NO_PROXY'] = domains
        os.environ['no_proxy'] = domains


def check(url):
    try:
        r = http.request('GET', url)
        print("urllib3 fungerte " + url)
        print("\t" + str(r.data))
    except:
        print("urllib3 feilet " + url)
        print("\t" + str(sys.exc_info()))
    try:
        req = request.Request(url)
        data = json.loads(request.urlopen(req).read().decode('utf-8'))
        print("urllib fungerte " + url)
        print("\t" + str(data))
    except:
        print("urllib feilet " + url)
        print("\t" + str(sys.exc_info()))


remove_no_proxy_domain(".nav.no")
remove_no_proxy_domain(".nais.io")
check("https://amplitude.nav.no/health/is-alive")
check("https://amplitude.labs.nais.io/health/is-alive")
check("https://docker.pkg.github.com/")
