import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, md5
from pyamf.remoting.client import RemotingService

__plugin__ = "NBC"
__authors__ = "BlueCop"
__credits__ = ""
__version__ = "0.2"

baseurl = 'http://www.usanetwork.com/'
fullurl = 'http://www.usanetwork.com/fullepisodes/'
weburl = 'http://www.nbc.com/Video/library/webisodes/'

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


def SHOWS():
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        shows = getHTML(fullurl)
        clean = re.compile('\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>').sub( '\n', shows)
        match=re.compile('<img src="(.+?)" border="0" height="142" width="276"></td>').findall(clean)
        shows = []
        for url in match:
                url = baseurl + url
                if 'monk.gif' in url:
                        name = 'Monk'
                        cat = 'monk'
                elif 'psych.gif' in url:
                        name = 'Pysch'
                        cat = 'psych'
                elif 'bn.gif' in url:
                        name = 'Burn Notice'
                        cat = 'burnnotice'
                elif 'ips.gif' in url:
                        name = 'In Plain Sight'
                        cat = 'inplainsight'
                elif 'sw.gif' in url:
                        name = 'Starter Wife'
                        cat = 'starterwife'
                elif 'steveo.gif' in url:
                        name = 'Dr. Steve O'
                        cat = 'drsteve-o'
                addDir(name,cat,1,url)

def EPISODES(cat):
        shows = getHTML(fullurl)
        clean = re.compile('\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>').sub( '\n', shows)
        match=re.compile('<a href="(.+?)" target="new">(.+?)</a>').findall(clean)
        for url,name in match:
                if '<img' in name:
                        continue
                if cat in url:
                        pidsplit = url.split('id=')
                        pid = pidsplit[1]
                        addDir(name,pid,2,'')
                

def PLAY(episodeGuid,name):
        gw = RemotingService(url='http://video.nbcuni.com/amfphp/gateway.php',
                     referer='http://www.usanetwork.com/[[IMPORT]]/video.nbcuni.com/outlet/extensions/inext_video_player/video_player_extension.swf',
                     user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)',
                     )
        ClipAll_service = gw.getService('getClipInfo.getClipAll')
        geo  ="inside"
        num1 = "www.usanetwork.com"
        num2 = "-1"
        response = ClipAll_service(episodeGuid,geo,num1,num2)
        if 'errordis' in response.keys():
                xbmcgui.Dialog().ok(xbmc.getLocalizedString(30005), xbmc.getLocalizedString(30005))
                return
        else:
                url = 'http://video.nbcuni.com/' + response['clipurl']
                PLAYRTMP(url, name)


def PLAYRTMP(url, name):
        rtmpurl = 'rtmp://8.18.43.101/ondemand?_fcs_vhost=cp35588.edgefcs.net'
        swfUrl = "http://www.usanetwork.com/[[IMPORT]]/video.nbcuni.com/outlet/extensions/inext_video_player/video_player_extension.swf"
        link = str(getHTML(url))
        match=re.compile('<video src="(.+?)"').findall(link)
        if (xbmcplugin.getSetting("quality") == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select(xbmc.getLocalizedString(30006), [xbmc.getLocalizedString(30002),xbmc.getLocalizedString(30003),xbmc.getLocalizedString(30007)])
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
print "\n\n\n\n\n\n\nstart of USA plugin\n\n\n\n\n\n"

if mode==None or url==None or len(url)<1:
        print ""
        SHOWS()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        EPISODES(url)      
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        PLAY(url,name)
elif mode==3:
        print ""+url

