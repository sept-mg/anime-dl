import os

def DownloadTorrent(magnet, Os, path):
      if Os == "nt":
            os.system(f'node .\\torrent-master\\cli.js "{magnet}" --path="{os.getcwd()}\\{path}"')
      else:
            try :
                os.system(f'node torrent-master/cli.js "{magnet}" --path="{os.getcwd()}/{path}"')
            except:
                os.system("sudo apt-get install nodejs")
                os.system(f'node torrent-master/cli.js "{magnet}" --path="{os.getcwd()}/{path}"')

def oldDownloadTorrent(magnet, Os, path):
    if Os == "nt":
                    os.system('.\\aria2\\aria2c -d ".\\' + path.replace('/','\\') + '" --seed-time=0 "' + magnet +'"')
    else:
        try :
            os.system('aria2c -d "/' + path + '" --seed-time=0 "' + magnet + '"')
        except:
            os.system("sudo apt-get install aria2")
            os.system('aria2c -d "/' + path + '" --seed-time=0 "' + magnet + '"')
    
    
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    return files[0]