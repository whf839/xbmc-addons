import xbmcplugin
import xbmcgui
import xbmc

import common
import urllib,urllib2
import sys
import re

class Main:

    def __init__( self ):
        name = common.args.name
        pid = common.args.pid
        thumbnail = common.args.thumbnail
        #print pid
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
            ok=xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(finalurl, item)

