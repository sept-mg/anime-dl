import requests
from exception import NoProxyException, blocked, noProxy
from bs4 import BeautifulSoup

def scraping(name, proxies, headers):
    url_mal = f"https://myanimelist.net/anime.php?cat=anime&q={name}"
    
    try:
        if noProxy[0]:
            reponse_mal = requests.get(url_mal , headers=headers)
        else:
            reponse_mal = requests.get(url_mal , proxies=proxies, headers=headers)
    except:
        blocked.append(proxies)
        raise NoProxyException
    
    soup_finding = BeautifulSoup(reponse_mal.content, 'html.parser')
    soup_finding = soup_finding.find_all('table')[1]

    pageMal = soup_finding.find_all('tr')[1].find('a').get('href')

    try:
        if noProxy[0]:
            reponse_page_mal = requests.get(pageMal, headers=headers)
        else:
            reponse_page_mal = requests.get(pageMal, proxies=proxies, headers=headers)
    except:
        blocked.append(proxies)
        raise NoProxyException

    soup_title = BeautifulSoup(reponse_page_mal.content, 'html.parser').find('div', {'itemprop': 'name'})
    (name, fullname, japanName) = getName(soup_title)

    print("\n" + fullname + "\n")
    
    try:
        if noProxy[0]:
            reponse_page_mal_pics = requests.get(pageMal + "/pics", headers=headers)
        else:
            reponse_page_mal_pics = requests.get(pageMal + "/pics", proxies=proxies, headers=headers)
    except:
        blocked.append(proxies)
        raise NoProxyException
    
    images_link = []
    soup_images = BeautifulSoup(reponse_page_mal_pics.content, 'html.parser').find_all('table')[2]
    for i in soup_images.find_all('a'):
        test = i.get('href')
        if not test.startswith('/'):
            images_link.append(test)
    
    return (name, fullname, japanName, pageMal, images_link)

def getName(name_section):
    japanName = name_section.find('h1').get_text()
    fullname = name_section.find('p', class_="title-english")
    if(fullname == None):
        fullname = "" + japanName
    else:
        fullname = fullname.get_text()
    fullname = str(fullname)
    
    result = ''
    for i in range(len(fullname)):
        if fullname[i].isalpha() or fullname[i] == ' ' or fullname[i].isnumeric() or fullname[i] == "'":
            if fullname[i] == "'":
                result+=" "
            else:
                result += fullname[i]
    return (result, fullname, japanName)