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
from mutagen.id3 import ID3, APIC, error, TPE1, TAL, TRCK, NumericPartTextFrame
from mutagen.mp3 import MP3

headers = {
    "Referer": "https://music.163.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "cookie":"JSESSIONID-WYYY=nv52rIU1mKfcCqo4BolbYnpTafJQZAN4ShhsWONCo%2BQkN2PB%2BFociJO%2B5z6rk%2F6khQzGwKQ%2FuZoehQCbmq0hrujVA3%2FHhqGQTHowfDW%2BayzD3aosjRPDspb8XOK6G%2Bc0BF%2FDg%2FY5DvumzS3sBAxQQSwIr%2BXvpXmoVY%5C3kfO1Sd7eYa%5CO%3A1614018916873; _iuqxldmzr_=32; _ntes_nnid=7d3f3ed20696adb697c39b8903f96390,1605021655445; _ntes_nuid=7d3f3ed20696adb697c39b8903f96390; NMTID=00Ovf-h0EG_gz5WkEtYm_oIIJc_UHsAAAF1sr7a3g; WM_NI=nV%2FZXWReA29bvSD7Tpwl3OycrTgbOAJaV4bXwby7lTgZTgdHr%2BzEH%2FWAOISvikwM1J%2Bfz5dZYaBgdZT86Oxx2SPAe0jqHeCu11qAP0wMDeX6nosn%2FcKUN33xgd%2FE5yoba2Q%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee9bbc63b2aa9899d53df69a8ab3c85a878e8fafae48b298acd8e26294e9a592e52af0fea7c3b92aae8ae1bbdb5d92bb8fd3bc6ab68d8cd8d77cb5b4fdb0fc69b28ca983ce4b8abf9ad5e154b5beb7d8ef60a5869c88e744b2f5b6a6cb25959f81aad27eabb5b9aeb442e9bab6d6e7529bbf8e88e75298e8fab0fb74f28da0a2e83caaaf8886c27ff3efbfa2d33cb5938c86db3eaeb1bd8fae69898b82d4b274a5bce1a6b873adbeafd3d437e2a3; WM_TID=sar%2Bllvyx4ZBVAFAUQd6d8oNj%2Fy3up7f; vinfo_n_f_l_n3=c69711b737e54c81.1.0.1612586030597.0.1612586053202; WEVNSM=1.0.0; WNMCID=gdfxnu.1605021655686.01.0; ne_analysis_trace_id=1612586030596; s_n_f_l_n3=c69711b737e54c811612586030598; MUSIC_U=0dbf635a4ff000ed0b256b841d6d2b4bfec295b63cdb5f100d4224d83774975eb8e3faaeac2dfde5c3061cd18d77b7a0; __remember_me=true; __csrf=7c33478149932f83200d9f4ca261d599"
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
        track_idx = 1
        for n in data:
            start = 13
            end = n.find("\"", 13)
            song_url = n[start:end]
            need_sleep = 1;
            try:
                need_sleep = get_song_single(domain + song_url, '%s/%s' % (track_idx, len(data)))
            except:
                print('exception occured retrieveing track %s, ignored for now' % track_idx)
                track_idx+=1
                continue;
            sys.stdout.flush()
            if n is not data[len(data)-1] and need_sleep:
                print('sleep 3 secs...')
                sys.stdout.flush()
                time.sleep(3.0)
            track_idx+=1
    else:
        get_song_single(url)

def get_song_single(url, track = None):
    # open page
    ff=urllib.request.urlopen(url)
    page=ff.read()
    # find title related info
    data=re.findall(r'\<title\>.*\<\/title\>',page.decode())
    splited = data[0].split(' - ')
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
    try:
        get_cover(f, cover, composer, album, track)
    except:
        print("err when downloading song, maybe behind paywall, delete invalid song file...")
        os.remove(f)
        return 1
    return 1

def get_cover(path, cover_path, composer, album, track):
    audio = MP3(path, ID3=ID3)
    print('try getting cover image from %s' % cover_path)
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
    if track:
        audio.tags.add(TRCK(text = track))
        print("adding track %s" % track)

    audio.save()

def get_song(info):
    song_url = url+str(info[0])
    try:
        req = requests.get(song_url, headers=headers, allow_redirects=False)
        music_link=req.headers['Location']
        fname=(str(info[1])+'.mp3').replace('/','_').replace(':',' ').replace('*', '')
        fname_encode = fname.encode('utf-8')
        if os.path.exists(fname_encode) and ignore_exist == True:
            print('ignore exist file %s' % fname_encode)
            return None
        print('downloading %s \n => %s start' % (music_link,fname.encode('utf-8')))
        sys.stdout.flush()
        # urllib.request.urlretrieve(music_link, fname.encode('utf-8'))
        md = requests.get(music_link, headers=headers).content
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
