import urllib,urllib2,re,xbmcplugin,xbmcgui

def INDEX():
        req = urllib2.Request('http://www.instantz.net')
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        eps=re.compile(r'<a style="font-weight:lighter;font-size:11px;" class="navigation" href="(.+?)">(.+?)</a><br>').findall(response)
        for url,name in eps:
                addDir(name,url,1,"")
def IPOD(url):
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit?/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3')
                ipod = urllib2.urlopen(req)
                addLink('Full unrestricted mp4',ipod.url,'')
        except:
                addLink('Video not available in mp4 format','http://novid.com','')
        
def VIDS(url):        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        req.add_header('Content-Type','application/xml')
        response = urllib2.urlopen(req).read()
        perma=re.compile(r'<a href="http://www.veoh.com/fullscreen_single2.+?permalinkId=(.+?)&videoAutoPlay=.+?&selected.+?">(.+?)</a><br>').findall(response)
        for url,name in perma:
                addDir(name,url,2,"")

def VIDEO(url,name):
        req = urllib2.Request('http://www.veoh.com/rest/v2/execute.xml?method=veoh.video.findByPermalink&permalink=%s&apiKey=5697781E-1C60-663B-FFD8-9B49D2B56D36'%url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        flash=re.compile('fullPreviewHashPath="(.+?)"').findall(response)
        ipod=re.compile('ipodUrl="(.+?)"').findall(response)
        if flash: addLink(name,flash[0],"")
        if ipod: addDir(name+' -Mp4 Full',ipod[0],3,"")
                
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
        liz.setInfo( type="Video", infoLabels={"Title": name})
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
        INDEX()
        
elif mode==1:
        print "GET INDEX OF PAGE : "+url
        VIDS(url)
elif mode==2:
        print "GET INDEX OF PAGE : "+url
        VIDEO(url,name)
elif mode==3:
        print "GET INDEX OF PAGE : "+url
        IPOD(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
