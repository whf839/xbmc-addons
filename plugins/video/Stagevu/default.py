import urllib,urllib2,re,xbmcplugin,xbmcgui
#StageVu V2008

def INDEXCATS():
        addDir('ANIMATION','http://stagevu.com/search?keywords=&category=Animation&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('COMEDY','http://stagevu.com/search?keywords=&category=Comedy&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('EDUCATIONAL','http://stagevu.com/search?keywords=&category=Educational&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('FILMS & MOVIES','http://stagevu.com/search?keywords=&category=Films+and+Movies&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('GAMES','http://stagevu.com/search?keywords=&category=Games&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('MUSIC','http://stagevu.com/search?keywords=&category=Music&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('TV-SHOWS','http://stagevu.com/search?keywords=&category=Television&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('OTHER','http://stagevu.com/search?keywords=&category=Others&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('SPORTS','http://stagevu.com/search?keywords=&category=Sports&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('NEWS & POLITICS','http://stagevu.com/search?keywords=&category=News+and+Politics&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('ART','http://stagevu.com/search?keywords=&category=Art&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('BLOGS','http://stagevu.com/search?keywords=&category=Blogs&perpage=100&page=1&sortby=relevance&ascdesc=DESC',1,'')
        addDir('SEARCH STAGEVU','http://stagevu.com',3,'')


def INDEX(url):
        p=re.compile('http://stagevu.com/search.+?keywords=&category=(.+?)&perpage=100&page=(.+?)&sortby=relevance&ascdesc=DESC')
        match=p.findall(url)
        for cat,pagenumb in match:
                page="http://stagevu.com/search?keywords=&category="+cat+"&perpage=100&page="+str(int(pagenumb)+1)+"&sortby=relevance&ascdesc=DESC"
                addDir("  NEXT PAGE",page,1,"")
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&quot;','',link)
        code1=re.sub('&#039;','',code)
        code2=re.sub('&amp;','&',code1)
        code3=re.sub("`",'',code2)
        response.close()
        p=re.compile('<a href="(.+?)">(.+?)</a></h2>\r\n\t\t\t\t<a href=".+?"><img src="(.+?)"')
        match=p.findall(code3)
        for url,name,thumb in match:
                addDir(name,url,2,"http://stagevu.com"+thumb)
                
def VIDEOLINK(url,name):
        req = urllib2.Request("http://stagevu.com"+url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<embed type="video/divx" src="(.+?)"')
        match=p.findall(link)
        vidstag=match[0]
        addLink(name,vidstag+"?.avi","")
        
def SEARCH():
        res=[]
        keyb = xbmc.Keyboard('', 'Search StageVu')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                next="http://stagevu.com/search?keywords="+encode+"&category=&perpage=100&page=1&sortby=relevance&ascdesc=DESC"
                req = urllib2.Request('http://stagevu.com/search?keywords='+encode+'&category=&perpage=100&page=1&sortby=relevance&ascdesc=DESC')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                code=re.sub('&quot;','',link)
                code1=re.sub('&#039;','',code)
                code2=re.sub('&amp;','&',code1)
                code3=re.sub("`",'',code2)
                response.close()
                p=re.compile('http://stagevu.com/search.+?keywords=(.+?)&.+?&perpage=100&page=(.+?)&sortby=relevance&ascdesc=DESC')
                match=p.findall(next)
                for key,pagenumb in match:
                        page="http://stagevu.com/search?keywords="+key+"&category=&perpage=100&page="+str(int(pagenumb)+1)+"&sortby=relevance&ascdesc=DESC"
                        addDir("  NEXT PAGE",page,1,"")
                p=re.compile('<a href="(.+?)">(.+?)</a></h2>\r\n\t\t\t\t<a href=".+?"><img src="(.+?)"')
                match=p.findall(code3)
                for url,name,thumb in match:
                        addDir(name,url,2,"http://stagevu.com"+thumb)

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
        INDEX(url)
elif mode==2:
        print "GET INDEX OF PAGE : "+url
        VIDEOLINK(url,name)
elif mode==3:
        print "GET INDEX OF PAGE : "+url
        SEARCH()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
