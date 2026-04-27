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
from mutagen.id3 import ID3, APIC, error, TPE1, TAL, TRCK, NumericPartTextFrame
from mutagen.mp3 import MP3

headers = {
    "Referer": "https://music.163.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "cookie":"_ntes_nnid=5cd17590f4e9046d9b337bdf41081767,1753761830051; _ntes_nuid=5cd17590f4e9046d9b337bdf41081767; NMTID=00O5puBeRnZGVLV8kOKiHIzPW7IwEUAAAGYVFnQIg; WNMCID=kyredy.1753761830351.01.0; NTES_P_UTID=k98kqHLUXerNJZn0mlZejIEsPp0hur1G|1777261103; MUSIC_U=004CB89896118F9C351FD0F3AD5078129126A40A998524F88C6D57D74216A8CF98C6538510EC0F998EB7D0F34D2B2DAE65CC0995D979BB6169A87569372D7BE4E503E72DDB07637D217744BB4F329B0A652A0521559AEA8F60496FD0ACB23EC7DF38B66ADF5EF739A35B1832287754D9293CEEADEA29FBBB738F00680FB27F0A631D65AA3D5A2CDC2A218E5286F5AE8D44D9BC2FDBD7F3EA0BE4CD7A459DC46A7CFA3378FAF4F92D368D72C02DD0B477C46F8E362775169F05A6A03B9B9E07FCBE74A3EA7BABED5FA3818CA8E14743CC26B3629B444CF12EE056ED070B390E446900622FE1044BBD53B41F98464D3549BA6C4486B362125ECFDDF918073578CA60F843ED14F9156D2DF9A8DF1E34BC51A6211B79C9683B1EBBE0947C631D4E50DAE418DF98DC4DD5453FDE71FB2CD99274F32E156917E5077DD7237CEC54305D1C2A11996FEF54D16DCEAEEED3E4B55480FF73A1B5593CFF1955C9B3FA0AD86B266FDE9A2BBCEC69AFEF73AB004A1B4FDA; __remember_me=true; ntes_kaola_ad=1; __csrf=4c5cb95aa8239865284daa834b6f589b; JSESSIONID-WYYY=WJgWxtZ5UpmBnsgSd6xNvCzq%2FUvRbE2SowakXtqhGlemKlNmoT0qmhXqorGBY5BioQVZmIf5z0dvV3%5C6zJA4NZlPSYbrq1zdSTPdTRFrG%2BZ6sIH4SkKxRz7HCWKHszB%2F0boye%2B2%2F4o4e47YuUuHWY6Za43Fm26OFxCF%5CkGo4w7V4S%5C8I%3A1777264619877; _iuqxldmzr_=32; WEVNSM=1.0.0; NTES_SESS=PDbb2DidBM8z5ByiCGsZrTtP6W2woLYfRwMwuaxdTtW4VQXFV_orx5MkyihM9pweDNOfVNYtLTjmLudGWTKucg3cTdU6wm_Nz3fYroJZyImyBB9Y1C1Ai5C_B9IEnQsv77556WQ_Ziknleuxyl.zoja2I37mEafUp6txuGcuKlv32qtRGYIqml.McmG72GqGZRlQ9igh7WSK5; S_INFO=1777261103|0|3&80##|spiritswithin; P_INFO=spiritswithin@163.com|1777261103|0|music|11&19|bej&1773111541&music#bej&null#10#0#0|&0||spiritswithin@163.com"
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
        assert(len(data)>=1)
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
