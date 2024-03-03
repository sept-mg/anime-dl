import json, os
from torrentManager.torrentDownloader import oldDownloadTorrent
from torrentManager.convert import convertToSupported
def readTransfer(path):
    data = None
    url = f'{path}/tranfer-info.json'
    with open(url, 'r') as file:
        # Load the JSON data from the file
        data = json.loads(file.read())
    
    return data['names'][0]
        

def extract(path, editing_name, episodeTitle):
    input_file = f'"{path}/{editing_name}"'
    output_file_ass = f'"{path}/sub.ass"'
    print("\nextracting...\n")
    os.system(f'ffmpeg -y -i {input_file} -map 0:m:language:fre -v quiet {output_file_ass}')
    
    output_file = f'"{path}/{editing_name}.mkv"'
    os.rename(input_file[1:-1], output_file[1:-1])
    # os.system(f'ffmpeg -y -i {input_file} -c:v copy -c:a copy -scodec copy -v quiet {output_file}') #-metadata title="{episodeTitle}"
    convertToSupported(path, editing_name + ".mkv")
    output_audio = f'"{path}/{editing_name}.mp4"'
    print("\naudio extracting...\n")
    os.system(f'ffmpeg -y -i {output_file} -vn -b:a 320k {output_audio}')

def editing(path, magnet, Os):
    files_path = {}
    path = path.replace("\\", "/")
    filename = readTransfer(path)
    if(filename == "DownloadErrorExecption") :
        filename = oldDownloadTorrent(magnet, Os, path)
    os.rename(f'{path}/{filename}', f'{path}/edit')
    
    folder = os.path.splitext(filename)[0]

    extract(path, "edit", folder)
    
    final_path = f"{path}/{folder}".replace("\\", "/")
    os.makedirs(final_path)

    # temp = f'{final_path}/{filename}'
    # os.rename(f'{path}/edit', temp)
    # files_path['download_link'] = temp
    # os.remove(f'{path}/edit')

    temp = f'{final_path}/{folder}.mkv'
    os.rename(f'{path}/edit.mkv', temp)
    files_path['video_path'] = "anime-dl/" + temp

    temp = f'{final_path}/{folder}.mp4'
    os.rename(f'{path}/edit.mp4', temp)
    files_path['audio_path'] = "anime-dl/" + temp

    temp = f'{final_path}/{folder}.ass'
    files_path['sub_path'] = "anime-dl/" + temp
    try:
        os.rename(f'{path}/sub.ass', temp)
    except:
        files_path.update({'sub_path' : "not found"})
        print("sub not found")
    
    return files_path

    
