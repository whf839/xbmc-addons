import urllib,urllib2,re,xbmcplugin,xbmcgui
#ALTERTUBE PLUGIN FOR XBMC 2008.#REQ: XBMCFORUMS.
#IF YOU`RE SEEING THIS YOU ARE A PYTHON ENTHUSIAST - GET INVOLVED !#

def INDEXCATS():
        addDir("1. VIDEOS","http://www.altertube.tv/channel_detail.php?chid=1",1,"http://www.altertube.tv/chimg/1.jpg")
        addDir( "2. MUSIC VIDEOS","http://www.altertube.tv/channel_detail.php?chid=2",1,"http://www.altertube.tv/chimg/2.jpg")
        addDir( "3. SHORT FILMS","http://www.altertube.tv/channel_detail.php?chid=3",1,"http://www.altertube.tv/chimg/3.jpg")
        addDir("4. FILM CLIPS","http://www.altertube.tv/channel_detail.php?chid=4",1,"http://www.altertube.tv/chimg/4.jpg")
        #addDir( "5. SEARCH","",3,"")
        

def INDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<IMG style="BORDER-RIGHT: #ffffff 5px solid; BORDER-TOP: #ffffff 5px solid; MARGIN-TOP: 10px; BORDER-LEFT: #ffffff\n\t\t\t\t5px solid; BORDER-BOTTOM: #ffffff 5px solid" height=60 src="(.+?)" width=80>\n\t\t\t</A>\n\n\t\t\t<DIV class=moduleEntrySpecifics style="FONT-WEIGHT: bold; PADDING-TOP: 5px">\n\n\t\t\t\t<A href="(.+?)">(.+?)</A>\n\t\t\t</DIV>')
        match=p.findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,2,thumbnail)
        p=re.compile(" <b><a href=\'(.+?)\'>next</a><b></div>\n\n")
        page=p.findall(link)
        url="http://www.altertube.tv/"+page[0]
        addDir("     NEXT PAGE   ",url,1,"")
                
        

def VIDEOLINKS(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('file=(.+?)&amp;autostart')
        match=p.findall(link)
        for url in match:
                addLink("WATCH VIDEO",url,"")

def SEARCH():
        res=[]
        keyb = xbmc.Keyboard('', 'SEARCH ALTERTUBE')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                req = urllib2.Request(''+encode+'')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('<IMG style="BORDER-RIGHT: #ffffff 5px solid; BORDER-TOP: #ffffff 5px solid; MARGIN-TOP: 10px; BORDER-LEFT: #ffffff\n\t\t\t\t5px solid; BORDER-BOTTOM: #ffffff 5px solid" height=60 src="(.+?)" width=80>\n\t\t\t</A>\n\n\t\t\t<DIV class=moduleEntrySpecifics style="FONT-WEIGHT: bold; PADDING-TOP: 5px">\n\n\t\t\t\t<A href="(.+?)">(.+?)</A>\n\t\t\t</DIV>')
                match=p.findall(link)
                for thumbnail,url,name in match:
                        addDir(name,url,2,thumbnail)
        p=re.compile(" <b><a href=\'(.+?)\'>next</a><b></div>\n\n")
        page=p.findall(link)
        if len(page)>0:
                url="http://www.altertube.tv/"+page[0]
                addDir("     NEXT PAGE   ",url,1,"")
        else:
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
        print " SEARCH STRING " +url
        SEARCH()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
