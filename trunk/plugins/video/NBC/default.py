import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, md5
from elementtree.ElementTree import *
from pyamf.remoting.client import RemotingService

__plugin__ = "NBC"
__authors__ = "BlueCop"
__credits__ = ""
__version__ = "0.2"

baseurl = 'http://www.nbc.com/'
liburl = 'http://www.nbc.com/Video/library/'
fullurl = 'http://www.nbc.com/Video/library/full-episodes/'
weburl = 'http://www.nbc.com/Video/library/webisodes/'
showsxml_url = 'http://www.nbc.com/assets/xml/video/shows.xml'

def getHTML( url ):
        try:
                print 'NBC --> getHTML :: url = '+url
                req = urllib2.Request(url)
                req.addheaders = [('Referer', 'http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)')]
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                return link

def processHTML( url ):
        html = getHTML(url)
        match=re.compile('<!-- debug info --><a href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(html)
        return match

def processFULL ( url ):
        html = getHTML(url)
        match=re.compile('<a class="list_full_det_thumb" href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(html)
        return match

def CATEGORIES():
        addDir('Full Episodes',url,1,thumb)
        addDir('Full Episodes',url,1,thumb)

def SHOWS():
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        shows = processHTML(fullurl)
        for url, name, thumb in shows:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                addDir(name,url,1,thumb)

def EPISODES(url):
        episodes = processFULL(url)
        for url, name, thumb in episodes:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                urlsplit = url.split('?vid=')
                url = urlsplit[1]
                addDir(name,url,2,thumb)

def PLAY(episodeGuid,name):
        gw = RemotingService(url='http://video.nbcuni.com/amfphp/gateway.php',
                     referer='http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf',
                     user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)',
                     )
        ClipAll_service = gw.getService('getClipInfo.getClipAll')
        geo  ="US"
        num1 = "632"
        num2 = "-1"
        response = ClipAll_service(episodeGuid,geo,num1,num2)
        url = 'http://video.nbcuni.com/' + response['clipurl']
        PLAYRTMP(url, name)

def SHOWSINT():        
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        showsxml=getHTML(showsxml_url)
        xml = ElementTree(fromstring(showsxml))
        for sh in xml.getroot().findall('show'):
                if sh.find('full') <> None:
                        addDir(sh.find('name').text,sh.find('link').text,1,'')
                else:
                        pass
                
def EPISODESINT(episodesurl):
        try:
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                episodesurl = episodesurl + 'episodes/init.xml'
                episodesxml=getHTML(episodesurl)
                xml = ElementTree(fromstring(episodesxml))
                for ep in xml.getroot().findall('episodes/episode'):
                        name = ep.find('epiTitle').text
                        epiNumber = ep.find('epiNumber').text
                        smallthumb = ep.find('epiImage').text
                        plot = ep.find('epiDescription').text
                        pid = smallthumb.replace('http://video.nbc.com/nbcrewind2/thumb/','').replace('_large.jpg','')
                        finalname = epiNumber + ' - ' + name
                        mode = 2
                        addLink(finalname,pid,2,smallthumb,plot)

        except:
                addDir('No Episodes','',0,'')

def PLAYINT(pid,name):
        url = 'http://video.nbcuni.com/nbcrewind2/smil/' + pid + '.smil'
        PLAYRTMP(url, name)


def PLAYRTMP(url, name):
        rtmpurl = 'rtmp://cp37307.edgefcs.net:80/ondemand?'
        swfUrl = "http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf"
        link = str(getHTML(url))
        match=re.compile('<video src="(.+?)"').findall(link)
        if (xbmcplugin.getSetting("quality") == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select('Select Quality Level?', ['High','Low','Exit'])
                if (ret == 2):
                        return
        else:        
                ret = None
        for playpath in match:
                playpath = playpath.replace('.flv','')
                if '_0700' in playpath and (xbmcplugin.getSetting("quality") == '1' or (ret == 0)):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", playpath)
                elif '_0500' in playpath and (xbmcplugin.getSetting("quality") == '2') or (ret == 1):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", playpath)
        if xbmcplugin.getSetting("dvdplayer") == "true":
                player_type = xbmc.PLAYER_CORE_DVDPLAYER
        else:
                player_type = xbmc.PLAYER_CORE_MPLAYER
        ok=xbmc.Player(player_type).play(rtmpurl, item)


        
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

def addLink(name,url,mode,iconimage,plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
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
print "\n\n\n\n\n\n\nstart of NBC plugin\n\n\n\n\n\n"

if mode==None or url==None or len(url)<1:
        print ""
        if (xbmcplugin.getSetting("international") == 'true'):
                SHOWSINT()
        else:
                SHOWS()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        if (xbmcplugin.getSetting("international") == 'true'):
                EPISODESINT(url)
        else:
                EPISODES(url)      
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        if (xbmcplugin.getSetting("international") == 'true'):
                PLAYINT(url,name)
        else:
                PLAY(url,name)
elif mode==3:
        print ""+url

