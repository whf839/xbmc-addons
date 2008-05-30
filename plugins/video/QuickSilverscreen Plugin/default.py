import urllib,urllib2,re,xbmcplugin,xbmcgui

#QUICKSILVERSCREEN 2008. - VOINAGE

def INDEXCATS():
        addDir("1. ANIME","http://quicksilverscreen.com/videos?c=3",3,"")
        addDir("2. TV-SHOWS","http://quicksilverscreen.com/videos?c=1",3,"")
        addDir( "3. MOVIES ","http://quicksilverscreen.com/videos?c=2&pt=thumbs",1,"")
        addDir("9. FOREIGN MOVIES","http://quicksilverscreen.com/videos?c=715",1,"")
        addDir( "4. CARTOONS","http://quicksilverscreen.com/videos?c=112",3,"")
        addDir("5. DOCUMENTARIES","http://quicksilverscreen.com/videos?c=44",1,"")
        addDir("6. MUSIC VIDEOS","http://quicksilverscreen.com/videos?c=30",1,"")
        addDir("7. STAND-UP COMEDY","http://quicksilverscreen.com/videos?c=137",1,"")
        addDir("8. BOLLYWOOD","http://quicksilverscreen.com/videos?c=142",1,"")
        addDir("10. SPORT","http://quicksilverscreen.com/videos?c=207&pt=thumbs",1,"")
        
        

        
def INDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        clean=re.sub('&quot;','',link)
        clean1=re.sub('&amp;','',clean)
        response.close()
        p=re.compile('<a href="(.+?)"><img src="(.+?)" width="214" height="120"></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t          </tr>\n\t\t\t          <tr> \n\t\t\t            <td width="17px" valign="bottom" bgcolor="#E2E2E2"><img src="http://static.quicksilverscreen.com/v3/elements/index_descript_bg_l.gif" width="17" height="35"></td>\n\n\t\t\t            <td width="182px" valign="top" bgcolor="#E2E2E2"> \n\t\t\t\t\t\t\t<div style="padding:3px;word-wrap:break-word;">\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<a href=".+?"><small>.+?</small>(.+?)</a>')
        match=p.findall(clean1)
        for url,thumbnail,name in match:
                vidlink="http://quicksilverscreen.com/"+url
                res.append((vidlink,thumbnail,name))
        p=re.compile('<a href="(.+?)"><img src="(.+?)\r\n\t" width="214" height="120"></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t          </tr>\n\t\t\t          <tr> \n\t\t\t            <td width="17px" valign="bottom" bgcolor="#E2E2E2"><img src="http://static.quicksilverscreen.com/v3/elements/index_descript_bg_l.gif" width="17" height="35"></td>\n\n\t\t\t            <td width="182px" valign="top" bgcolor="#E2E2E2"> \n\t\t\t\t\t\t\t<div style="padding:3px;word-wrap:break-word;">\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<a href=".+?"><small>.+?</small>(.+?)</a>')
        match2=p.findall(clean1)
        for url,thumbnail,name in match2:
                vidlink="http://quicksilverscreen.com/"+url
                res.append((vidlink,thumbnail,name))
        for vidlink,thumbnail,name in res:
                addDir(name,vidlink,2,thumbnail)
                    
        p=re.compile('<li class="nextpage"><a rel="nofollow" href="(.+?)">>></a></li>')
        page=p.findall(clean1)
        try:
                next="http://quicksilverscreen.com/"+page[0]
                addDir("    NEXT PAGE   ",next,1,"")
        except IndexError:
                try:
                        addDir(name,vidlink,2,thumbnail)
                except UnboundLocalError:
                        addDir("QUICKSILVERSCREEN HAS NO FILES IN THIS FOLDER","","","")
def INDEX2(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        CLEAN=re.sub('&amp;','',link)
        p=re.compile('<a href="(.+?)">(.+?)</a><br/>')
        match=p.findall(CLEAN)
        match=match[:-25]
        for bit,name in match:
                url2="http://quicksilverscreen.com/"+bit
                addDir(name,url2,1,"")
                
                

def ExtractMediaUrl(url, data):
        
        if url.find("megavideo.com") > 0:
                codeRegex = '<ROW url="(.+?)" runtime=".+?" runtimehms=".+?" size=".+?" waitingtime=".+?" k=".+?"></ROW>'
                codeResults = re.findall(codeRegex, data, re.DOTALL + re.IGNORECASE)
                if len(codeResults) > 0:
                        code = codeResults[-1]
                        dictionary = {"0":":","%24": ".", "%25": "/", "%3A": "0", "%3B": "1", "8": "2", "9": "3", "%3E": "4", "%3F": "5", "%3C": "6", "%3D": "7", "2": "8", "3": "9", "a": "k", "b": "h", "c": "i", "d": "n", "e": "o", "f": "l", "g": "m", "h": "b", "i": "c", "k": "a", "l": "f", "m": "g", "n": "d", "o": "e", "p": "z", "s": "y", "%7E": "t", "y": "s","%7C": "v", "%7D": "w", "z": "p"}
                        return RegexReplaceDictionary(code, dictionary) 
                else:
                        return ""
        
def RegexReplaceDictionary(string, dictionary):
      
        rc = re.compile('|'.join(map(re.escape, dictionary)))
        def Translate(match):
                return dictionary[match.group(0)]
        return rc.sub(Translate, string)
 
def VIDEOLINKS(url,name):
        
        #VEOH
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\n\t\t\t\t<embed src=".+?permalinkId=(.+?)&id=anonymous')
        match=p.findall(link)
        for VEOH in match:
                url='http://127.0.0.1:64652/'+VEOH
                addLink("WATCH VEOH HIGH QUALITY",url,"")
                
        #MEGAVIDEO
        p=re.compile('<param name="movie" value="(.+?)">')
        match=p.findall(link)
        for a in match:
                if len(a)<79:
                        a=a[:-43]
                        code=re.sub('http://www.megavideo.com/v/','v=',a)
                        url="http://www.megavideo.com/xml/videolink.php?"+code
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        new=ExtractMediaUrl(url,link)
                        flvappend="voinage.flv"
                        flvlink=new+flvappend
                        addLink("WATCH MEGAVIDEO",flvlink,"")
                        
                
                elif len(a)<80:
                                a=a[:-44]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
                                
                                        
                                
                elif len(a)<81:
                                a=a[:-45]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
                                
        #YOUKU
        p=re.compile('<embed src="http://player.youku.com/player.php/sid/(.+?)/v.swf"')
        YOUKU=p.findall(link)
        DECODE='http://clipnabber.com/gethint.php'
        try:
                YOUKU2='http://v.youku.com/v_show/id_'+YOUKU[0]+'=.html'
                data = "mode=1&url="+YOUKU2
                req = urllib2.Request(DECODE,data)
                response = urllib2.urlopen(req)
                results = response.read()
                p=re.compile('<a href=(.+?)><strong>(.+?)</strong></a>&nbsp;&nbsp;&nbsp;')
                final=p.findall(results)
                for url,name in final:
                        addLink("WATCH YOUKU - "+name,url,"")
        except IndexError:
                pass
        
                
        #GOOGLE
        p=re.compile('\n\t\t\t\t\t<a rel="nofollow" target="_blank" href=".+?docId=(.+?)">fullscreen</a>')
        GOOGLE=p.findall(link)
        DECODE='http://clipnabber.com/gethint.php'
        try:
                GOOGLE2='http://video.google.com/videoplay?docid='+GOOGLE[0]
                data = "mode=1&url="+GOOGLE2
                req = urllib2.Request(DECODE,data)
                response = urllib2.urlopen(req)
                results = response.read()
                p=re.compile('<a href=\'(.+?)\' >')
                final=p.findall(results)
                for url in final:
                        addLink("WATCH GOOGLE HIGH QUALITY",url,"")
        except IndexError:
                pass
        
                
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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
        print "CATEGORY INDEX : "
        INDEXCATS()
elif mode==1:
        print "GET INDEX OF PAGE : "+url
        INDEX(url,name)
elif mode==2:
        print "GET VIDEO LINK: "+url
        VIDEOLINKS(url,name)
elif mode==3:
        print "GET TV INDEX: "+url
        INDEX2(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
