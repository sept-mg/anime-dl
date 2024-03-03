import warnings, requests
from exception import NoProxyException, blocked, noProxy
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

def tokyotoshoFinder(proxies, name, headers, stringNbEp):
    url = f"https://www.tokyotosho.info/rss.php?terms={name}" 
    if stringNbEp != "" :
        url = url + "+" + stringNbEp + "+1080p+sub"
    
    try:
        if noProxy[0]:
            response = requests.get(url, headers=headers, timeout=1)
        else:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
    except:
        blocked.append(proxies)
        raise NoProxyException
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
    magnet = BeautifulSoup(response.content, "lxml").find_all('a')

    found = not (magnet == None)
    if found:
        try:
            magnet = magnet[1]
        except IndexError:
            found = False
    return (found, magnet)