import os, requests
from exception import NoProxyException, PosterDownloadException, noProxy

def makeFolder(name, Os, posters):
        path = "Download/" + name
        try:
            if Os == "nt":
                os.mkdir("Download\\" + name)
            else:
                os.mkdir(path)
            print(f"Download directory : {path}/")
        except:
            print("FolderCreationException")

        if posters :
            try:
                if Os == "nt":
                    poster_path = f"Download\\{name}\\poster\\"
                else :
                    poster_path = f"Download/{name}/poster/"
                os.makedirs(poster_path)
                print(f"Poster directory : {poster_path}".replace("\\", "/"))
            except:
                print("FolderCreationException")
        
        return path

def downloadPoster(images_link, name, proxies, headers, Os, posters):
    images_local_path = []
    for i in images_link:
        try :
            if noProxy[0]:
                current_image = requests.get(i, headers=headers)
            else:
                current_image = requests.get(i, proxies=proxies, headers=headers)
        except:
            raise NoProxyException
        basename = os.path.basename(i)
        if Os == "nt" :
            local_path = f"Download\\{name}\\poster\\{basename}"
        else :
            local_path = f"Download/{name}/poster/{basename}"
        if posters :
            try:
                if os.path.isfile(local_path):
                    raise PosterDownloadException
                
                with open(local_path, 'wb') as f:
                    f.write(current_image.content)
                print("Poster " + basename + " Download")
            except:
                print("PosterDownloadException")
                
            images_local_path.append(local_path.replace("\\", "/"))

    return images_local_path