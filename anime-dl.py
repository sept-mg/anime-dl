from subprocess import call, CalledProcessError
from os import name, path
response = "-1"

currentPath = path.dirname(path.abspath(__file__)) + "/"

if name == "nt":
    pythonPath = "python"
else:
    pythonPath = "python3"

print("")
print("*********************************\n")
print("[0] Ajout Complet sans proxy\n")
print("[1] Ajout Complet avec proxy\n")
print("[2] Ajout Série/film en db\n")
print("[3] Ajout de série avec magnet et sans proxy\n")
print("[4] Ajout de série avec magnet\n")
print("[5] Ajout de série depuis un dossier magnet sans proxy\n")
print("*********************************\n")

while (not response.isdigit() or int(response) < 0 or int(response) > 5):

    response = input("Choisissez votre option : ")

response = int(response)
if response == 0:
    try:
        call([pythonPath, currentPath + "main.py", "-noproxy"])
    except CalledProcessError as e:
        print("Erreur lors de l'exécution du script :", e)

elif response == 1:
    try:
        call([pythonPath, currentPath + "main.py"])
    except CalledProcessError as e:
        print("Erreur lors de l'exécution du script :", e)

elif response == 2 :
    from scraping.scrapMal import ScrapMal
    search = input("search: ")
    scrapMal = ScrapMal(search, False)

    from infoFileCreation import InfoFileCreation, InfoMySql
    from mysql import connector

    files = []

    for i in range(scrapMal.episodes):
        files.append({"video_path" : "not found", "sub_path" : "not found", "audio_path" : "not found"})

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
    except connector.Error as error:
        print("SQL error : {}".format(error))


elif response == 3:
    print("si vous n'avez pas trouvé de magnet, alors indiqué \"not found\"")
    try:
        call([pythonPath, currentPath + "main.py", "-CustomMagnet", "-noproxy"])
    except CalledProcessError as e:
        print("Erreur lors de l'exécution du script :", e)

elif response == 4:
    print("si vous n'avez pas trouvé de magnet, alors indique \"not found\"")
    try:
        call([pythonPath, currentPath + "main.py", "-CustomMagnet"])
    except CalledProcessError as e:
        print("Erreur lors de l'exécution du script :", e)

elif response == 5:
    input("WIP")
    from scraping.scrapMal import ScrapMal
    search = input("search: ")
    scrapMal = ScrapMal(search, False)

    from torrentManager.torrentDownloader import  DownloadTorrent
    DownloadTorrent(input("magnet: "), scrapMal.os, scrapMal.path)

    import os, json
    isfoldersource = True
    tempPath = scrapMal.path + "/" + os.listdir(scrapMal.path)[0]
    if((not os.path.exists(tempPath)) and os.path.isfile(tempPath)):
        isfoldersource = False
        tempPath = scrapMal.path
    

    # Filtrer les fichiers avec l'extension ".mkv"
    fichiers = [fichier for fichier in os.listdir(tempPath) if fichier.endswith('.mkv')]
    fichiers.sort()

    def is_video_codec_compatible(filename):
        # Utiliser la commande ffprobe pour récupérer les informations du fichier vidéo
        command = f'ffprobe -v error -show_streams -select_streams v:0 -of json "{filename}"'
        result = os.popen(command).read()

        # Analyser les informations JSON pour vérifier le codec vidéo
        info = json.loads(result)
        video_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            # Aucun flux vidéo trouvé
            return False

        # Vérifier que le codec vidéo est compatible avec les navigateurs
        codec = video_stream['codec_name']
        return codec in ['h264', 'vp8', 'vp9']

    # def is_audio_codec_compatible(filename):
    #     # Utiliser la commande ffprobe pour récupérer les informations du fichier audio
    #     command = f'ffprobe -v error -show_streams -select_streams a:0 -of json "{filename}"'
    #     result = os.popen(command).read()

    #     # Analyser les informations JSON pour vérifier le codec audio
    #     info = json.loads(result)
    #     audio_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'audio'), None)
    #     if audio_stream is None:
    #         # Aucun flux audio trouvé
    #         return False

    #     # Vérifier que le codec audio est compatible avec les navigateurs
    #     codec = audio_stream['codec_name']
    #     return codec in ['aac', 'pcm_mulaw', 'pcm_alaw', 'libmp3lame', 'libopus', 'flac', 'wave']
    files = []
    from infoFileCreation import InfoFileCreation, InfoMySql
    for i in range(len(fichiers)):
        print(fichiers[i])

       

        input_file = tempPath + "/" + fichiers[i]
        name = os.path.splitext(fichiers[i])[0]
        output_file = scrapMal.path + "/" + name + "/" + name
        try:
            os.mkdir(scrapMal.path + "/" + name)
        except:
            pass

        print("\nextracting sub...\n")

        tracks = os.popen(f'ffprobe -v error -select_streams s -show_entries stream=index:stream_tags=language -of csv=p=0 {input_file}').read().split("\n")
        tracks.remove("")
        result = {}
        for j in tracks:
            a, b = j.split(",")
            result[b] = a
        
        os.system(f'ffmpeg -y -i "{input_file}" -map 0:{result["fre"]} "{output_file}.ass"')

        print("\nextracting video...\n")
        if(not is_video_codec_compatible(input_file)):
            os.system(f'ffmpeg -i "{input_file}" -vcodec libx264 -b:v 6M -c:a copy -scodec copy "{output_file}.mkv"')
        else:
            os.system(f'ffmpeg -i "{input_file}" -c:v copy -c:a copy -scodec copy "{output_file}.mkv"')

        print("\nextracting audio...\n")
        os.system(f'ffmpeg -y -i "{input_file}" -vn -b:a 320k "{output_file}.mp4"')

        if(not isfoldersource):
            if os.name == "nt":
                os.remove(input_file)
            else:
                os.system("rm -rf " + input_file)

        files.append({"video_path" : "anime-dl/" + output_file + ".mkv", "sub_path" : "anime-dl/" + output_file + ".ass", "audio_path" : "anime-dl/" + output_file + ".mp4"})
    
    if(isfoldersource):
        rem ="rm -rf "
        if os.name == "nt":
            rem = "rm "

        os.system(rem + tempPath)
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
    except Exception as e:
        print(e)