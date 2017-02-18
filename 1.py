import requests
import urllib
import urllib2
import os
import sys
import time
from bs4 import BeautifulSoup
import re

#change proxy or set to ' ' if no proxy
proxies = {'http' : 'http://proxy.iiit.ac.in:8080','https' : 'http://proxy.iiit.ac.in:8080'}

symbol = "()"

myPath = ''

#change your path as required
myPath = '/home/' + sys.argv[1]

#input your playlist ID and your google api key
googleApiKey = ''

def check():
	if len(sys.argv) < 3:
		print "Usage - 'python 1.py PATH_TO_DOWNLOAD_TO PLAYLIST_ID START_LIMIT END_LIMIT' to download a playlist whose id you should pass as a command-line arg.START_LIMIT and END_LIMIT specify the range of songs to download"
		print "Also you can download individual songs - python 1.py MUSIC_VIDEO_ID"
		exit(0)
	elif len(sys.argv) == 3:
		downloadVid(str(sys.argv[2]))
		exit(0)
	else:
		playlistId = str(sys.argv[2])
		limit1 = int(sys.argv[3])
		limit2 = int(sys.argv[4])
		chooseLink(limit1,limit2,playlistId)


def downloadVid(id1):
	resp = ''
	x = True
	url = ''
	response = ''
	while x:
		print 'https://www.youtubeinmp3.com/fetch/?format=JSON&video=https://www.youtube.com/watch?v=' + id1
		resp = requests.get('https://www.youtubeinmp3.com/fetch/?format=JSON&video=https://www.youtube.com/watch?v=' + id1)
		# if resp.headers['content-type'] == 'text/html':
		# 	st = resp.text
		# 	print resp.text
		# 	l = len(resp.text)
		# 	z = st.find("url")
		# 	url = st[z+4:l-3]
		# 	x = False
		# else:
		response = resp.json()
		# print response['link']
		if response['link'] != '':
			x = False
		print "Checking"
	# if url == '':
	response = resp.json()
		# print response['link']
	url = response['link']
	# print "Downloading " + response['title']
	filename = os.path.join(myPath, response['title'] +'.mp3')
	url = response['link']
	# proxy = urllib2.ProxyHandler(proxies)
	# opener = urllib2.build_opener(proxy)
	# urllib2.install_opener(opener)
	# usock = urllib2.urlopen(url)
	#string = []
	usock = requests.get(url,stream=True)
	# length = len(filename)
	# for i in xrange(0,length):
	# 	# print filename[:i] + '\\' + filename[i:]
	# 	if filename[i] == ' ' or filename[i] in symbol:
	# 		string.append('\\')
	# 		string.append(filename[i])
	# 	else:
	# 		string.append(filename[i])
	# filename = ''
	# for i in xrange(0,len(string)):
	# 	filename = filename + string[i]
	# print filename
	f = open(filename, 'wb')
	x = str(usock.headers['content-type'])
	if x == 'text/html':
		soup = BeautifulSoup(usock.text,'lxml')
		for link in soup.findAll('a', attrs={'href' : re.compile("/download"),'class' : 'button fullWidth'}):
				link = str(link)
				i = link.index('?')
				j = link.find("id=",40)
				j = j - 2
				link = 'http://www.youtubeinmp3.com/download/get' + link[i:j]
				usock1 = requests.get(link,stream=True)
				y = str(usock1.headers['content-type'])
				print "Downloading: %s" % (filename)
				for chunk in usock1.iter_content(chunk_size=512 * 1024):
				   	if not chunk:
				    		break
					f.write(chunk)
					f.flush()
		f.flush()
		f.close()
	# file_size = int(usock.headers['Content-Length'])
	# size = float(file_size/float(1048576))
	# print "Downloading: %s Size: %2.1f MB" % (filename, size)
	else:
		print "Downloading: %s" % (filename)
		for chunk in usock.iter_content(chunk_size=512 * 1024):
			# sys.stdout.flush()
		   	if not chunk:
		    		break
		 	# downloaded = downloaded + len(chunk)
		 	# download_status = downloaded * 100.00 / file_size
			f.write(chunk)
			f.flush()
			# sys.stdout.write('%3.2f%%\r' % download_status)
	  #   	sys.stdout.flush()
	  	f.flush()
		f.close()
	print "Done"

def chooseLink(limit1,limit2,playlistId):
	pageToken = ''
	while limit1 >= 50:
		resp1 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken='+pageToken+'&playlistId=' + playlistId + '&key=' + googleApiKey)
		response1 = resp1.json()
		pageToken = response1['nextPageToken']
		# print pageToken
		limit1 = limit1 - 50
		limit2 = limit2 - 50
		# print response1['items'][]['snippet']['resourceId']['videoId']
	limit1 = limit1 - 1
	limit2 = limit2 - 1
	pageTok = ''
	resp1 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken='+pageToken+'&playlistId=' + playlistId + '&key=' + googleApiKey)
	# pageTok = resp1.json()['nextPageToken']
	prevLastIdTemp = resp1.json()['items'][limit1]['snippet']['resourceId']['videoId']
	x = limit1
	while x <= limit2:
		if x % 50 == 0 and x > 0:
			pageToken = pageTok
			resp1 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken='+pageToken+'&playlistId=' + playlistId + '&key=' + googleApiKey)
		# print response1['items'][0]['snippet']['resourceId']['videoId']
			pageTok = resp1.json()['nextPageToken']
			x = 0
			limit2 = limit2 - 50
		if resp1.status_code != 200:
		    # This means something went wrong.
		    raise ApiError('GET /tasks/ {}'.format(resp1.status_code))
		    print("Woooops")
		if resp1.status_code == 200:
			response = resp1.json()
			pageToken = response['nextPageToken']
			vidId = response['items'][x]['snippet']['resourceId']['videoId']
			# if vidId == prevLastId:
			# 	print "Already updated"
			# 	exit(0)
			# else:
			# print vidId
			downloadVid(vidId)
			#print vidId
		x = x + 1
check()
