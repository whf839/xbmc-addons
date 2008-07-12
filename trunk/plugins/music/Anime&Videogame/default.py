import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

#Thumbnail holder
Thumb=[]
                               

def getmp3index(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a href="(.+?)">(.+?)</a><br>')
        match=p.findall(link)                
        for url,name in match:
                res.append((url,name))
        return res

def getmp3list(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\r\n\t<tr>\r\n\t\t<td><a href="(.+?)">(.+?)</a></td>\r\n')
        match=p.findall(link)                
        for url,name in match:
                res.append((url,name))
        #Get thumb
        p=re.compile('<img src="(.+?)" border="0"></a>')
        match=p.findall(link)
        if len(match)>0:
                tb=match[0]
                Thumb.append(tb)
        else:
                tb="http://thumbs.dreamstime.com/thumb_42/1140841917tAa9Gn.jpg"
                Thumb.append(tb)
        return res

def getmp3(url):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a style="color: .+?" href="(.+?)">')
        match=p.findall(link)
        res.append(match[1])
        return res



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
	
def addLink(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,thumbnail):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def Folder():
        addDir("ANIME & VIDEOGAME MP3'S","http://downloads.khinsider.com/game-soundtracks/browse/all",1,"")

def showmp3index(url,name):
        tracks=getmp3index(url,name)
        for url,name in tracks:
                addDir(name,url,2,"")

def showmp3list(url,name):
        egg=getmp3list(url,name)
        for url,name in egg:
                addDir(name,url,3,Thumb[0])

def showmp3link(url):
        mp3link=getmp3(url)
        for mp3 in mp3link:
                addLink("PLAY TRACK",mp3)

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
	print "Start Folder  :"
	Folder()
elif mode==1:
        print "Index of Mp3's  : "+url
        showmp3index(url,name)
elif mode==2:
        print "List of Mp3's  :"+url+" - "+name
        showmp3list(url,name)
elif mode==3:
        print "Final resolved Mp3   :"+url
        showmp3link(url)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
