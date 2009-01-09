import urllib,urllib2,re,xbmcplugin,xbmcgui

################################
#     TV SHACK PLUGIN 2008.    #
#############VOIN###############

def CATS():
        addDir("1. ANIME","http://tvshack.net/anime",1,"http://www.grandedeluxe.com/images/anime_logo_big.jpg")
        addDir("2. MOVIES","http://tvshack.net/movies",1,"http://www.learncoombedean.co.uk/mediamadness/images/movies_logo.gif")
        addDir("3. T.V SHOWS","http://tvshack.net/tv",1,"http://www.tenorvossa.co.uk/Images/TV%20Logo%20Crop.jpg")
        addDir("4. COMEDY","http://tvshack.net/comedy",1,"http://assets.hulu.com/companies/key_art_comedy_time.jpg")
        addDir("5. DOCUMENTARIES","http://tvshack.net/documentaries",1,"http://www.britishcouncil.org/arts-film-255x256-documentaries.jpg")
        addDir("6. MUSIC","http://tvshack.net/music",1,"http://www.britishcouncil.org/arts-music-graphic")
        addDir("7. SEARCH TV SHACK","http://tvshack.net/search/",6,"http://www.searchengineoptimizationcompany.ca/img/Search-Engine-Marketing.jpg")

def INDEX(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        clean=re.sub('&eacute;','ea',link)
        clean2=re.sub('&amp;','&',clean)
        clean3=re.sub('&quot;','',clean2)
        clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
        clean5=re.sub('<font class="new-updated">Updated!</font>','',clean4);clean6=re.sub('<font class="new-new">New!</font>','',clean5)
        match=re.compile('<li><a href="(.+?)">(.+?)<span>').findall(clean6)
        for url,name in match:
                if url.find('/movies/')>0:
                        addDir(name,url,2,"")
                if url.find('/documentaries/')>0:
                        addDir(name,url,3,"")
                if url.find('/anime/')>0:
                        addDir(name,url,4,"")
                if url.find('/comedy/')>0:
                        addDir(name,url,3,"")
                if url.find('/music/')>0:
                        addDir(name,url,4,"")
                if url.find('/tv/')>0:
                        addDir(name,url,4,"")
                

def ALTERNATE(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req);link=response.read();response.close()
        clean=re.sub('&eacute;','ea',link);clean2=re.sub('&amp;','&',clean)
        clean3=re.sub('&quot;','',clean2);clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
        alt=re.compile('<h3>Alternate links</h3>\n(.+?)\n</ul>').findall(clean4)
        altlink=re.compile('<li><a href="(.+?)"><img src="(.+?)" />').findall(str(alt))
        for url,thumb in altlink:
                addDir(name,url,3,thumb)

def PART(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req);link=response.read();response.close()
        clean=re.sub('&eacute;','ea',link);clean2=re.sub('&amp;','&',clean)
        clean3=re.sub('&quot;','',clean2);clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
        partpage=re.compile('NewWindow2."(.+?)","video",650,470.').findall(clean4)
        req = urllib2.Request(partpage[0])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        page = urllib2.urlopen(req);response=page.read();page.close()
        clean=re.sub(' style="color:#e3e3e3;background-color:#676767;"','',response)
        parturl=re.compile('<li>Select a part</li>\n(.+?)\n</div>').findall(clean)
        parts=re.compile('<li><a href="(.+?)">(.+?)</a>').findall(str(parturl))
        if len(parts)<2:
                addDir(name,url,5,'')
        else:
                for url,pnumb in parts:
                        addDir(name+' Part-'+pnumb,url,5,'')

def EPS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req);link=response.read();response.close()
        clean=re.sub('&eacute;','ea',link);clean2=re.sub('&amp;','&',clean)
        clean3=re.sub('&quot;','',clean2);clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
        match=re.compile('<li><a href="(.+?)">(.+?)</a><a href=""><span>.+?</span></a>').findall(clean4)
        if len(match)<1:
                match=re.compile('<a href="(.+?)">(.+?)<span>').findall(clean4)
        for url,name in match:
                season=re.compile('http://tvshack.net/.+?/.+?/(.+?)/episode_.+?/').findall(url)
                try:
                        addDir(season[0]+' - '+name,url,3,'')
                except:
                        addDir(name,url,3,'')
def SEARCH():
        keyb = xbmc.Keyboard('', 'Search TV Shack')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                req = urllib2.Request('http://tvshack.net/search/'+encode)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                clean=re.sub('&eacute;','ea',link)
                clean2=re.sub('&amp;','&',clean)
                clean3=re.sub('&quot;','',clean2)
                clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
                clean5=re.sub('<font class="new-updated">Updated!</font>','',clean4);clean6=re.sub('<font class="new-new">New!</font>','',clean5)
                match=re.compile('<li><a href="(.+?)">.+?<strong>(.+?)</strong></a>').findall(clean6)
                for url,name in match:
                        if url.find('/movies/')>0:
                                addDir(name,url,2,"")
                        if url.find('/documentaries/')>0:
                                addDir(name,url,3,"")
                        if url.find('/anime/')>0:
                                addDir(name,url,4,"")
                        if url.find('/comedy/')>0:
                                addDir(name,url,3,"")
                        if url.find('/music/')>0:
                                addDir(name,url,4,"")
                        if url.find('/tv/')>0:
                                addDir(name,url,4,"")


def IMDB(url):
    req = urllib2.Request('http://www.imdb.com/find?s=all&q='+urllib.quote(url))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    response = urllib2.urlopen(req).read()
    alt=re.compile('<b>Media from&nbsp;<a href="/title/(.+?)/">').findall(response)
    if len(alt)>0:
        req = urllib2.Request('http://imdb.com/title/'+alt[0])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        genre=re.compile(r'<h5>Genre:</h5>\n<a href=".+?">(.+?)</a>').findall(response)
        year=re.compile(r'<a href="/Sections/Years/.+?/">(.+?)</a>').findall(response)
        image=re.compile(r'<img border="0" alt=".+?" title=".+?" src="(.+?)" /></a>').findall(response)
        rating=re.compile(r'<div class="meta">\n<b>(.+?)</b>').findall(response)
        req = urllib2.Request('http://www.imdb.com/title/'+alt[0]+'/plotsummary')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        plot=re.compile('<p class="plotpar">\n(.+?)\n<i>\n').findall(response)
        try:
            if plot[0].find('div')==1:
                plot[0]='No Plot found on Imdb'
        except IndexError: pass
        if len(plot)<1:
            req = urllib2.Request('http://www.imdb.com/title/'+alt[0]+'/synopsis')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            plotter = urllib2.urlopen(req).read();clean=re.sub('\n','',plotter)
            plot=re.compile('<div id="swiki.2.1">(.+?)</div>').findall(clean)
            try:
                if plot[0].find('div')>0:
                    plot[0]='No Plot found on Imdb'
            except IndexError: pass
                
        return genre[0],int(year[0]),image[0],rating[0],plot[0]
    else :
        genre=re.compile(r'<h5>Genre:</h5>\n<a href=".+?">(.+?)</a>').findall(response)
        year=re.compile(r'<a href="/Sections/Years/.+?/">(.+?)</a>').findall(response)
        image=re.compile(r'<img border="0" alt=".+?" title=".+?" src="(.+?)" /></a>').findall(response)
        rating=re.compile(r'<div class="meta">\n<b>(.+?)</b>').findall(response)
        bit=re.compile(r'<a class="tn15more inline" href="/title/(.+?)/plotsummary" onClick=".+?">.+?</a>').findall(response)
        if len(bit)<1:
            bit=re.compile(r'<a name="poster" href="/.+?/.+?/.+?-photo/media/.+?/(.+?)" title=".+?">').findall(response)
        req = urllib2.Request('http://www.imdb.com/title/'+bit[0]+'/plotsummary')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        plot=re.compile('<p class="plotpar">\n(.+?)\n<i>\n').findall(response)
        try:
            if plot[0].find('div')>0:
                plot[0]='No Plot found on Imdb'
        except IndexError: pass
        if len(plot)<1:
            req = urllib2.Request('http://www.imdb.com/title/'+bit[0]+'/synopsis')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            plotter = urllib2.urlopen(req).read();clean=re.sub('\n','',plotter)
            plot=re.compile('<div id="swiki.2.1">(.+?)</div>').findall(clean)
            try:
                if plot[0].find('div')>0:
                    plot[0]='No Plot found on Imdb'
            except IndexError: pass
        return genre[0],year[0],image[0],rating[0],plot[0]	
                        
                       

#####Megavideo - Coolblaze xbc forums.
                                
def ajoin(arr):
    strtest = ''
    for num in range(len(arr)):
        strtest = strtest + str(arr[num])
    return strtest

def asplit(mystring):
    arr = []
    for num in range(len(mystring)):
        arr.append(mystring[num])
    return arr
        
def decrypt(str1, key1, key2):

    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        if (holder == "0"):
            __reg1.append("0000")
        else:
            if (__reg0 == "1"):
                __reg1.append("0001")
            else:
                if (__reg0 == "2"): 
                    __reg1.append("0010")
                else: 
                    if (__reg0 == "3"):
                        __reg1.append("0011")
                    else: 
                        if (__reg0 == "4"):
                            __reg1.append("0100")
                        else: 
                            if (__reg0 == "5"):
                                __reg1.append("0101")
                            else: 
                                if (__reg0 == "6"):
                                    __reg1.append("0110")
                                else: 
                                    if (__reg0 == "7"):
                                        __reg1.append("0111")
                                    else: 
                                        if (__reg0 == "8"):
                                            __reg1.append("1000")
                                        else: 
                                            if (__reg0 == "9"):
                                                __reg1.append("1001")
                                            else: 
                                                if (__reg0 == "a"):
                                                    __reg1.append("1010")
                                                else: 
                                                    if (__reg0 == "b"):
                                                        __reg1.append("1011")
                                                    else: 
                                                        if (__reg0 == "c"):
                                                            __reg1.append("1100")
                                                        else: 
                                                            if (__reg0 == "d"):
                                                                __reg1.append("1101")
                                                            else: 
                                                                if (__reg0 == "e"):
                                                                    __reg1.append("1110")
                                                                else: 
                                                                    if (__reg0 == "f"):
                                                                        __reg1.append("1111")

        __reg3 = __reg3 + 1

    mtstr = ajoin(__reg1)
    __reg1 = asplit(mtstr)
    __reg6 = []
    __reg3 = 0
    while (__reg3 < 384):
    
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        __reg6.append((int(key1) + int(key2)) % 128)
        __reg3 = __reg3 + 1
    
    __reg3 = 256
    while (__reg3 >= 0):

        __reg5 = __reg6[__reg3]
        __reg4 = __reg3 % 128
        __reg8 = __reg1[__reg5]
        __reg1[__reg5] = __reg1[__reg4]
        __reg1[__reg4] = __reg8
        __reg3 = __reg3 - 1
    
    __reg3 = 0
    while (__reg3 < 128):
    
        __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
        __reg3 = __reg3 + 1

    __reg12 = ajoin(__reg1)
    __reg7 = []
    __reg3 = 0
    while (__reg3 < len(__reg12)):

        __reg9 = __reg12[__reg3:__reg3 + 4]
        __reg7.append(__reg9)
        __reg3 = __reg3 + 4
        
    
    __reg2 = []
    __reg3 = 0
    while (__reg3 < len(__reg7)):
        __reg0 = __reg7[__reg3]
        holder2 = __reg0
    
        if (holder2 == "0000"):
            __reg2.append("0")
        else: 
            if (__reg0 == "0001"):
                __reg2.append("1")
            else: 
                if (__reg0 == "0010"):
                    __reg2.append("2")
                else: 
                    if (__reg0 == "0011"):
                        __reg2.append("3")
                    else: 
                        if (__reg0 == "0100"):
                            __reg2.append("4")
                        else: 
                            if (__reg0 == "0101"): 
                                __reg2.append("5")
                            else: 
                                if (__reg0 == "0110"): 
                                    __reg2.append("6")
                                else: 
                                    if (__reg0 == "0111"): 
                                        __reg2.append("7")
                                    else: 
                                        if (__reg0 == "1000"): 
                                            __reg2.append("8")
                                        else: 
                                            if (__reg0 == "1001"): 
                                                __reg2.append("9")
                                            else: 
                                                if (__reg0 == "1010"): 
                                                    __reg2.append("a")
                                                else: 
                                                    if (__reg0 == "1011"): 
                                                        __reg2.append("b")
                                                    else: 
                                                        if (__reg0 == "1100"): 
                                                            __reg2.append("c")
                                                        else: 
                                                            if (__reg0 == "1101"): 
                                                                __reg2.append("d")
                                                            else: 
                                                                if (__reg0 == "1110"): 
                                                                    __reg2.append("e")
                                                                else: 
                                                                    if (__reg0 == "1111"): 
                                                                        __reg2.append("f")
                                                                    
        __reg3 = __reg3 + 1

    endstr = ajoin(__reg2)
    return endstr

#########
def DAP(url):
    name=url.split('/')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    response = urllib2.urlopen(req)
    size=int(response.info().get('Content-Length'));split=size/3
    p1='bytes=0-'+str(split)
    p2='bytes='+str((split+1))+'-'+str((split*2))
    p3='bytes='+str((split*2+1))+'-'+str(size)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Range',p1)
    response1 = urllib2.urlopen(req)
    buf1=response.read()
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Range',p2)
    response2 = urllib2.urlopen(req)
    buf2=response.read()
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Range',p3)
    response3 = urllib2.urlopen(req)
    buf3=response.read()
    print time.asctime(),'Downloading: bytes= %s of %s' % (str(len(buf1)), str(size))
    fileout=open('X:/'+name[-1],'wb')
    fileout.write(buf1)
    if len (buf1)>=split-1:
        buf1=buf1+buf2
    if len(buf1)>=split*2-1:
        buf1=buf1+buf3
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(fileout.truncate(size))
    if len(buf1)>=size:
        response1.close()
        response2.close()
        response3.close()
        fileout.flush()
        fileout.close()

                                
def VIDLINK(url,name):
        try:
                info=IMDB(name)
        except:
                info=['','0','','','']
                
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req);link=response.read();response.close()
        clean=re.sub('&eacute;','ea',link);clean2=re.sub('&amp;','&',clean)
        clean3=re.sub('&quot;','',clean2);clean4=re.sub('&nbsp;<font class=".+?">.+?</font>','',clean3)
        partpage=re.compile('NewWindow2."(.+?)","video",650,470.').findall(clean4)
        try:
                req = urllib2.Request(partpage[0])
        except: pass
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        page = urllib2.urlopen(req);response=page.read();page.close()
        try:
                tweety=re.compile('flashvars="file=(.+?)&type=flv').findall(response)
                addLink(name,tweety[0],'',info)
                
        except IndexError:
                try:
                        i=0
                        bit=re.compile('<iframe src="(.+?)"').findall(response)
                        req = urllib2.Request(bit[0])
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        page = urllib2.urlopen(req);response=page.read();page.close()
                        Id=re.compile("'VideoIDS','(.+?)'").findall(response)
                        youku="http://www.flvcd.com/parse.php?kw=http%3A%2F%2Fv.youku.com%2Fv_show%2Fid_"+Id[0]+"%3D%3D.html"
                        req = urllib2.Request(youku)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        page = urllib2.urlopen(req);response=page.read();page.close()
                        match=re.compile('<a href="(.+?)" target="_blank" onclick=".+?">').findall(response)
                        for url in match:
                                i=i+1
                                addLink(name+" Part -"+str(i),url,'',info)
                except IndexError:
                        try:
                                mega=re.compile('<param name="movie" value="http://www.megavideo.com/v/(.+?)">').findall(response)
                                mega[0] = mega[0][0:8]
                                req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+mega[0])
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                req.add_header('Referer', 'http://www.megavideo.com/')
                                page = urllib2.urlopen(req);response=page.read();page.close()
                                errort = re.compile(' errortext="(.+?)"').findall(response)
                                if len(errort) > 0:
                                        addLink(errort[0], '', '')
                                else:
                                        s = re.compile(' s="(.+?)"').findall(response)
                                        k1 = re.compile(' k1="(.+?)"').findall(response)
                                        k2 = re.compile(' k2="(.+?)"').findall(response)
                                        un = re.compile(' un="(.+?)"').findall(response)
                                        movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/"
                                        info = ['','','','','','','','','']
                                        addLink(name, movielink+'?.flv','',info)
                        
                        
                        except IndexError: pass

       
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
def addLink(name,url,thumbnail,info):
        ok=True
        
        def Download(url,dest):
                dp = xbmcgui.DialogProgress()
                dp.create("Tv-shack Download","Downloading File",url)
                urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
                try:
                        percent = min((numblocks*blocksize*100)/filesize, 100)
                        print percent
                        dp.update(percent)
                except:
                        percent = 100
                        dp.update(percent)
                if dp.iscanceled():
                        dp.close()
        if xbmcplugin.getSetting("Download Flv") == "true":
                dialog = xbmcgui.Dialog()
                path = dialog.browse(3, 'Choose Download Directory', 'files', '', False, False, '')
                Download(url,path+name+'.flv')
        try:
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=info[2])
                liz.setInfo( type="Video", infoLabels={ "Title": name , "Genre": info[0], "Year": int(info[1]), "Plot": info[4]} )
        except:
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='http://ia.media-imdb.com/media/imdb/01/I/27/89/15/10.gif')
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,thumbnail):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
                                                                    
params=get_params()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
        print "categories"
        CATS()
elif mode==1:
        print "INDEX OF LINKS : "+url
        INDEX(url,name)
elif mode==2:
        print "ALTERNATE VIDEO SOURCES: "+url
        ALTERNATE(url,name)
elif mode==3:
        print "PARTS OF VIDEO: "+url
        PART(url,name)
elif mode==4:
        print "EPISODES : "+url
        EPS(url,name)
elif mode==5:
        print "VIDLINKS : "+url
        VIDLINK(url,name)
elif mode==6:
        print "SEARCH  :"+url
        SEARCH()
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
