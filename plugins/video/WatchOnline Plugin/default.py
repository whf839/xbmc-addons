import urllib,urllib2,re,xbmcplugin,xbmcgui
#WATCHONLINE PLUGIN FOR XBMC 2008.#REQ:LONDONBOY XBMCFORUMS.
#IF YOU`RE SEEING THIS YOU ARE A PYTHON ENTHUSIAST - GET INVOLVED !#

def INDEXCATS():
        addDir("1. MOVIES","http://www.watch0nline.info",1,"")
        addDir( "2. TV SHOWS","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=shows",2,"")
        addDir( "3. CARTOONS","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=cartons",2,"")
        addDir("4. SPORT","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=Sport",2,"")
        addDir( "5. OTHER","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=other",2,"")
        addDir( "6. EXYU SERIJE","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=Serije",2,"")

def INDEXMOVIES():
        addDir( "1. 2008 MOVIES","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=2008",2,"")
        addDir( "2. 2007 MOVIES","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=2007",2,"")
        addDir( "3. ENGLISH MOVIES","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=English",2,"")
        addDir( "4. DIVX MOVIES","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=Divx",2,"")
        addDir( "5. EXYU MOVIES","http://www.watch0nline.info/index.php?option=com_seyret&task=searchvideos&Itemid=26&searchkey=exyu-movies",2,"")
       
def INDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\n\t\t\t\t<td valign=".+?" width=".+?"><a href=".+?"><img src=(.+?) width=".+?" style=".+?"  alt="" /></a></td>\n\t\t\t\t<td valign=".+?" class="searchresultvideodetails"><span class="searchresultvideotitle"><a href="(.+?)">(.+?)</a></span>')
        match=p.findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,3,thumbnail)

def VIDEOLINKS(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<embed type="video/divx" src="(.+?)"')
        match=p.findall(link)
        if len(match)<1:
                res = []
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('file=(.+?)&image')
                match=p.findall(link)
                cache=match[0]
                req = urllib2.Request(cache)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link2=response.read()
                response.close()
                p=re.compile('\r\n<location>(.+?)</location>\r\n<image>(.+?)</image>\r\n')
                match=p.findall(link2)
                for url,thumbnail in match:
                        clean=re.sub('&amp;','&',url)
                        addLink("WATCH VIDEO",clean,thumbnail)
                
        else:
                url=match[0]
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
        print "CATEGORY INDEX : "
        INDEXCATS()
elif mode==1:
        print "MOVIECAT INDEX : "+url
        INDEXMOVIES()
elif mode==2:
        print "GET INDEX OF PAGE : "+url
        INDEX(url,name)
elif mode==3:
        print "GET MOVIE/TV/SPORT/OTHER ETC VIDEO LINK: "+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
