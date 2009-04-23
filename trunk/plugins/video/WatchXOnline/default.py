import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, time
import cookielib

baseurl = 'http://watchxonline.com'

def getHTML( url, referer, redirect=False):
        try:
                print 'WATCHXONLINE --> getHTML :: url = ' + url
                cj = cookielib.LWPCookieJar()
                req = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                req.addheaders = [('Referer', referer),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
                response = req.open(url)
                link = response.read()
                response.close()
                reurl = response.geturl()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                if redirect==True:
                        reurl = re.compile('file=(.+?)&').findall(reurl, re.DOTALL)[0]
                        response = req.open(reurl)
                        link = response.read()
                        response.close()
                        return link
                else:
                        return link

def CATEGORIES():
        data = getHTML(baseurl,baseurl)
        cats = re.compile('<li><a href="(.+?)">(.+?)</a>\s*<a href="javascript:void\(0\);"').findall(data, re.DOTALL)
        for url, cat in cats:
                #skipping movies because most don't use coldlink
                #if cat == 'Movies':
                #        continue
                url = baseurl + url
                addDir(cat,url,1,'')
        return

def SUBCATEGORIES(url):
        data = getHTML(url,baseurl)
        subcats = re.compile('<h4 class="category">Sub-categories(.+?)</h4>').findall(data, re.DOTALL)[0]
        subcats = re.compile('<a href="(.+?)">(.+?)</a>').findall(subcats)
        for url, cat in subcats:
                url = baseurl + url
                addDir(cat,url,2,'')
        return

def SHOW(url):
        data = getHTML(url,baseurl)
        subcats = re.compile('<h4 class="category">Sub-categories(.+?)</h4>').findall(data, re.DOTALL)
        if subcats <> []:
                subcats = re.compile('<a href="(.+?)">(.+?)</a>').findall(subcats[0])
        else:
                rssurl = re.compile('<link rel="alternate" type="application/rss\+xml" title=".+?" href="(.+?)"').findall(data)[0]
                EPISODES(rssurl)
                return
        for url, cat in subcats:
                url = baseurl +'/rss'+ url
                addDir(cat,url,3,'')
        return

def EPISODES(url):
        data = getHTML(url,baseurl)
        episodes = re.compile('<item>\s*<author>.+?</author>\s*<title>(.+?)</title>\s*<link>(.+?)</link>\s*<description>\s*<!\[CDATA\[\s*<img src="(.+?)"').findall(data, re.DOTALL)
        for title, url, thumb in episodes:
                cleantitle = re.compile('Episode.+?\((.+?)\)').findall(title)
                if cleantitle <> []:
                        title = cleantitle[0]
                title = title.replace('  ',' ').replace(' - ',' ').replace('(','- ').replace('&amp;','&').replace('&#039;',"'").title()
                addDir(title,url,4,thumb)

def VIDEOLINKS(url,name):
        data = getHTML(url,baseurl)
        coldlink =  re.compile('<param name="movie" value="(.+?)" />').findall(data, re.DOTALL)
        if coldlink <> []:
                data = getHTML(coldlink[0] , url, True)
                videolink = re.compile('<location>(.+?)</location>').findall(data, re.DOTALL)[0]
                item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                item.setInfo( type="Video", infoLabels={ "Title": name})
                xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(videolink, item)
        else:
                xbmcgui.Dialog().ok('Unsupported Video Provider','Unsupported Video Provider')


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
        print ""
        CATEGORIES()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        SUBCATEGORIES(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        SHOW(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==3:
        print ""+url
        EPISODES(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)




