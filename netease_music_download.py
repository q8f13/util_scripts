# -*- coding:utf8 -*-
# download music from netease music
# 2020.8.3

import requests
import re
import os
# from multiprocessing import Pool
import urllib
import sys
import time
from mutagen.id3 import ID3, APIC, error, TPE1, TAL
from mutagen.mp3 import MP3

headers = {
    "Referer": "https://music.163.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "cookie":"JSESSIONID-WYYY=0mQzqffYpyykD1dP%2BWAGc4HMYvI9feCU8gIGytuTld7mn7OX42Mm9yf7h8JF2y5qs2At3fYYEB7Aq5Vz%2BAHYq35Wj7DXiJ9CCdBMhIHaENr7SFbPrirs0W%2Bf1mXG5cFpQvTKgWHBruCNy33pDgQC%2BGymwKxCEcojGaKlr%2FKQGC0CYdFD%3A1593775427643; _iuqxldmzr_=32; _ntes_nnid=8149fac49738c8f7e914d371cbf8a0b9,1590637819707; _ntes_nuid=8149fac49738c8f7e914d371cbf8a0b9; WM_NI=SFKpIwKfH0%2Butl7J2L8jAMojUsxSwYE9Z4M7Xpea4GL5JRlVDNyHw0oWgrwc3U%2Bvqk7%2BmN98yHyFpK%2Bwv1OmpGzMXHBgaZxHnoZAVxu%2BRmJ9dLi5g8rdp%2FnFjjCJhwVqT1Y%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeaff6808eeda490c16792b08aa3c54b878a8eabf460b596a485e57b9b9b85b4cd2af0fea7c3b92a919a8591cc7d89ba88d1aa7fb8b4f9abb148fcb68faeee6297adb8b4f65387e796d5d03d9cb0ab82b74d90eb86b3ef5e8892b7a9f63cad89a993f669f18be597f461f5f5a3afbc34bb98b7a7f341e9a9bad2ce67b499b6aedb4482b9afbbfb44aeb196a2d574b7f59e8ec933a894a7d6e634b2bcc0d0ed4eaab68dabeb7d96af9cd2dc37e2a3; WM_TID=LOFMCAfj6%2BpAEAFVQRJ7SWeDaGy%2Fl1K3; playerid=89565470; MUSIC_U=13ed853b271ff47be61277cccd76c83f5ad7bfae54577152b3dada19dbba5eb6a1dbc3772dc096f12b09be53347219dfbf122d59fa1ed6a2; __remember_me=true; __csrf=f61370320823b99083e35a2862db4f3c"
}

url = 'https://music.163.com/song/media/outer/url?id='
domain = 'https://music.163.com'

ignore_exist = False

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
		# song_url_list = re.findall(r'\/song\?id=.*?\<\/a\>',res.text)
		print('analyzing and downloading playlist, please wait...')
		assert(len(data)>=1)
		for n in data:
			start = 13
			end = n.find("\"", 13)
			song_url = n[start:end]
			need_sleep = get_song_single(domain + song_url) == 1
			sys.stdout.flush()
			if n is not data[len(data)-1] and need_sleep:
				print('sleep 3 secs...')
				sys.stdout.flush()
				time.sleep(3.0)
	else:
		get_song_single(url)

def get_song_single(url):
	# open page
	ff=urllib.request.urlopen(url)
	page=ff.read()
	# find title related info
	data=re.findall(r'\<title\>.*\<\/title\>',page.decode())
	splited = data[0].split('-')
	sep=[m.start() for m in re.finditer(' - ',data[0])]
	composer = splited[1]
	song_title=data[0][7:sep[0]]
	# find album info
	album_raw = re.findall(r'\<meta property="og:music:album".*\>', page.decode())
	# <meta property="og:music:album" content="Snö">
	album = album_raw
	if len(album_raw) < 1:
		print("fail to find album")
	else:
		equal_char_idx = album_raw[0].rfind('=')
		album = album_raw[0][equal_char_idx+2:-3]
		# print(album_raw[0][equal_char_idx+2:-3].encode('utf-8'))
	coverdom = re.findall(r'class=\"j-img\".*\>', page.decode())[0]
	cover = coverdom[coverdom.find('data-src=')+10:-2]
	# print(cover)

	id=url[url.find('id=')+3:]
	f = get_song((id,song_title))
	if f == None:
		return 0
	get_cover(f, cover, composer, album)
	return 1

def get_cover(path, cover_path, composer, album):
	audio = MP3(path, ID3=ID3)
	print('try getting cover image from' ,cover_path)
	img = None
	try:
		img = requests.get(cover_path, headers=headers).content
		# img = requests.get(cover_path, headers=headers).content
	except error:
		print(error)
		return
	
	if audio.tags == None:
		audio.add_tags()
	audio.tags.add(
		APIC(
			encoding=3,
			mime='image/jpeg',
			type=3,
			desc=u'Cover',
			data=img,
		)
	)
	audio.tags.add(TPE1(text = composer))
	audio.tags.add(TAL(text = album))

	audio.save()

def get_song(info):
	song_url = url+str(info[0])
	try:
		req = requests.get(song_url, headers=headers, allow_redirects=False)
		music_link=req.headers['Location']
		fname=(str(info[1])+'.mp3').replace('/','_').replace(':',' ').replace('*', '')
		print('downloading %s \n => %s start' % (music_link,fname.encode('utf-8')))
		sys.stdout.flush()
		# urllib.request.urlretrieve(music_link, fname.encode('utf-8'))
		md = requests.get(music_link, headers=headers).content
		fname_encode = fname.encode('utf-8')
		if os.path.exists(fname_encode) and ignore_exist == True:
			print('ignore exist file' % fname_encode)
			return None
		with open(fname_encode, 'wb') as f:
			f.write(md)
		print('downloading %s complete' % fname_encode)
	except Exception as e:
		print('Unexpected error:', e)
		raise
	return fname_encode

if len(sys.argv) > 2:
	ignore_exist = sys.argv[2] == "1"
get_page(sys.argv[1])
