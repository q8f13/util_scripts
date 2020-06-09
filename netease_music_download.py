# -*- coding:utf8 -*-
# download music from netease music
# 2020.2.5

import requests
import re
import os
# from multiprocessing import Pool
import urllib
import sys
import time
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

headers = {
    'Referer': 'https://music.163.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 "
                  "Safari/537.36"
}

url = 'https://music.163.com/song/media/outer/url?id='

def get_page(url):
	if '#' in url:
		url=url.replace('#/', '')
		print('url changed to %s' % url)

	if '/my/m/music' in url:
		url=url.replace('/my/m/music', '')
		print('url changed to %s' % url)

	is_playlist=bool('playlist' in url or 'album' in url)

	if is_playlist:
		res = requests.get(url, headers=headers)
		data = re.findall(r'\<li\>\<a href=\"\/song\?id=.*?\<\/a\>\<\/li\>', res.text)
		print('analyzing and downloading playlist, please wait...')
		assert(len(data)>=1)
		for n in data:
			id=n[n.find('id=')+3:n.find('\">')]
			name=n[n.find('\">')+2:n.find('</a>')]
			# print('id: %s, name: %s' % (id,name))
			get_song((id,name))
			sys.stdout.flush()
			if n is not data[len(data)-1]:
				print('sleep 3 secs...')
				sys.stdout.flush()
				time.sleep(3.0)
	else:
		ff=urllib.request.urlopen(url)
		page=ff.read()
		data=re.findall(r'\<title\>.*\<\/title\>',page.decode())
		sep=[m.start() for m in re.finditer(' - ',data[0])]
		song_title=data[0][7:sep[1]]
		coverdom = re.findall(r'class=\"j-img\".*\>', page.decode())[0]
		cover = coverdom[coverdom.find('data-src=')+10:-2]
		# cover = coverdom[coverdom.find('data-src=')+8:coverdom.find('\"')]
		# print(song_title)
		# print(page.decode())
		print(cover)
	
		id=url[url.find('id=')+3:]
		f = get_song((id,song_title))
		get_cover(f, cover)


def get_cover(path, cover_path):
	audio = MP3(path, ID3=ID3)
	print('try getting cover image from' ,cover_path)
	img = None
	try:
		img = requests.get(cover_path, headers=headers).content
		# img = requests.get(cover_path, headers=headers).content
	except error:
		print(error)
		pass
	
	if audio.tags == None:
		audio.add_tags()
	audio.tags.add(
		APIC(
			encoding=3,
			mime='image/jpeg',
			type=3,
			desc=u'Cover',
			data=img
		)
	)

	audio.save()

def get_song(info):
	song_url = url+str(info[0])
	try:
		req = requests.get(song_url, headers=headers, allow_redirects=False)
		music_link=req.headers['Location']
		fname=(str(info[1])+'.mp3').replace('/','_').replace(':',' ')
		print('downloading %s \n => %s start' % (music_link,fname.encode('utf-8')))
		sys.stdout.flush()
		# urllib.request.urlretrieve(music_link, fname.encode('utf-8'))
		md = requests.get(music_link, headers=headers).content
		with open(fname.encode('utf-8'), 'wb') as f:
			f.write(md)
		print('downloading %s complete' % fname.encode('utf-8'))
	except Exception as e:
		print('Unexpected error:', e)
		raise
	return fname.encode('utf-8')

get_page(sys.argv[1])
