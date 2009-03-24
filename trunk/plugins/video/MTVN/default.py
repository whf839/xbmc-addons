__plugin__ = "MTVN Plugin"
__authors__ = "BlueCop"
__credits__ = ""
__version__ = "0.1"

import urllib, urllib2
import os, re, sys, md5
import xbmc, xbmcgui, xbmcplugin

import mtvn as mtvn

def listCategories():
        addDir('Browse Artists A-Z', 'artists', 1)
        addDir('Browse Artists by Genre', 'artists', 2)
        addDir('Browse Videos by Genre', 'videos', 2)
        addDir('Search Artist', 'searchArtist', 5)
        addDir('Search Video', 'searchVideo', 5)
        #addDir('Favorite Videos', 'favArtist', 1)
        #addDir('Favorite Artists', 'favVideo', 1)
        
def listAZ():
        addDir('#', '-', 11)
        addDir('A', 'a', 11)
        addDir('B', 'b', 11)
        addDir('C', 'c', 11)
        addDir('D', 'd', 11)
        addDir('E', 'e', 11)
        addDir('F', 'f', 11)
        addDir('G', 'g', 11)
        addDir('H', 'h', 11)
        addDir('I', 'i', 11)
        addDir('J', 'j', 11)
        addDir('K', 'k', 11)
        addDir('L', 'l', 11)
        addDir('M', 'm', 11)
        addDir('N', 'n', 11)
        addDir('O', 'o', 11)
        addDir('P', 'p', 11)
        addDir('Q', 'q', 11)
        addDir('R', 'r', 11)
        addDir('S', 's', 11)
        addDir('T', 't', 11)
        addDir('U', 'u', 11)
        addDir('V', 'v', 11)
        addDir('W', 'w', 11)
        addDir('X', 'x', 11)
        addDir('Y', 'y', 11)
        addDir('Z', 'z', 11)
        return

def listGenres(mode):
        if mode == 'artists':
                linkmode = 22
        elif mode == 'videos':
                linkmode = 23
        #       Genre Name                      Genre Alias             Mode           
        addDir('World/Reggae',                  'world_reggae',         linkmode)
        addDir('Pop',                           'pop',                  linkmode)
        addDir('Metal',                         'metal',                linkmode)
        addDir('Environmental',                 'environmental',        linkmode)
        addDir('Latin',                         'latin',                linkmode)
        addDir('R&B',                           'randb',                linkmode)
        addDir('Rock',                          'rock',                 linkmode)
        addDir('Easy Listening',                'easy_listening',       linkmode)
        addDir('Jazz',                          'jazz',                 linkmode)
        addDir('Country',                       'country',              linkmode)
        addDir('Hip-Hop',                       'hip_hop',              linkmode)
        addDir('Classical',                     'classical',            linkmode)
        addDir('Electronic / Dance',            'electronic_dance',     linkmode)
        addDir('Blues / Folk',                  'blues_folk',           linkmode)
        addDir('Alternative',                   'alternative',          linkmode)
        addDir('Soundtracks / Musicals',        'soundtracks_musicals', linkmode)

def listArtistsAZ(letter):
        artists = mtvn.artistBrowse(letter)
        for url, name, thumbnail in artists:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                addDir(name, url, 3, thumbnail)
        return

def listGenreArtist(genre):
        artists = mtvn.genreArtists(genre)
        for url, name, thumbnail in artists:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                addDir(name, url, 3, thumbnail)
        return

def listGenreVideos(genre):
        videos = mtvn.genreVideos(genre)
        print videos
        for url, name, thumbnail in videos:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                addLink(name, url, 4, thumbnail)
        return

def listArtistVideos(artist):
        videos = mtvn.artistVideos(artist)
        print videos
        for url, name, thumbnail in videos:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                addLink(name, url, 4, thumbnail)
        return

def listSearch(searchtype):
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                if searchtype == 'searchArtist':
                        videos = mtvn.artistSearch(search)
                        for url, name, thumbnail in videos:
                                name = name.replace('&amp;','&').replace('&#039;',"'")
                                addDir(name, url, 3, thumbnail)
                elif searchtype == 'searchVideo':
                        videos = mtvn.videoSearch(search)
                        for url, name, thumbnail in videos:
                                name = name.replace('&amp;','&').replace('&#039;',"'")
                                addLink(name, url, 4, thumbnail)
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return
                
#Get SMIL url and play video
def playRTMP(url, name):
        ret = ''
        if (xbmcplugin.getSetting("quality") == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select(xbmc.getLocalizedString(30006), [xbmc.getLocalizedString(30002),xbmc.getLocalizedString(30003),xbmc.getLocalizedString(30007)])
                if (ret == 2):
                        return
        rtmps = mtvn.getrtmp(url)
        swfUrl = mtvn.getswfUrl()
        print rtmps
        for _url,_playpath in rtmps:
                if '_320' in _playpath and (xbmcplugin.getSetting("quality") == '1' or '_320' in _playpath and (ret == 0)):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", _playpath)
                        rtmpurl = _url
                elif '_240' in _playpath and (xbmcplugin.getSetting("quality") == '2') or '_240' in _playpath and (ret == 1):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", _playpath)
                        rtmpurl = _url
                elif '_650' in _playpath and (xbmcplugin.getSetting("quality") == '1' or '_650' in _playpath and (ret == 0)):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", _playpath)
                        rtmpurl = _url
                elif '_300' in _playpath and (xbmcplugin.getSetting("quality") == '2') or '_300' in _playpath and (ret == 1):
                        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                        item.setInfo( type="Video",infoLabels={ "Title": name})
                        item.setProperty("SWFPlayer", swfUrl)
                        item.setProperty("PlayPath", _playpath)
                        rtmpurl = _url
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

#List Categories
if mode==None or url==None or len(url)<1:
        print ""
        listCategories()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#ARTISTS
elif mode==1:
        print ""+url
        listAZ()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==11:
        print ""+url
        listArtistsAZ(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#GENRES
elif mode==2:
        print ""+url
        listGenres(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==22:
        print ""+url
        listGenreArtist(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==23:
        print ""+url
        listGenreVideos(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#ARTISTS VIDEOS
elif mode==3:
        print ""+url
        listArtistVideos(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#SEARCH ARTISTS or VIDEOS
elif mode==5:
        print ""+url
        listSearch(url)

#Play Video
elif mode==4:
        print ""+url
        playRTMP(url, name)
