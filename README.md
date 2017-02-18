# YoutubeDownloader
An mp3 downloader program written in python. Can download entire playlists or single songs
This program makes use of the youtubeinmp3.com API to download youtube videos.

Before you start
Specify your google api key - if you don't have one, get it from here https://console.developers.google.com. You must also enable the 'YouTube Data API v3' on the same site. After you get the key go to the python script and paste the api key where the googleApiKey variable is specified.

USAGE
1. 'python 1.py PATH_TO_DOWNLOAD_TO PLAYLIST_ID START_LIMIT END_LIMIT' to download a playlist from video number START_LIMIT to video number END_LIMIT.Get PLAYLIST_ID from the youtube url in your browser.
2. You can download individual songs - python 1.py PATH_TO_DOWNLOAD_TO MUSIC_VIDEO_ID
