#############################################################################
#
# Navi-X Playlist browser
# v2.7 by rodejo (rodejo16@gmail.com)
#
# -v2.7   (2009/04/11)
#
# Changelog (v2.7)
# -Added new playlist item called 'processor'. Points to a playlist item processing server.
# -Youtube fix
# -Added PLX playlist multiline comment tag (""").
#
#############################################################################

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

sys.path.append(os.path.join(os.getcwd().replace(";",""),'src'))
from libs2 import *
from navix import *

######################################################################
# Description: 
######################################################################
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

######################################################################
# Description: 
######################################################################

params=get_params()
#mode=None
#name=None
mode=0
name=''
url=''
processor=''
date=''
type=''
page=1

mediaitem=CMediaItem(name="Navi-X home", type="playlist", URL="http://www.navi-x.org/playlists/homeplg.plx")

try:
        url=urllib.unquote_plus(params["url"])
        mediaitem.URL = url
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
        mediaitem.name = name
except:
        pass
try:
        type=urllib.unquote_plus(params["type"])
        mediaitem.type = type
except:
        pass
try:
        processor=urllib.unquote_plus(params["processor"])
        mediaitem.processor = processor
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
        mediaitem.date = date
except:
        pass         
#try:
#        mode=int(params["mode"])
#except:
#        pass
#try:
#        page=int(params["page"])
#except:
#        pass

#Trace(type + " " + name + " " + url + '\n')

Init()

SelectItem(mediaitem)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
