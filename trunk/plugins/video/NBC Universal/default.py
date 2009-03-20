__plugin__ = "NBC Universal"
__authors__ = "BlueCop"
__credits__ = ""
__version__ = "0.1"

import urllib, urllib2
import os, re, sys, md5
import xbmc, xbmcgui, xbmcplugin

import nbc as nbc
import scifi as scifi
import usa as usa


#lists NBC Universal Channels
def listCategories():
        if xbmcplugin.getSetting("channel") == "true":
                addDir('NBC', 'nbc', 1)
                addDir('USA', 'usa', 1)
                addDir('Sci-Fi', 'scifi', 1)
        elif xbmcplugin.getSetting("channel") == "false":
                cat = 'nbc'
                shows = nbc.shows()
                for url, show, thumbnail in shows:
                        show = str(show).replace('&amp;','&').replace('&#039;',"'")
                        addDir(show, cat + '<break>' + url, 2, thumbnail)
                cat = 'usa'
                shows = usa.shows()
                for url, show, thumbnail in shows:
                        show = str(show).replace('&amp;','&').replace('&#039;',"'")
                        addDir(show, cat + '<break>' + url, 2, thumbnail)                
                cat = 'scifi'
                shows = scifi.shows()
                #Add show links
                for url, show, thumbnail in shows:
                        show = str(show).replace('&amp;','&').replace('&#039;',"'")
                        addDir(show, cat + '<break>' + url, 2, thumbnail)

        
#Lists shows for a particular channel
def listShowsByCat(cat):
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        #Get shows for selected channel
        if cat == 'nbc':
                shows = nbc.shows()
        elif cat == 'usa':
                shows = usa.shows()
        elif cat == 'scifi':
                shows = scifi.shows()
        #Add show links
        for url, show, thumbnail in shows:
                show = str(show).replace('&amp;','&').replace('&#039;',"'")
                addDir(show, cat + '<break>' + url, 2, thumbnail)


#lists episodes
def listEpisodes(url):
        cat = url.split('<break>')[0]
        show = url.split('<break>')[1]
        #Get episodes for selected show for selected channel
        if cat == 'nbc':
                episodes = nbc.episodes(show)
        elif cat == 'usa':
                episodes = usa.episodes(show)
        elif cat == 'scifi':
                episodes = scifi.episodes(show)
        #Add Episode links
        print episodes
        for url, name, thumbnail in episodes:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                if 'id=' in url:
                        urlsplit = url.split('id=')
                        vid = urlsplit[1]
                else:
                        #urlsplit = url.split('/')
                        #n = len(urlsplit)
                        #vid = urlsplit[n-2]
                        vid = url
                addLink(name, cat + '<break>' + vid, 3 , thumbnail)
       

#Get SMIL url and play video
def playRTMP(url, name):
        cat = url.split('<break>')[0]
        vid = url.split('<break>')[1]
        if cat == 'nbc':
                smilurl = nbc.getsmil(vid)
                rtmpurl = str(nbc.getrtmp())
                swfUrl = nbc.getswfUrl()
                link = str(nbc.getHTML(smilurl))
        elif cat == 'usa':
                smilurl = usa.getsmil(vid)
                rtmpurl = str(usa.getrtmp())
                swfUrl = usa.getswfUrl()
                link = str(usa.getHTML(smilurl))
        elif cat == 'scifi':
                smilurl = scifi.getsmil(vid)
                rtmpurl = str(scifi.getrtmp())
                swfUrl = scifi.getswfUrl()
                link = str(scifi.getHTML(smilurl))
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
                if '_0700' in playpath and (xbmcplugin.getSetting("quality") == '1' or '_0700' in playpath and (ret == 0)):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", playpath)
                elif '_0500' in playpath and (xbmcplugin.getSetting("quality") == '2') or '_0500' in playpath and (ret == 1):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", playpath)
        if xbmcplugin.getSetting("dvdplayer") == "true":
                player_type = xbmc.PLAYER_CORE_DVDPLAYER
        else:
                player_type = xbmc.PLAYER_CORE_MPLAYER
        xbmc.Player(player_type).play(rtmpurl, item)
        
        
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


def addLink(name, url, mode, iconimage='', plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name, url, mode, iconimage='', plot=''):
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
print "\n\n\n\n\n\n\nstart of NBC Universal plugin\n\n\n\n\n\n"

if mode==None or url==None or len(url)<1:
        print ""
        listCategories()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        listShowsByCat(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        listEpisodes(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==3:
        print ""+url
        playRTMP(url, name)
