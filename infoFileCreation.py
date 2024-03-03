import json, mysql.connector

def littleInfoFileCreation(name, fullname, japanName, s_type, episodes, episodes_name_list, images_link, images_local_path, Os,pageMal):
    """create file the default info in a json"""
    
    data = {
        "name" : fullname,
        "type" : s_type,
        "japan_name" : japanName,
        "episode" : episodes,
        "episode_name" : episodes_name_list,
        "poster_online" : images_link,
        "poster_local" : images_local_path, 
        "info_link" : pageMal,
    }

    if Os == "nt":
        path = "Download\\" + name
        filename = "\\data.json"
    else:
        path =  "Download/" + name
        filename = "/data.json"
    with open(path+filename, "w") as f:
        json.dump(data, f)


def InfoFileCreation(name, fullname, japanName, s_type, episodes, episodes_name_list, files, images_link, images_local_path, Os,pageMal):
    """create file the default info in a json"""
    
    data = {
        "name" : fullname,
        "type" : s_type,
        "japan_name" : japanName,
        "episode" : episodes,
        "episode_name" : episodes_name_list,
        "files" : files,
        "poster_online" : images_link,
        "poster_local" : images_local_path, 
        "info_link" : pageMal,
    }

    if Os == "nt":
        path = "Download\\" + name
        filename = "\\data.json"
    else:
        path =  "Download/" + name
        filename = "/data.json"
    with open(path+filename, "w") as f:
        json.dump(data, f)
    print("Json Data File has been created successfully")

def InfoMySql(fullname, japanName, s_type, episodes, episodes_name_list, files, poster_links : list, images_local_path, pageMal):

    with open("mysqlinfo.json", "r") as f:
        data = json.load(f)

    cnx = mysql.connector.connect(
        user=data["user"], password=data["password"],
        host=data["host"],
        database=data["database"])

    cursor = cnx.cursor()

    # Insérer les données dans la table
    cursor.execute('''CREATE TABLE IF NOT EXISTS info
                (id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                type VARCHAR(255),
                alt_name VARCHAR(255),
                episode INT,
                info_link VARCHAR(255),
                poster_online TEXT,
                poster_local TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS episodes
                (line INT AUTO_INCREMENT PRIMARY KEY,
                id INT,
                name VARCHAR(255),
                episode_number INT,
                episode_name VARCHAR(255),
                video_path TEXT,
                sub_path TEXT,
                audio_path TEXT,
                FOREIGN KEY (id) REFERENCES info(id))''')

    cursor.execute("SELECT COUNT(*) FROM info WHERE name = %s", (fullname,))
    result = cursor.fetchone()[0]

    replaceTransTable = str.maketrans(",", "|", '[ ]\'\"')
    if result > 0:
        cursor.execute("UPDATE info SET type = %s, alt_name = %s, episode = %s, info_link = %s, poster_online = %s, poster_local = %s  WHERE name = %s", 
                       (s_type, japanName, episodes, pageMal, str(poster_links).translate(replaceTransTable), str(images_local_path).translate(replaceTransTable), fullname))
        
    else:
        
        # Insérer les données dans la table
        query = "INSERT INTO info (name, type, alt_name, episode, info_link, poster_online, poster_local) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (fullname, s_type, japanName, episodes, pageMal, str(poster_links).translate(replaceTransTable), str(images_local_path).translate(replaceTransTable))
        cursor.execute(query, values)

    cursor.execute("SELECT id FROM info WHERE name = %s", (fullname,))
    id_ = cursor.fetchone()[0]
    for i in range(1,episodes+1):
        cursor.execute("SELECT COUNT(*) FROM episodes WHERE name = %s AND episode_number = %s", (fullname, i))
        result = cursor.fetchone()[0]
        if result > 0:
            cursor.execute("UPDATE episodes SET id = %s, episode_number = %s, episode_name = %s, video_path = %s, sub_path = %s, audio_path = %s WHERE name = %s AND episode_number = %s", 
                       (id_, i, episodes_name_list[i-1], files[i-1]["video_path"], "fr:" + files[i-1]["sub_path"], "vo:" + files[i-1]["audio_path"], fullname, i))
        else:
            query = "INSERT INTO episodes (id, name, episode_number, episode_name, video_path, sub_path, audio_path) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (id_, fullname, i, episodes_name_list[i-1], files[i-1]["video_path"], "fr:" + files[i-1]["sub_path"], "vo:" + files[i-1]["audio_path"])
            cursor.execute(query, values)

    # Valider les changements et fermer la connexion
    cnx.commit()
    cursor.close()
    cnx.close()

    print("MySql Data has been added successfully")