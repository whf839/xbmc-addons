import xbmcplugin
import xbmcgui
import xbmc

import common
import urllib,urllib2
import sys
import re
import os

class Main:

    def __init__( self ):
        name = common.args.name
        pid = common.args.pid
        thumbnail = common.args.thumbnail
        #print pid
        if (xbmcplugin.getSetting('480p') == 'true'):
            breakpid = pid.split('<break>')
            pid=breakpid[0]
        if (xbmcplugin.getSetting('720p') == 'true'):
            breakpid = pid.split('<break>')
            pid=breakpid[1]
        if '<break>' in pid:
            breakpid = pid.split('<break>')
            for pid in breakpid:
                url = sys.argv[0]+'?mode="'+'Play'+'"&name="'+urllib.quote_plus(name)+'"&pid="'+urllib.quote_plus(pid)+'"&thumbnail="'+urllib.quote_plus(thumbnail)+'"'
                item=xbmcgui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
                item.setInfo( type="Video",
                             infoLabels={ "Title": name,
                                          #"Season": season,
                                          #"Episode": episode,
                                          #"Duration": duration,
                                          #"Plot": plot
                                          })
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=item)
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )
        else:            
            url = "http://release.theplatform.com/content.select?format=SMIL&Tracking=true&balance=true&pid=" + pid
            link=common.getHTML(url)
            if "rtmp://" in link:
                    stripurl = re.compile('<ref src="rtmp://(.+?)" ').findall(link)
                    cleanurl = stripurl[0].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').split('<break>')
                    finalurl = "rtmp://" + cleanurl[0]
                    if ".mp4" in cleanurl[1]:
                            playpath = 'mp4:' + cleanurl[1]
                    else:
                            playpath = cleanurl[1].replace('.flv','')
            elif "http://" in link:
                    stripurl = re.compile('<ref src="http://(.+?)" ').findall(link)
                    finalurl = "http://" + stripurl[0]
                    playpath = ""
                    name = name + '.flv'
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
                    if (xbmcplugin.getSetting('download') == 'true'):
                                    flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                                    Download(finalurl,flv_file)
                    elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
                            dia = xbmcgui.Dialog()
                            ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
                            if (ret == 0):
                                    flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                                    Download(finalurl,flv_file)
                            elif (ret == 1):
                                    stream = 'true'
                            else:
                                    pass
                    elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'false'):
                            stream = 'true'
                    if (flv_file != None and os.path.isfile(flv_file)):
                            finalurl =str(flv_file)

            if "720p" in finalurl or "720p" in playpath:
                    finalname = '720p: ' + name
            elif "480p" in finalurl or "480p" in playpath:
                    finalname = '480p: ' + name
            else:
                    finalname = name
            #print "platpath: " + playpath
            #print "finalurl: " + finalurl
            item=xbmcgui.ListItem(finalname, iconImage=thumbnail, thumbnailImage=thumbnail)
            item.setInfo( type="Video",
                         infoLabels={ "Title": finalname,
                                      #"Season": season,
                                      #"Episode": episode,
                                      #"Duration": duration,
                                      #"Plot": plot,
                                       }
                         )
            swfUrl = "http://www.cbs.com/thunder/player/1_0/chromeless/1_5_1/CAN.swf"
            item.setProperty("SWFPlayer", swfUrl)
            item.setProperty("PlayPath", playpath)
            if xbmcplugin.getSetting("dvdplayer") == "true":
                    player_type = xbmc.PLAYER_CORE_DVDPLAYER
            else:
                    player_type = xbmc.PLAYER_CORE_MPLAYER
            ok=xbmc.Player(player_type).play(finalurl, item)
            xbmc.sleep(200)

