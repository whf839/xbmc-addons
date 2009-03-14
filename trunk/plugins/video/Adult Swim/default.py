'''
        [adult swim] v0.2 for XBMC
                
'''

__plugin__ = "[adult swim]"
__author__ = "thecheese,BlueCop(XBMC fixes and updated)"
__url__ = ""
__svn__ = ""
__version__ = "0.2"

import urllib, urllib2, re, md5
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin
from adultswim_api import *


#grab to root directory and assign the image forlder a var
rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
imageDir = os.path.join(rootDir, 'resources', 'thumbnails') + '/'
resourceDir = os.path.join(rootDir, 'resources')

#lists initial categories and caches them
def listCategories():
        aswim = AdultSwim()
        categories = aswim.getCategories()
        for category in categories:
                if category['name'] == 'Action' and (xbmcplugin.getSetting('action') == '1'):
                        shows = aswim.getShowsByCategory( category['id'] )
                        for show in shows:
                                addDir(show['name'], 'showTypes?id='+show['id'], 3 , imageDir + 'video.png')          
                elif category['name'] == 'Action' and (xbmcplugin.getSetting('action') == '0'):
                        addDir(' '+category['name'], 'listShowsByCat?cid='+category['id'], 2 , imageDir + 'categories.png', category['description'])
                elif category['name'] == 'Action' and (xbmcplugin.getSetting('action') == '2'):
                        pass
                elif category['name'] == 'Comedy' and (xbmcplugin.getSetting('comedy') == '1'):
                        shows = aswim.getShowsByCategory( category['id'] )
                        for show in shows:
                                addDir(show['name'], 'showTypes?id='+show['id'], 3 , imageDir + 'video.png')    
                elif category['name'] == 'Comedy' and (xbmcplugin.getSetting('comedy') == '0'):
                        addDir(' '+category['name'], 'listShowsByCat?cid='+category['id'], 2 , imageDir + 'categories.png', category['description'])
                elif category['name'] == 'Comedy' and (xbmcplugin.getSetting('comedy') == '2'):
                        pass
                elif category['name'] == 'Other' and (xbmcplugin.getSetting('other') == '1'):
                        shows = aswim.getShowsByCategory( category['id'] )
                        for show in shows:
                                addDir(show['name'], 'showTypes?id='+show['id'], 3 , imageDir + 'video.png')    
                elif category['name'] == 'Other' and (xbmcplugin.getSetting('other') == '0'):
                        addDir(' '+category['name'], 'listShowsByCat?cid='+category['id'], 2 , imageDir + 'categories.png', category['description'])
                elif category['name'] == 'Other' and (xbmcplugin.getSetting('other') == '2'):
                        pass

        #f = open(os.path.join(resourceDir, 'categories.xml'),'wb')
        #f.write(response)
        
#lists shows for a particular category
def listShowsByCat(url):
        aswim = AdultSwim()
        params = qs2dict(url.split('?')[1])
        shows = aswim.getShowsByCategory( params['cid'] )
        for show in shows:
                addDir(show['name'], 'showTypes?id='+show['id'], 3 , imageDir + 'video.png')


#lists episodes by show id              
def showTypes(showid):
        aswim = AdultSwim()
        url = showid+'&filterByEpisodeType=PRE,EPI'
        params = qs2dict(url.split('?')[1])
        episodes = aswim.getEpisodesByShow( params['id'], params['filterByEpisodeType'] )        
        if len(episodes) == 0:
                url = showid+'&filterByEpisodeType=CLI'
                params = qs2dict(url.split('?')[1])
                episodes = aswim.getEpisodesByShow( params['id'], params['filterByEpisodeType'] )
                for episode in episodes:
                        addDir(episode['title']+' (Clip)', 'initEpisode?ids='+episode['id'], 5 , episode['thumbnail'], episode['description'])
                return

        for episode in episodes:
                addDir(episode['title'], 'initEpisode?ids='+episode['id'], 5 , episode['thumbnail'], episode['description'])
        

        addDir(" Clips", showid+'&filterByEpisodeType=CLI', 4 , imageDir + 'video.png', 'Clips')

        #addDir(" Full Episodes", url+'&filterByEpisodeType=PRE,EPI', 4 , imageDir + 'video.png', 'Full Episodes')


#lists episodes by show id
def listEpisodes(url):
        aswim = AdultSwim()
        params = qs2dict(url.split('?')[1])
        episodes = aswim.getEpisodesByShow( params['id'], params['filterByEpisodeType'] )
        
        if len(episodes) == 0:
                xbmcgui.Dialog().ok("[adult swim]", "No entries found.")
                return

        for episode in episodes:
                addDir(episode['title']+' (Clip)', 'initEpisode?ids='+episode['id'], 5 , episode['thumbnail'], episode['description'])


def getVideoURL(id):
        params = qs2dict(url.split('?')[1])
        aswim = AdultSwim()
        episodes = aswim.getEpisodesByIDs( params['ids'] )
        playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        playlist.clear()
        playlist_urls = []
        for episode in episodes:
                for segment in episode['segments']:
                        response = aswim.getPlaylist(segment['id'])
                        match = re.compile('href="(.+?)"').findall(response)
                        title = episode['collectionTitle'] + ' - ' + episode['title']
                        item  = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=segment['thumbnail'])
                        item.setInfo(type='Video', infoLabels={'Title': title, 'Genre': episode['collectionCategoryType']})
                        playlist_urls.append(match[0])
                        playlist.add(match[0], item)
        stream = httpDownload(playlist_urls,name)
        if stream == 'false':
                return
        if xbmcplugin.getSetting("dvdplayer") == "true":
                    player_type = xbmc.PLAYER_CORE_DVDPLAYER
        else:
                    player_type = xbmc.PLAYER_CORE_MPLAYER
        ok=xbmc.Player(player_type).play( playlist )
        #xbmc.sleep(200)
        #xbmc.executebuiltin('XBMC.ActivateWindow(FullscreenVideo)')

def httpDownload( playlist_urls, name):
        def Download(url,dest):
                    dp = xbmcgui.DialogProgress()
                    dp.create('Downloading','',name)
                    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
                    try:
                                    percent = min((numblocks*blocksize*100)/filesize, 100)
                                    dp.update(percent)
                    except:
                                    percent = 100
                                    dp.update(percent)
                    if dp.iscanceled():
                                    dp.close()
        flv_file = None
        stream = 'false'
        C = 0
        if (xbmcplugin.getSetting('download') == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select(xbmc.getLocalizedString( 30011 ),[xbmc.getLocalizedString( 30006 ),xbmc.getLocalizedString( 30007 ),xbmc.getLocalizedString( 30008 ),xbmc.getLocalizedString( 30012 )])
                if (ret == 0):
                        stream = 'true'
                elif (ret == 1):
                        for url in playlist_urls:
                                C = C + 1
                                flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name+'-part'+str(C)+'.flv'))
                                Download(url,flv_file)
                elif (ret == 2):
                        for url in playlist_urls:
                                C = C + 1
                                flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name+'-part'+str(C)+'.flv'))
                                Download(url,flv_file)
                        stream = 'true'
                else:
                        return stream
        #Play
        elif (xbmcplugin.getSetting('download') == '1'):
                stream = 'true'
        #Download
        elif (xbmcplugin.getSetting('download') == '2'):
                for url in playlist_urls:
                        C = C + 1
                        flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name+'-part'+str(C)+'.flv'))
                        Download(url,flv_file)
        #Download & Play
        elif (xbmcplugin.getSetting('download') == '3'):
                for url in playlist_urls:
                        C = C + 1
                        flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name+'-part'+str(C)+'.flv'))
                        Download(url,flv_file)
                stream = 'true'            
        if (flv_file != None and os.path.isfile(flv_file)):
                finalurl =str(flv_file)
        return stream


"""
        addLink()
        this function simply adds a media link to boxee's current screen
"""
def addLink(name,url,info):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=info[2])
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Date": info[0], "Plot": info[1] } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


"""
        addDir()
        this function simply adds a directory link to boxee's current screen
"""
def addDir(name,url,mode,iconimage, plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        if plot:
                liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        else:
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



"""
        getParams()
        grab parameters passed by the available functions in this script
"""
def getParams():
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

def qs2dict(qs):
    try:
        params = dict([part.split('=') for part in qs.split('&')])
    except:
        params = {}
    return params


#grab params and assign them if found
params=getParams()
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

#print params to the debug log
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

#check $mode and execute that mode
if mode==None or url==None or len(url)<1:
        print "CATEGORY INDEX : "
        listCategories()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        listShowsByCat(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==3:
        showTypes(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==4:
        listEpisodes(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),cacheToDisc=True)
elif mode==5:
        getVideoURL(url)

