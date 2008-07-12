import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

#Channel 101 Plugin - By Voinage 2008.

def CATS():
        addDir("PRIME TIME","http://www.channel101.com/shows/primetime.php",1,"http://www.channel101.com/img/cache/titles/showHeader_79e0d3d2184f8e238396b0054ca4c973.png")
        addDir("CANCELLED","http://www.channel101.com/shows/cancelled.php",1,"http://www.channel101.com/img/cache/titles/showHeader_5135924d9f5240fe716473ac4957935c.png")
        addDir("FAILED PILOTS","http://www.channel101.com/shows/failedpilots.php",1,"http://www.channel101.com/img/cache/titles/showHeader_1aecc651832437eeeb4a098084e18dc2.png")
        addDir("SPECIALS","http://www.channel101.com/shows/specials.php",1,"http://www.channel101.com/img/cache/titles/showHeader_b0408b5efdece83eeff166ce87f8d656.png")
        addDir("TOP DOWNLOADS","http://www.channel101.com/shows/topdownloads.php",1,"http://www.channel101.com/img/cache/titles/showHeader_ac21fa6008b54eaf9eda3f8f8562e2fd.png")

def INDEX(url):

        req=urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\n      <a href="(.+?)"><img src="(.+?)"  width="180" height="120" alt="(.+?) -.+?" title="" border="0"/>')
        match=p.findall(link)
        for url2,thumbnail,name in match:
                main="http://www.channel101.com"
                thumbnail=main+thumbnail
                addDir(name,main+url2,2,thumbnail)
        p=re.compile('<a href="(.+?)"><img src="(.+?)" border="0" alt="NEXT &gt;"  />')
        match=p.findall(link)
        for next,thumbnail in match:
                main="http://www.channel101.com"
                thumbnail=main+thumbnail
                addDir(" NEXT PAGE",main+next,1,thumbnail)
def VIDEO(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        p=re.compile('&nbsp;&nbsp;<a href="(.+?)">download</a>')
        match=p.findall(link)
        i=0
        for link in match:
                link="http://www.channel101.com"+link
                if len(link)>20:
                        i=i+1
                        addLink(name+" Episode "+str(i),link,"")
                else:
                        addLink("NO VIDEO FOUND ON WEBSITE",link,"")
                
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
        CATS()
elif mode==1:
        print "index of : "+url
        INDEX(url)
elif mode==2:
        print "index of : "+url
        VIDEO(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
