from urllib import request
import sys
from collector import remove_no_proxy_domain
import json


def check(url):
    try:
        req = request.Request(url)
        data = json.loads(request.urlopen(req).read().decode('utf-8'))
        print("urllib fungerte " + url)
        print("\t" + str(data))
    except:
        print("urllib feilet " + url)
        print("\t" + str(sys.exc_info()))


remove_no_proxy_domain(".nav.no", "NO_PROXY")
remove_no_proxy_domain(".nais.io", "NO_PROXY")
remove_no_proxy_domain(".nav.no", "no_proxy")
remove_no_proxy_domain(".nais.io", "no_proxy")
check("https://amplitude.nav.no/health/is-alive")
check("https://amplitude.labs.nais.io/health/is-alive")
check("https://docker.pkg.github.com/")
