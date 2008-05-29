import urllib,urllib2,re,xbmcplugin,xbmcgui
#MEGAVIDEO PLUGIN FOR XBMC 2008.#
#IF YOU`RE SEEING THIS YOU ARE A PYTHON ENTHUSIAST - GET INVOLVED !#

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

def INDEXCATS():
        addDir("1. ARTS & ANIMATION","http://www.megavideo.com/?c=categories&s=1",1,"http://www.megavideo.com/mvthumbs/ico_art.gif")
        addDir( "2. AUTO'S & VEHICLES","http://www.megavideo.com/?c=categories&s=2",1,"http://www.megavideo.com/mvthumbs/ico_autos.gif")
        addDir( "3. COMEDY","http://www.megavideo.com/?c=categories&s=23",1,"http://www.megavideo.com/mvthumbs/ico_comedy.gif")
        addDir("6. ENTERTAINMENT","http://www.megavideo.com/?c=categories&s=24",1,"http://www.megavideo.com/mvthumbs/ico_entertainment.gif")
        addDir( "5. MUSIC","http://www.megavideo.com/?c=categories&s=10",1,"http://www.megavideo.com/mvthumbs/ico_music.gif")
        addDir( "7. NEWS & BLOGS","http://www.megavideo.com/?c=categories&s=25",1,"http://www.megavideo.com/mvthumbs/ico_news.gif")
        addDir( "8. PEOPLE","http://www.megavideo.com/?c=categories&s=22",1,"http://www.megavideo.com/mvthumbs/ico_people.gif")
        addDir( "4. PETS & ANIMALS","http://www.megavideo.com/?c=categories&s=15",1,"http://www.megavideo.com/mvthumbs/ico_pets.gif")
        addDir( "9. SCIENCE & TECHNOLOGY","http://www.megavideo.com/?c=categories&s=26",1,"http://www.megavideo.com/mvthumbs/ico_science.gif")
        addDir( "10. SPORTS","http://www.megavideo.com/?c=categories&s=17",1,"http://www.megavideo.com/mvthumbs/ico_sport.gif")
        addDir( "11. TRAVEL & PLACES","http://www.megavideo.com/?c=categories&s=19",1,"http://www.megavideo.com/mvthumbs/ico_travel.gif")
        addDir( "12. VIDEO GAMES","http://www.megavideo.com/?c=categories&s=20",1,"http://www.megavideo.com/mvthumbs/ico_games.gif")
        addDir( "13. SEARCH MEGAVIDEO","www.megavideo.com",3,"http://www.hull.ac.uk/incofish/images/DataSearch.jpg")


def INDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<div style=".+?"><a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?" border=".+?"></a></div>\n\n\n\t\t\t<div style=".+?"><a href=".+?" style=".+?">(.+?)</a></div>\n\t\t\t<div style=".+?"><font color=".+?">Added:</font>.+?</div>\n\t\t\t<div style=".+?"><font color=".+?">By:</font> <a href=".+?" style=".+?">.+?</a></div>\n\t\t\t<div style=".+?"><font color=".+?">.+?</font>(.+?)</div>\n\t\t\t')
        match=p.findall(link)
        for url,thumbnail,name,runtime in match:
                runtime="  RUN TIME: "+runtime
                url2="http://www.megavideo.com/xml/videolink.php"+url
                addDir(name+runtime,url2,2,thumbnail)
        p=re.compile('<TD width=".+?" align="right"><a href="(.+?)" accesskey=".+?" style=".+?">.+?</a></TD>')
        page=p.findall(link)
        addDir("   NEXT PAGE   ","http://www.megavideo.com/"+page[0],1,"http://www.nicolasart.com/images/Right%20Arrow.png")

def INDEX2(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        p=re.compile('<div style=".+?"><a href="(.+?)"><IMG src="(.+?)" width=".+?" height=".+?" border=".+?"></div></div>\n\n\t\t\t</div>\n\t\t\t\n\t\t\t</TD>\n\t\t\t<TD valign=".+?" width=".+?" style=".+?">\n\n\t\t\t<div style=".+?"><a href=".+?" style=".+?">(.+?)</a></div>\n\t\t\t\n\t\t\t<div class=".+?" id=".+?">\n\t\t\t.+?\t\t\t</div>\n\n\t\t\t<div class=".+?" style=".+?" id=".+?">\n\t\t\t.+?\t\t\t</div>\n\n\n\n\t\t\t<div style=".+?"><b>.+?</b>.+?<font style=".+?">(.+?)</font></div>')
        match=p.findall(link)
        for url,thumbnail,name,runtime in match:
                runtime="  RUN TIME: "+runtime
                url2="http://www.megavideo.com/xml/videolink.php"+url
                addDir(name+runtime,url2,2,thumbnail)
        p=re.compile('<TD width=".+?" align="right"><a href="(.+?)" accesskey=".+?" style=".+?">.+?</a></TD>')
        page=p.findall(link)
        addDir("   NEXT PAGE   ","http://www.megavideo.com/"+page[0],4,"http://www.nicolasart.com/images/Right%20Arrow.png")
        

def MEGAVIDEOLINKS(url):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        new=ExtractMediaUrl(url,link)
        flvappend="voinage.flv"
        flvlink=new+flvappend
        addLink("WATCH VIDEO",flvlink,"")

def SEARCH():
        res=[]
        keyb = xbmc.Keyboard('', 'SEARCH MEGAVIDEO')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                CODE=re.sub(' ','%20',search)
                req = urllib2.Request('http://www.megavideo.com/?c=search&s='+CODE)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('<div style=".+?"><a href="(.+?)"><IMG src="(.+?)" width=".+?" height=".+?" border=".+?"></div></div>\n\n\t\t\t</div>\n\t\t\t\n\t\t\t</TD>\n\t\t\t<TD valign=".+?" width=".+?" style=".+?">\n\n\t\t\t<div style=".+?"><a href=".+?" style=".+?">(.+?)</a></div>\n\t\t\t\n\t\t\t<div class=".+?" id=".+?">\n\t\t\t.+?\t\t\t</div>\n\n\t\t\t<div class=".+?" style=".+?" id=".+?">\n\t\t\t.+?\t\t\t</div>\n\n\n\n\t\t\t<div style=".+?"><b>.+?</b>.+?<font style=".+?">(.+?)</font></div>')
                match=p.findall(link)
                for url,thumbnail,name,runtime in match:
                        runtime="  RUN TIME: "+runtime
                        url2="http://www.megavideo.com/xml/videolink.php"+url
                        addDir(name+runtime,url2,2,thumbnail)
        p=re.compile('<TD width=".+?" align="right"><a href="(.+?)" accesskey=".+?" style=".+?">.+?</a></TD>')
        page=p.findall(link)
        try:
                addDir("   NEXT PAGE   ","http://www.megavideo.com/"+page[0],4,"http://www.nicolasart.com/images/Right%20Arrow.png")
        except IndexError:
                addDir(name+runtime,url2,2,thumbnail)
         


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
        print "GENERAL INDEX : "+url
        INDEX(url,name)
elif mode==2:
        print "GET MEGAVIDEOLINKS : "+url
        MEGAVIDEOLINKS(url)
elif mode==3:
        print "SEARCH MEGAVIDEO : "+url
        SEARCH()
elif mode==4:
        print "SEARCH MEGAVIDEO : "+url
        INDEX2(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
