import requests
from bs4 import BeautifulSoup

# place
# _________________________________________________________________
# ____________________SUBS FROM OPENSUBTITLES.ORG__________________
# _________________________________________________________________

base_url = "https://www.opensubtitles.org/fr/search/sublanguageid-fre/imdbid-"
dlbase_url = "https://dl.opensubtitles.org/fr/download/sub/"


def GetLinkSub(imdb_id):  # Returns direct dl link for the best French srt
    response = requests.get(base_url + imdb_id)
    if response.status_code == 404:
        print("Subtitle removed by DCMA")
        return "Removed by DCMA"
    elif response.status_code != 200:
        raise Exception("Change proxy")
    page = response.content.decode()
    if "OpenSubtitles.org was HACKED" in page:
        raise Exception("Change proxy")

    soup = BeautifulSoup(page, 'html.parser')
    for divSub in soup.find_all('tr'):  # Verify that the sub got 1CD and BluRay in his file_title
        if divSub.get('id') and divSub.get('id')[:4] == "name" and divSub.find_all('td')[2].text[0] == '1':
            content = divSub.find_all('td')[0].text[:-48]
            begin = content.find(')')
            file_title = content[begin+1:]
            if 'BluRay' in file_title:
                id_open_subtitle = divSub.get('id')[4:]
                print(f"BluRay sub: {id_open_subtitle}")
                return f"{dlbase_url}{id_open_subtitle}"

    for divSub in soup.find_all('tr'):  # Verify that the sub got 1CD and BluRay in his file_title
        if divSub.get('id') and divSub.get('id')[:4] == "name" and divSub.find_all('td')[2].text[0] == '1':
            id_open_subtitle = divSub.get('id')[4:]
            print(f"Recent sub: {id_open_subtitle}")
            return f"{dlbase_url}{id_open_subtitle}"

    for divSub in soup.find_all('h3'):
        for a in divSub.find_all('a'):
            if a.get('ret'):
                id_open_subtitle = a.get('ret').split('/')[3]
                print(f"Default sub: {id_open_subtitle}")
                return f"{dlbase_url}{id_open_subtitle}"

    print("Not found / Speechless")  # No sub file found
    return "Not found / Speechless"