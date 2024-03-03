import requests
from exception import NoProxyException, blocked, noProxy
from bs4 import BeautifulSoup
from torrentManager.utils import Utils as utils
from exception import NoProxyException

URL = "https://nyaa.si/"


def search(proxies, headers, keyword, **kwargs):
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        try :
            if page > 0:
                url = "{}?f={}&c={}_{}&q={}&p={}&s=seeders&o=desc".format(URL, filters, category, subcategory, keyword, page)
                print(url)
                if noProxy[0]:
                    r = requests.get(url, headers=headers, timeout=1)
                else:
                    r = requests.get(url, proxies=proxies, headers=headers, timeout=1)
            else:
                url = "{}?f={}&c={}_{}&q={}&s=seeders&o=desc".format(URL, filters, category, subcategory, keyword)
                print(url)
                if noProxy[0]:
                    r = requests.get(url, headers=headers, timeout=1)
                else:
                    r = requests.get(url, proxies=proxies, headers=headers, timeout=1)
        except :
            raise NoProxyException

        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        return utils.parse_nyaa(rows, limit=None)


def nyaaFinder(proxies, headers, anime_name, episode, complement = "", quality=1080, uploader = "", untrusted_option = True):
    if uploader != "":
        uploader = '[' + uploader + ']'
    if complement != "":
        complement = " " + complement

    found_torrents = search(
        proxies,
        headers,
        keyword=f"{uploader} {anime_name} - {episode} [{quality}p]{complement}",
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    ) + search(
        proxies,
        headers,
        keyword=f"{uploader} {anime_name} - {episode} ({quality}p){complement}",
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    )
    
    try:
        # We take the very closest title to what we are looking for.
        torrent = None
        for t in found_torrents:  # (break if found, so we get the most recent one)
            if (
                t["name"].lower().find(f"{anime_name} - {episode}".lower()) != -1
                and t["name"].lower().find("~") == -1
            ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
                torrent = t
                break

        # Else, we take try to get a close title to the one we are looking for.
        if torrent is None:
            for t in found_torrents:
                if (
                    t["name"].lower().find(f"{anime_name}".lower()) != -1
                    and t["name"].lower().find(f" {episode} ") != -1
                    and t["name"].lower().find("~") == -1
                ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
                    torrent = t
                    break

    # The only exception possible is that no torrent have been found when NyaaPy.Nyaa.search()
    # (we are doing dict operations on a None object => raise an exception)
    except:
        return (False, None)
    
    if torrent is None:
        return (False, None) 
    return (True, torrent['magnet'])


def nyaaFinderOld(proxies, headers, name, stringNbEp, complement =""):
        # regarde si l'uploader n'utilise pas la notation S01E01 mais 01.
        NosaisonUploader = ["Team Arcedo"]
        
        if complement in NosaisonUploader:
            saison = ""
        else:
            saison = "S01E"

        if complement != "":
            complement = complement.replace(" ", "+")

        if stringNbEp == "":
            url = f"{URL}?f=0&c=0_0&q={name}+{complement}+sub&s=seeders&o=desc"
        else:
            url = f"{URL}?f=0&c=0_0&q={name}+{saison}{stringNbEp}+vostfr+{complement}&s=seeders&o=desc"

        print(url)
        try:
            if noProxy[0]:
                response = requests.get(url, headers=headers, timeout=1)
            else:
                response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
        except:
            blocked.append(proxies)
            raise NoProxyException
        soup = BeautifulSoup(response.content, "html.parser").find('tbody')
        # magnet = soup.find('a').get("href")

        found = not (soup == None)
        
        if found:
            magnet = soup.find('tr').find_all('td')[2].find('a').find_next('a')
            return (found, magnet.get("href"))
        else:
            return (False, None)
        
def nyaaFinderTeam(proxies, headers, name, stringNbEp, user, complement =""):
    """recherche dans une équipe en partuculier"""
    if complement != "":
            complement = complement.replace(" ", "+")
    
    saison = ""
    if user == "Tsundere-Raws":
        if complement == "":
            saison = "S01E"
        else:
            saison = complement + "E"
            complement = ""
    
    if stringNbEp == "":
        url = f"{URL}user/{user}?f=0&c=0_0&q={name}+{complement}&s=seeders&o=desc"
    else:
        url = f"{URL}user/{user}?f=0&c=0_0&q={name}+{saison}{stringNbEp}+{complement}&s=seeders&o=desc"

    print(url)

    try:
        if noProxy[0]:
                response = requests.get(url, headers=headers, timeout=1)
        else:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
    except:
        blocked.append(proxies)
        raise NoProxyException
    soup = BeautifulSoup(response.content, "html.parser").find('tbody')
    # magnet = soup.find('a').get("href")

    found = not (soup == None)
    
    if found:
        magnet = soup.find('tr').find_all('td')[2].find('a').find_next('a')
        return (found, magnet.get("href"))
    else:
        return (False, None)