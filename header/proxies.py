import requests, pandas as pd
from exception import blocked, moreDebug

def proxies(headers, torrentFinding = False):
    # url = "https://httpbin.org/ip"
    url2 = "https://myanimelist.net/" if not torrentFinding else "https://nyaa.si/"
    # proxiesList = None
    good_proxies = set()
    print("search a proxy...")
    response = requests.get("https://free-proxy-list.net/")
    proxy_list = pd.read_html(response.text)[0]
    proxy_list["url"] = "http://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)

    https_proxies = proxy_list[(proxy_list["Https"] == "yes")]
    for proxy_url in https_proxies["url"]:
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        try:
            print(f"Proxy {proxy_url} TEST")
            if(proxies in blocked):
                print(f"Proxy {proxy_url} NOT VALID")
                raise Exception(f"Proxy {proxy_url} NOT VALID")
            # response = requests.get(url, headers=headers,proxies=proxies, timeout=1)
            response =  requests.get(url2, headers=headers,proxies=proxies, timeout=1)
            good_proxies.add(proxy_url)
            print(f"Proxy {proxy_url} OK, a good proxy found")
        except Exception as error:
            if moreDebug[0]:
                print(error)
            pass
        
        if len(good_proxies) >= 1:
            break
            
    return proxies