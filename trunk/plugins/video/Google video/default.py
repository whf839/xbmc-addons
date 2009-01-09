import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,socket,os

#Google Plugin - By Voinage 2008.
#set socket timeout globally in seconds for bad server days.
timeout = 50
socket.setdefaulttimeout(timeout)



def SEARCH():
        
        if xbmcplugin.getSetting("Search Duration : Short") == "true":
                dur="&dur=1"
                SITE(dur)
        elif xbmcplugin.getSetting("Search Duration : Medium") == "true":
                dur="&dur=2"
                SITE(dur)
        elif xbmcplugin.getSetting("Search Duration : Long") == "true":
                dur="&dur=3"
                SITE(dur)
        else:
                dur="&dur="
                SITE(dur)

def SITE(dur):
        
        if xbmcplugin.getSetting("site : GOOGLE") == "true":
                site="+site%3Avideo.google.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : YOUTUBE") == "true":
                site="+site%3Ayoutube.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : GUBA") == "true":
                site="+site%3Aguba.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : YOUKU") == "true":
                site="+site%3Ayouku.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : TUDOU") == "true":
                site="+site%3Atudou.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : VEOH") == "true":
                site="+site%3Aveoh.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : MYSPACE") == "true":
                site="+site%3Amyspace.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : DAILYMOTION") == "true":
                site="+site%3Adailymotion.com"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : TRILULILU") == "true":
                site="+site%3Atrilulilu.ro"
                GOOGLESEARCH(dur,site)
        elif xbmcplugin.getSetting("site : CLIPVN") == "true":
                site="+site%3Aclip.vn"
                GOOGLESEARCH(dur,site)
        else:
                site=""
                GOOGLESEARCH(dur,site)

        
def CATS():
        if xbmcplugin.getSetting("Clear Previous Searches") == "true":
                os.remove('Q:/plugins/video/Google video/Search.google')
        else:
                addDir("SEARCH GOOGLE","http://Voinage.com",2,"");addDir("PREVIOUS SEARCHES","http://Voinage.com",1,"")

def PREVSEARCH():
        main=open('Q:/plugins/video/Google video/Search.google','r').read()
        bits=re.compile('<URL>(.+?)</URL><NAME>(.+?)</NAME>').findall(main)
        for url,name in bits:
                addDir(name,url,3,"")
def INDEX(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read();page=re.compile('<a class="main-pagi-abs" href="(.+?)">').findall(response)
        if len(page)<1:
                match=re.compile('<img class="thumbnail-img" src="(.+?)"></a></div>\n<div class="rl-thumbnail-rollover" onclick=".+?"></div>\n<div class=".+?"></div>\n</div>\n<div class="rl-metadata">\n<div class="rl-title" onclick=".+?">\n<span class="rl-filetype">\n</span>\n<a href="(.+?)" target="_top">\n(.+?)\n</a>').findall(response)
                for thumbnail,url,name in match:
                        if url.find('myspace')>0:
                                code=re.sub('http://.+?myspace.com/.+?fuseaction=.+?individual&.+?=','',url)
                                url='http://mediaservices.myspace.com/services/rss.ashx?videoID='+code
                        addDir(name,url,4,thumbnail)
        else:
                for i in range(0,len(page)):
                        req = urllib2.Request('http://video.google.com'+page[i])
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req);link=response.read();response.close()
                        code=re.sub('&#39;','',link);code2=re.sub('&amp;','',code);code3=re.sub('&quot;','',code2)
                        match=re.compile('<img class="thumbnail-img" src="(.+?)"></a></div>\n<div class="rl-thumbnail-rollover" onclick=".+?"></div>\n<div class=".+?"></div>\n</div>\n<div class="rl-metadata">\n<div class="rl-title" onclick=".+?">\n<span class="rl-filetype">\n</span>\n<a href="(.+?)" target="_top">\n(.+?)\n</a>').findall(code3)
                        for thumbnail,url,name in match:
                                if url.find('myspace')>0:
                                        code=re.sub('http://.+?myspace.com/.+?fuseaction=.+?individual&.+?=','',url)
                                        url='http://mediaservices.myspace.com/services/rss.ashx?videoID='+code
                                addDir(name,url,4,thumbnail)

def GOOGLESEARCH(dur,site):
        res=[]
        keyb = xbmc.Keyboard('', 'Search Google Video')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                test=search
                encode=urllib.quote_plus(search)
                req = urllib2.Request('http://video.google.com/videosearch?hl=en&q='+encode+site+'&btnG=Google+Search&lr='+dur+'&so=0&num=100#')
                f = open('Q:/plugins/video/Google video/Search.google', 'a');f.write('<URL>http://video.google.com/videosearch?hl=en&q='+encode+site+'&btnG=Google+Search&lr='+dur+'&so=0&num=100#</URL><NAME>'+search+'</NAME>');f.close()
                response = urllib2.urlopen(req).read();page=re.compile('<a class="main-pagi-abs" href="(.+?)">').findall(response)
                if len(page)<1:
                        match=re.compile('<img class="thumbnail-img" src="(.+?)"></a></div>\n<div class="rl-thumbnail-rollover" onclick=".+?"></div>\n<div class=".+?"></div>\n</div>\n<div class="rl-metadata">\n<div class="rl-title" onclick=".+?">\n<span class="rl-filetype">\n</span>\n<a href="(.+?)" target="_top">\n(.+?)\n</a>').findall(response)
                        for thumbnail,url,name in match:
                                if url.find('myspace')>0:
                                        code=re.sub('http://.+?myspace.com/.+?fuseaction=.+?individual&.+?=','',url)
                                        url='http://mediaservices.myspace.com/services/rss.ashx?videoID='+code
                                addDir(name,url,4,thumbnail)
                else:
                        for i in range(0,len(page)):
                                req = urllib2.Request('http://video.google.com'+page[i])
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req);link=response.read();response.close()
                                code=re.sub('&#39;','',link);code2=re.sub('&amp;','',code);code3=re.sub('&quot;','',code2)
                                match=re.compile('<img class="thumbnail-img" src="(.+?)"></a></div>\n<div class="rl-thumbnail-rollover" onclick=".+?"></div>\n<div class=".+?"></div>\n</div>\n<div class="rl-metadata">\n<div class="rl-title" onclick=".+?">\n<span class="rl-filetype">\n</span>\n<a href="(.+?)" target="_top">\n(.+?)\n</a>').findall(code3)
                                for thumbnail,url,name in match:
                                        if url.find('myspace')>0:
                                                code=re.sub('http://.+?myspace.com/.+?fuseaction=.+?individual&.+?=','',url)
                                                url='http://mediaservices.myspace.com/services/rss.ashx?videoID='+code
                                        addDir(name,url,4,thumbnail)
                
def VIDEO(name,url):
        if url.find('veoh')>0:
                url2=url+'-';bit=re.compile(r'http://www.veoh.com/videos/(.+?)-').findall(url2)
                req = urllib2.Request('http://www.veoh.com/rest/videos/'+bit[0]+'/details')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                veoh=re.compile('fullPreviewHashPath="(.+?)"').findall(response)
                thumb=re.compile('fullHighResImagePath="(.+?)"').findall(response)
                addLink(name,veoh[0],thumb[0])
                addLink(name+'-AVI','http://127.0.0.1:64653/'+bit[0],thumb[0])
        if url.find('myspace')>0:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req);link=response.read();response.close()
                title=re.compile('<item>\r\n      <title>(.+?)</title>').findall(link)
                thumb=re.compile('<media:thumbnail url="(.+?)" />').findall(link)
                flv=re.compile('<media:content url="(.+?)" type="video/x-flv" medium=".+?" status=".+?" duration=".+?" />').findall(link)
                addLink(title[0],flv[0],thumb[0])
        if url.find('youtube')>0:
                url2=url+'-';bit=re.compile('http://www.youtube.com/.+?v=(.+?)-').findall(url2)
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('"t": "(.+?)"').findall(response)
                for youtube in match:
                        addLink(name+"-YOUTUBE","http://www.youtube.com/get_video?video_id="+bit[0]+"&t="+youtube,"http://www.webtvwire.com/wp-content/uploads/2007/06/youtube.jpg")
                        addLink(name+"-YOUTUBE Hi-def","http://www.youtube.com/get_video?video_id="+bit[0]+"&t="+youtube+"&fmt=18","http://www.webtvwire.com/wp-content/uploads/2007/06/youtube.jpg")
        if url.find('ideoplay')>0:
               req = urllib2.Request("http://video.google.com"+url)
               req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
               response = urllib2.urlopen(req).read()
               match=re.compile('.+?videoUrl.+?.+?.+?.+?(.+?)%26sigh').findall(response)
               addLink(name,urllib.unquote(match[0]),"")
        if url.find('clip')>0:
                bit=re.compile('http://clip.+?/watch/.+?/(.+?),vn').findall(url)
                req = urllib2.Request("http://clip.vn/movies/nfo/"+bit[0])
                req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile(r'\r\n\t\t\t\t\t\t\t<enclosure url=\'(.+?)\' duration=\'.+?\' id=\'.+?\' type=\'video/x-flv\'/>\r\n\t\t\t\t\t</ClipInfo>').findall(response)
                addLink(name,match[0],"")
        if url.find('dailymotion')>0:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('url=rev=.+?&uid=.+?&lang=en&callback=.+?&preview=.+?&video=(.+?)%40%40spark').findall(response)
                addLink(name,"http://www.dailymotion.com"+urllib.unquote(match[0]),"")
        if url.find('guba')>0:
                url=url+'-';bit=re.compile('http://www.guba.com/watch/(.+?)-').findall(url)                
                req = urllib2.Request('http://www.guba.com/xml/playerConfig/'+bit[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('<videoUrl><.+?CDATA.(.+?)..></videoUrl>').findall(response)
                if match[0].find('skinvideo')>0:
                        addLink('Video removed from site.',match[0],"")
                else:
                        addLink(name,match[0],"")
        if url.find('tudou')>0:
                bit=re.compile(r'http://www.tudou.com/programs/view/(.+?)/').findall(url)
                req = urllib2.Request("http://www.flvcd.com/parse.php?kw=http%3A%2F%2Fwww.tudou.com%2Fprograms%2Fview%2F"+bit[0]+"%2F&flag=")
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('<a href="(.+?)" target="_blank" onclick=".+?">').findall(response)
                addLink(name,match[0],"")
        if url.find('youku')>0:
                i=0;bit=re.compile(r'http://v.youku.com/.+?/(.+?)=.html').findall(url)
                req = urllib2.Request("http://www.flvcd.com/parse.php?flag=&kw=http%3A%2F%2Fv.youku.com%2Fv_show%2F"+bit[0]+"%3D.html&sbt=%BF%AA%CA%BCGO%21")
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('<a href="(.+?)" target="_blank" onclick=".+?">').findall(response)
                for url in match:
                        i=i+1;addLink(name+" part-"+str(i),url,"")
        if url.find('metacafe')>0:
                req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+urllib.quote_plus(url)+"&flag=")
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req).read()
                match=re.compile('<a href="(.+?)" target="_blank" class="link">').findall(response)
                addLink(name,match[0],"")

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

      
def addLink(name,url,thumbnail):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
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
        print "PREV SEARCH"
        PREVSEARCH()
elif mode==2:
        print "SEARCH"
        SEARCH()
elif mode==3:
        print "INDEX"
        INDEX(url)
elif mode==4:
        print "VIDEO"
        VIDEO(name,url)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
