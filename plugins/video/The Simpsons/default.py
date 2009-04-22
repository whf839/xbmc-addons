import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, time
import cookielib

baseurl = 'http://wtso.net'

rootDir = os.getcwd()
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)
resDir = os.path.join(rootDir, 'resources')
COOKIEFILE  = os.path.join(resDir, 'cookies.lwp')

def getHTML( url, referer, redirect=False):
        try:
                print 'THE SIMPSONS --> getHTML :: url = ' + url
                cj = cookielib.LWPCookieJar()
                if os.path.isfile(COOKIEFILE):
                        cj.load(COOKIEFILE)
                req = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                req.addheaders = [('Referer', referer),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
                response = req.open(url)
                link = response.read()
                response.close()
                cj.save(COOKIEFILE)
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

def SEASONS():
        data = getHTML(baseurl,baseurl)
        seasons = re.compile('<a href="(.+?)" title="Season .+?">(.+?)</a>').findall(data, re.DOTALL)
        for url, season in seasons:
                season = 'Season ' + season
                addDir(season,url,1,'')
        addDir('Shorts','http://wtso.net/cat/22.html',1,'')
        addDir('Simpsons Movie','http://wtso.net/movie/2-The_Simpsons_Movie.html',2,'')
        return

def EPISODES(url):
        data = getHTML(url,baseurl)
        episodes = re.compile('<a href="(.+?)" title="(.+?)">\s*<img src="(.+?)" width=".+?" height=".+?" alt=".+?" />\s*</a>\s*</div>\s*<h3>.+?</h3>\s*<p>\s*(.+?)</p>').findall(data, re.DOTALL)
        for url, title, thumb, plot in episodes:
                title = title.replace('&#039;',"'").replace('&amp;','&').replace('  ',' ').replace('The Simpsons ','')
                plot = plot.replace('&#039;',"'").replace('&amp;','&')
                addDir(title,url,2,thumb)

def VIDEOLINKS(url,name):
        data = getHTML(url,baseurl)
        coldlink =  re.compile('<param name="movie" value="(.+?)" />').findall(data, re.DOTALL)[0]
        data = getHTML(coldlink , url, True)
        videolink = re.compile('<location>(.+?)</location>').findall(data, re.DOTALL)[0]
        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
        item.setInfo( type="Video", infoLabels={ "Title": name})
        if xbmcplugin.getSetting("dvdplayer") == "true":
                player_type = xbmc.PLAYER_CORE_DVDPLAYER
        else:
                player_type = xbmc.PLAYER_CORE_MPLAYER
        xbmc.Player(player_type).play(videolink, item)


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
        SEASONS()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        EPISODES(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)




