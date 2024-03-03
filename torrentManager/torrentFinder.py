from header.headers import getHeaders
from torrentManager.torrentDownloader import DownloadTorrent #, oldDownloadTorrent
from torrentManager.nyaa import nyaaFinder, nyaaFinderOld, nyaaFinderTeam
#from torrentManager.tokyotosho import tokyotoshoFinder
from  torrentManager.editing import editing
import os, json
from exception import files, requestNB, customMagnet

class TorrentFinder:
    """find torrent on nyaa.si"""

    def __init__(self, s_name = None, episodes = None, s_type = None, proxies = None, fullname = None, japanName = None, path = None, Os = None, type=None, ep=None):
        

        self.headers = getHeaders()
        self.currentEpisodes = ep
        self.s_name = s_name
        self.episodes = episodes
        self.s_type = s_type
        self.proxies = proxies
        self.japanName = japanName
        self.fullname = fullname
        self.path = path
        self.os = Os
        self.type = type
        # search_query = input("search: ").replace(" ", "+")
    
    def start(self):
        global requestNB
        name = self.s_name.replace(" ", "+")
        japanName = self.japanName.replace(" ", "+")
        fullname = self.fullname.replace(" ", "+")

        magnetCustomList = []
        if customMagnet[0]:
                for i in range(self.currentEpisodes,self.episodes+1):
                    magnetCustomList.append(input("magnet ep {} : ".format(i)))

        for i in range(self.currentEpisodes,self.episodes+1):
            print("\nsearch a magnet...")
            self.currentEpisodes = i
            if self.s_type == "film":
                stringNbEp = ""
            else:
                stringNbEp = str(i)
                if(len(stringNbEp)) == 1:
                    stringNbEp = "0" + stringNbEp

            found = False
            if customMagnet[0]:
                (found, magnet) = (True, magnetCustomList[i-1])
                if magnet.lower() == "not found" or magnet.lower() == "notfound" or magnet == "404":
                    found = False
            else :
                currentRequestNB = 1

                def printRequestNB(): 
                    print("↑ requet", requestNB, "↑")
                    print()
                if currentRequestNB > requestNB:
                    (found, magnet), requestNB = nyaaFinderTeam(self.proxies, self.headers, fullname, stringNbEp, "Tsundere-Raws"), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinderTeam(self.proxies, self.headers, japanName, stringNbEp, "Arcedo", "vostfr"), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinderTeam(self.proxies, self.headers, fullname, stringNbEp, "Erai-raws", "FRE"), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinderTeam(self.proxies, self.headers, fullname, stringNbEp, "Erai-raws", "Multiple Subtitle"), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinderOld(self.proxies, self.headers, fullname, stringNbEp), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinderOld(self.proxies, self.headers, japanName, stringNbEp), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if currentRequestNB > requestNB and not found:
                    (found, magnet), requestNB = nyaaFinder(self.proxies, self.headers, self.japanName, stringNbEp), requestNB + 1
                    printRequestNB()
                currentRequestNB += 1

                if not found:
                    requestNB = 0
                    print("episode " + stringNbEp + " not found")


            
            print("\nmagnet :")
            print(magnet)
            print()
            if found:
                requestNB = 0
                DownloadTorrent(magnet, self.os, self.path)
                files_path = editing(self.path, magnet, self.os)
                # try:
                #     editing(self.path, magnet, self.os)
                # except:
                #     pass
                files.append(files_path)
            else :
                files.append({"video_path" : "not found", "sub_path" : "not found", "audio_path" : "not found"})

        try:
            os.remove(f"{self.path}/tranfer-info.json".replace("\\", "/"))
        except:
            pass