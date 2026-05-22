# -*- coding:utf8 -*-
# download music from netease music
# 2020.8.3

# if encounting any issue, try update 'cookie' in headers

import requests
import re
import os
# from multiprocessing import Pool
import urllib
import sys
import time
from mutagen.id3 import ID3, APIC, error, TPE1, TAL, TRCK, NumericPartTextFrame, PictureType, ID3NoHeaderError
from mutagen.mp3 import MP3

headers = {
    "Referer": "https://music.163.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "cookie":"_ntes_nnid=5cd17590f4e9046d9b337bdf41081767,1753761830051; _ntes_nuid=5cd17590f4e9046d9b337bdf41081767; NMTID=00O5puBeRnZGVLV8kOKiHIzPW7IwEUAAAGYVFnQIg; WNMCID=kyredy.1753761830351.01.0; __snaker__id=CpWSAWd95ydeCqOW; NTES_P_UTID=k98kqHLUXerNJZn0mlZejIEsPp0hur1G|1779336869; MUSIC_U=00959300D3B47F9063C16926453459C608D7A02029F2F0609C0D2AF1C15200B4CED1C897ADF0105A3F8BC6E8A077C11EEEEA3D33ECE995A58D50423ABAE142DD7234DAFA7091868A234EFDC8960A0ABC51FA9C8B93E90E790AFCE8E8DC27131E79191D18C4175EA87113386683871770A4B83E41CEC6911847C9A363FA5331E4A3603570BA3316A94E87F61611AE4A15D76A280334508AB4948584AE8C1B9EB452EC3A9B74C26ED4536999159FE973F4335E31E1BE6D257CB58D3E45C87E867DDC8FEE8D943AA3540C9AA34EF36695DD3B9F586FCF8ED16939B1D86A01DF8298E6CF8377A6795019F95248B6E7A92F35FDDFB64AF99C8A79068989C4D16832444CFF9F0E2B17B57B7579AEAAFBC7CB1633111A13DE4AB79AB87C2C036C6C7E6E3362923587EDA4F5540BB4EC1E064D1CD282ADF6D441AE26158025EDF04DEDDD95D5538419165A88BF3459265190813D5CAE29E80C5D05EA624529A08FA979EF058ABB4CAD713C4BE6DB9870206E547F06; __remember_me=true; ntes_kaola_ad=1; __csrf=bb71a6611e63a5fcf4aacbc4124b32b3; __csrf=4c5cb95aa8239865284daa834b6f589b; timing_user_id=time_Tg1YI3yNg3; JSESSIONID-WYYY=sTcG0t2mcHcjIOuB23b3fBVaFJpxxWHBTiM65IuR6c6iuRitiIZU0xhUsdn5nBRxW0P4BTFmzANdNh%5CiJneZSiVuIbfowFEEc07dJHWAy%2BUXGcq17197G1oZ4KkeEfO9yqNlJRkh%5Cu6%2BOkTHmoDXk3714U1Xoq2ssdfja05BJGVpz0Aa%3A1779436597236; _iuqxldmzr_=32; WEVNSM=1.0.0; WM_NI=CRI39fhMuuHVvFg9L427S8fESpSpPus1ZWOr8g9HnX54tU9sKS%2FQ81cK%2FbT7NmEQf1HoCT5Q9DiDJPP7QH61ak1ueB110cgR2eRoZu6cg3XP0imo5L6rn%2BVNKYZTsGLyNEE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee96f23cabbda2d2e53db28e8ab6d54f968a8ab0c77a818cfc85aa34908b8499f12af0fea7c3b92a818e87d4bc6eac93bb96cb5eb69aa9dacf40f2e99dd9e54f91b09d91d37fb1ef96b8ce7afcb9f7a9ed54f7ecbcb6bc79898de1b2bb3ba195e183d73d8eb38bb2e53b8cb18db5b85bfb9ca7a5c95c94e99fa9b53ba3b5ff96e84af3ef0084e65af2bb9e90d97ff6bda9d4db5cf4b7a390b848f6aea2ccd546898796b5f24d90a782a6c837e2a3; WM_TID=2F3UXQZe3ktEEUVERFfTxXYlJsL9hmuX; gdxidpyhxdE=AKjl7U2PmV5%2BiO7%2FBgZs4r6KRVMsHTufMuAwLvdwTpIJOMfstj3IXufnGoMPRS9%2Fd07OMyP94xpWvEgpS%2BU5ZJfcY9tC3IkBCyhvQ3WWvOn73kZOOCXiGVtRl0S%5CeoOKtdMb5%2BQicN2%2FiYB8MVwdxTn0AGKS81jYoCGjX%2FysaJvM%5C%2BPk%3A1779342801945; P_INFO=spiritswithin@163.com|1779336869|0|music|11&19|bej&1775618454&music#bej&null#10#0#0|&0||spiritswithin@163.com; _ntes_origin_from=duckduckgo.com; playerid=65061081"
}

url = 'https://music.163.com/song/media/outer/url?id='
domain = 'https://music.163.com'

ignore_exist = True

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
        assert(len(data) >=1)
        print('analyzing and downloading playlist, count: %s, please wait...' % len(data))
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
                print('sleep 1 secs...')
                sys.stdout.flush()
                time.sleep(1.0)
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
    # cover = coverdom[coverdom.find('data-src=')+10:-2]
    cover = coverdom[coverdom.find('data-src=')+10:coverdom.find('jpg')+3]
    # print("cover url detect: %s" % cover)

    id=url[url.find('id=')+3:]
    f = get_song((id,song_title))
    if f == None:
        return 0
    try:
        get_cover(f, song_title, cover, composer, album, track)
    except requests.HTTPError as e:
        print(e)
        print("err when downloading song, maybe behind paywall, delete invalid song file...")
        os.remove(f)
        return 1
    return 1

def get_cover(path, title, cover_path, composer, album, track):
    audio = MP3(path, ID3=ID3)
    print('try getting cover image from %s' % cover_path)
    res = requests.get(cover_path)
    # res = requests.get(cover_path, headers=headers)
    res.raise_for_status()
    img = res.content
    # img = requests.get(cover_path, headers=headers).content
    try:
        audio = ID3(path)
    except ID3NoHeaderError:
        print("no ID3 header found, creating one...")
        audio = ID3()

    audio.delall('APIC')
    audio.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            title=title,
            type=3,
            desc=u'Cover',
            data=img,
        )
    )
    audio.add(TPE1(text = composer))
    audio.add(TAL(text = album))
    if track:
        audio.add(TRCK(text = track))
        print("adding track %s" % track)

    audio.save(path, v2_version=3)
    print("Tags saved successfully.")
    

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
