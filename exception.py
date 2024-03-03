class NoProxyException(Exception):
    "No proxy finder found"

# class FolderCreationException(Exception):
#     """can't create folder"""

class NoTorrentFoundException(Exception):
    """any torrent found"""

class PosterDownloadException(Exception):
    """can't download poster"""

blocked = []

files = [] #link of downloaded files

requestNB = 0 #finderrequests

moreDebug = [] #more debug info

noProxy = [] #no proxy use

customMagnet = [] #custom magnet