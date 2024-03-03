from scraping.scrapMal import ScrapMal
from infoFileCreation import InfoFileCreation, InfoMySql, littleInfoFileCreation
from torrentManager.torrentFinder import TorrentFinder
from exception import NoProxyException
from header.proxies import proxies
from header.headers import getHeaders
from exception import files, moreDebug, noProxy, customMagnet
import sys, mysql, json

good, scraped, scrapMal, download  = False, False, None, TorrentFinder()

if "-img" in sys.argv:
    posters = True
else:
    posters = False

if "-debug" in sys.argv:
    moreDebug.append(True)
else:
    moreDebug.append(False)

if "-noproxy" in [x.lower() for x in sys.argv]:
    noProxy.append(True)
else:
    noProxy.append(False)

if "-CustomMagnet" in sys.argv:
    customMagnet.append(True)
else:
    customMagnet.append(False)


def main(search):
    global scraped, posters, scrapMal, download
    
    # scrapMal = ScrapMal(name)
    if not scraped:
        try:
            scrapMal = ScrapMal(search, posters)
            
        except NoProxyException:
            test = input("wan't a rescan (Y/n): ")

            if(test == "Y" or test == "y" or test == None or test ==""):
                return False
            return True
        
        
        proxy = scrapMal.proxies
        scraped = True

        def startFromFirstEP():
            print("starting from scratch")
            littleInfoFileCreation(
                scrapMal.name, 
                scrapMal.fullname,
                scrapMal.japanName,
                scrapMal.type,
                scrapMal.episodes,
                scrapMal.episodes_name_list,
                scrapMal.images_link,
                scrapMal.images_local_path,
                scrapMal.os,
                scrapMal.pageMal
            )
        #recuperation des episodes locaux
        ep = 1
        try:
            url = f'{scrapMal.path}/data.json'
            with open(url, 'r') as file:
                # Load the JSON data from the file
                ep_path = json.loads(file.read())
            ep_path = ep_path["files"]
            counter = 0
            for d in ep_path:
                if "video_path" in d:
                    if d["video_path"] != "not found" :
                        counter += 1
                        files.append(d)
                    else:
                        break
            
            ep = counter + 1
            if ep == 1:
                startFromFirstEP()
        except:
            startFromFirstEP()
    else :
        proxy = proxies(getHeaders(), True)
        ep = download.currentEpisodes

    try:
        if ep <= scrapMal.episodes :
            download = TorrentFinder(
                scrapMal.name,
                scrapMal.episodes,
                scrapMal.type,
                proxy,
                scrapMal.fullname,
                scrapMal.japanName,
                scrapMal.path,
                scrapMal.os,
                scrapMal.type,
                ep
            )
            
            download.start()

        InfoFileCreation(
                    scrapMal.name, 
                    scrapMal.fullname, 
                    scrapMal.japanName, 
                    scrapMal.type, 
                    scrapMal.episodes, 
                    scrapMal.episodes_name_list,
                    files,
                    scrapMal.images_link, 
                    scrapMal.images_local_path, 
                    scrapMal.os,
                    scrapMal.pageMal,
        )
        try :
            InfoMySql(
                scrapMal.fullname, 
                scrapMal.japanName, 
                scrapMal.type, 
                scrapMal.episodes, 
                scrapMal.episodes_name_list,
                files, 
                scrapMal.images_link, 
                scrapMal.images_local_path, 
                scrapMal.pageMal
            )
        except mysql.connector.Error as error:
            print("SQL error : {}".format(error))

    except NoProxyException:
        #test = input("wan't a rescan (Y/n): ")
        test = "y"

        if(test == "Y" or test == "y" or test == None or test ==""):
            return False
        return True
    
    return True

if __name__ == "__main__":
    search = input("search: ")
    while not good:
        good = main(search)