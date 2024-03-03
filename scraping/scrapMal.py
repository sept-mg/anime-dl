import os
from exception import NoProxyException, noProxy
from header.headers import getHeaders
from scraping.scrap import scraping
from header.proxies import proxies
from scraping.make import makeFolder, downloadPoster
import requests
from bs4 import BeautifulSoup

class ScrapMal:
    """mal scapring"""
    def __init__(self, search, posters : bool):
        self.os = "linux"
        if os.name == "nt":
            self.os = "nt"
        self._headers = getHeaders()

        if noProxy == []:
            noProxy.append(True)
        if noProxy[0]:
            self.proxies = noProxy
        else:
            self.proxies = proxies(self._headers)
        

        if len(self.proxies) == 0: 
            raise NoProxyException
        (self.name, self.fullname, self.japanName, self.pageMal, self.images_link) = scraping(search, self.proxies, self._headers)
        (self.episodes,self.episodes_name_list) = (1,[self.fullname])
        self.path = makeFolder(self.name, self.os, posters)
        self.images_local_path = downloadPoster(self.images_link, self.name, self.proxies, self._headers, self.os, posters)
        self.type = "anime"
        try:
            (self.episodes, self.episodes_name_list) = self.getEpisodes(self.fullname, self.pageMal, self.proxies, self._headers)
        except:
            pass

    
    def getEpisodes(self, fullname, pageMal, proxies, headers):
        episodes_name_list = []
        try :
            def testWiki(url):
                if noProxy[0]:
                    responce = requests.get(url, headers=headers)
                else:
                    responce = requests.get(url, proxies=proxies, headers=headers)

                return BeautifulSoup(responce.content, 'html.parser')

            soup_episodes = testWiki("https://en.wikipedia.org/w/index.php?search=" + fullname)

            found = (soup_episodes.find('span', id='Anime') != None)

            if not found:
                soup_episodes = soup_episodes.find('table', class_='infobox').find('tbody').find_all('tr')
                for current in soup_episodes:
                    if( current.find('th') != None and current.find('th').get_text().startswith('Episode')):
                        current = current.find('td').find('a').get('href')
                        found = (current != None)
                        if found :
                            url = "https://en.wikipedia.org" + current
                            soup_episodes = testWiki(url)
                            print(url)
                            break
            if found:
                if(soup_episodes.find('table', class_='wikiepisodetable') == None):
                    soup_episodes = soup_episodes.find('span', id="Episodes")
                    found = (soup_episodes != None)
                    if found :
                        soup_episodes = soup_episodes.find_next('table').find('tbody').find_all('tr', class_="vevent") 
                elif found :
                    soup_episodes = soup_episodes.find('table', class_='wikiepisodetable').find('tbody').find_all('tr', class_="vevent")
                
                if found:
                    for current in soup_episodes:
                        current = current.find('td').contents[0].strip()[1:-1]
                        episodes_name_list.append(str(current))
        except:
            found = False

        if not found :
            try :
                if noProxy[0]:
                    responce = requests.get(pageMal + "/episode", headers=headers)
                else:
                    responce = requests.get(pageMal + "/episode", proxies=proxies, headers=headers)
                
                if responce.status_code == 404:
                    self.type = "film"
            except:
                self.type = "film"

            soup_episodes = BeautifulSoup(responce.content, 'html.parser').find_all('table')[3].find_all('tr')
            i = 1
            for current in soup_episodes:
                if i == 1:
                    i = 0
                    continue
                current = current.find('td', class_="episode-title").find('a').get_text()
                episodes_name_list.append(str(current))
        
        result = len(episodes_name_list)
        if(episodes_name_list[-1] == 'ranscription: '):
            episodes_name_list.pop()
            result-=1

        print("Episode Titles : " + str(episodes_name_list))
        
        print("Episode number : " + str(result))
        return (result, episodes_name_list)

    
