import os, json


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

def get_video_bitrate(filename):
    default_bitrate = "5M"
    # Utiliser la commande ffprobe pour récupérer les informations du fichier vidéo
    command = f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of json "{filename}"'
    result = os.popen(command).read()

    # Analyser les informations JSON pour récupérer le bitrate vidéo
    info = json.loads(result)
    if 'streams' in info and len(info['streams']) > 0:
        video_stream = info['streams'][0]
        if 'bit_rate' in video_stream:
            return video_stream['bit_rate']

    # Le bitrate vidéo n'a pas été trouvé
    else:
        return default_bitrate

def is_audio_codec_compatible(filename):
    # Utiliser la commande ffprobe pour récupérer les informations du fichier audio
    command = f'ffprobe -v error -show_streams -select_streams a:0 -of json "{filename}"'
    result = os.popen(command).read()

    # Analyser les informations JSON pour vérifier le codec audio
    info = json.loads(result)
    audio_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream is None:
        # Aucun flux audio trouvé
        return False

    # Vérifier que le codec audio est compatible avec les navigateurs
    codec = audio_stream['codec_name']
    return codec in ['aac', 'pcm_mulaw', 'pcm_alaw', 'libmp3lame', 'libopus', 'flac', 'wave']




def convertToSupported(path, filename):
    output_file = f"{path}/{filename}"
    (needVideoConvert, needAudioConvert) = (not is_video_codec_compatible(output_file), not is_audio_codec_compatible(output_file))
    if (not needVideoConvert) and (not needAudioConvert):
        return True
    
    
    temp_file = f"{path}/temp.mkv"
    os.rename(output_file, temp_file)
    

    if needVideoConvert and needAudioConvert:
        bitrate = get_video_bitrate(temp_file)
        # Convertir à la fois la vidéo et l'audio
        try:
            os.system(f'-scodec copy')
            os.remove(temp_file)
        except:
            os.rename(temp_file, output_file)
            print("conversion failed")
            return False

    elif needVideoConvert:
        bitrate = get_video_bitrate(temp_file)
        # Convertir uniquement la vidéo
        try:
            os.system(f'ffmpeg -i "{temp_file}" -vcodec libx264 -b:v {bitrate} -c:a copy -scodec copy "{output_file}"')
            os.remove(temp_file)
        except:
            os.rename(temp_file, output_file)
            print("conversion failed")
            return False

    elif needAudioConvert:
        # Convertir uniquement l'audio
        try:
            os.system(f'ffmpeg -i "{temp_file}" -c:v copy -c:a aac -ar 44100 -b:a 320k -scodec copy "{output_file}"')
            os.remove(temp_file)
        except:
            os.rename(temp_file, output_file)
            print("conversion failed")
            return False

    return True