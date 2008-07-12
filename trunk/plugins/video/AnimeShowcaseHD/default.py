import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

#ANIMESHOWCASE-HD - By Voinage 2008.

main="http://www.animeshowcase.net/videos/"

def INDEX(main):
        res=[]
        req = urllib2.Request(main)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('..&gt;','e.wmv',link)
        response.close()
        p=re.compile('<A HREF="(.+?)">(.+?)/</A>')
        match=p.findall(code)
        if len(match)>0:
                for url,name in match:
                        url=main+url
                        if url.find('videos/BlackLagoon')>0:
                                thumbnail='http://www.animeshowcase.net/images/box2.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/Bleach')>0:
                                thumbnail='http://www.animeshowcase.net/images/Bleach/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/CowBoyBebop')>0:
                                thumbnail='http://www.animeshowcase.net/images/Cowboy%20Bebop/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/Deathnote')>0:
                                thumbnail='http://www.animeshowcase.net/images/DeathNote/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/DragonballZ')>0:
                                thumbnail='http://www.animeshowcase.net/images/Dragonball%20Z/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/FMPSeries')>0:
                                thumbnail='http://www.animeshowcase.net/images/box1.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/Films')>0:
                                thumbnail=''
                                addDir(name,url,2,"")
                        if url.find('videos/LastExile')>0:
                                thumbnail='http://www.animeshowcase.net/images/Last%20Exile/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/Naruto')>0:
                                thumbnail='http://www.animeshowcase.net/images/box7.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/NarutoShippuden')>0:
                                thumbnail='http://www.animeshowcase.net/images/Naruto%20Shippunden/box.jpg'
                                res.append((url,name,thumbnail))
                        if url.find('videos/Trigun')>0:
                                thumbnail='http://www.animeshowcase.net/images/box3.jpg'
                                res.append((url,name,thumbnail))
                                del res[7]
                for url,name,thumbnail in res:
                        addDir(name,url,1,thumbnail)
       
                
def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('..&gt;','e.wmv',link)
        response.close()
        p=re.compile('<A HREF="(.+?)">(.+?)/</A>')
        match=p.findall(code)
        if len(match)>0:
                for urla,name in match:
                        url="http://www.animeshowcase.net/videos/FMPSeries/"+urla
                        if url.find('videos/FMPSeries')>0:
                                thumbnail='http://www.animeshowcase.net/images/box1.jpg'
                                addDir(name,url,1,thumbnail)
        else:
                res=[]
                p=re.compile('<A HREF="(.+?)">(.+?).wmv</A>')
                matchlink=p.findall(code)
                if len(matchlink)>0:
                        for urla,name in matchlink:
                                
                                if url.find('videos/FMPSeries/')>0:
                                        thumbnail='http://www.animeshowcase.net/images/FMP/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/FMPSeries/')>0:
                                        thumbnail='http://www.animeshowcase.net/images/FMP/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/FMPSeries/')>0:
                                        thumbnail='http://www.animeshowcase.net/images/FMP/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/BlackLagoon')>0:
                                        thumbnail='http://www.animeshowcase.net/images/BlackLagoon/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/Bleach')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Bleach/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/CowBoyBebop')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Cowboy%20Bebop/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/DeathNote')>0:
                                        thumbnail='http://www.animeshowcase.net/images/DeathNote/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/DragonballZ')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Dragonball%20Z/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/LastExile')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Last%20Exile/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/Naruto')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Naruto/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/NarutoShippuuden')>0:
                                        thumbnail='http://www.animeshowcase.net/images/flash2.jpg'
                                        res.append((name,url+urla,thumbnail))
                                if url.find('videos/Trigun')>0:
                                        thumbnail='http://www.animeshowcase.net/images/Trigun/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                                                      
                                
                                       
                for name,url,thumbnail in res:
                        addLink(name,url,thumbnail)
                        pass
                res=[]
                p=re.compile('<A HREF="(.+?)">(.+?).mkv</A>')
                matchlink=p.findall(code)
                if len(matchlink)>0:
                        for urla,name in matchlink:
                                if url.find('videos/FMPSeries/')>0:
                                        thumbnail='http://www.animeshowcase.net/images/FMP/header.jpg'
                                        res.append((name,url+urla,thumbnail))
                                
                for name,url,thumbnail in res:
                        addLink(name,url,thumbnail)
def INDEX3(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('..&gt;','e.wmv',link)
        response.close()
        p=re.compile('<A HREF="(.+?)">(.+?).wmv</A>')
        matchlink=p.findall(code)
        for urla,name in matchlink:
                url="http://www.animeshowcase.net/videos/Films/"+urla
                addLink(name,url,"")
        
                
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
        print "categories"
        INDEX(main)
elif mode==1:
        print "index of : "+url
        INDEX2(url)
elif mode==2:
        print "index of : "+url
        INDEX3(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
