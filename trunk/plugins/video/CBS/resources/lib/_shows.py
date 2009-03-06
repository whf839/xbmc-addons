import xbmcplugin
import xbmcgui
import xbmc

import common
import urllib,urllib2
import sys
import re

class Main:

    def __init__( self ):
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        if common.args.mode == 'Shows':
            self.LISTSHOWS('all')
        elif common.args.mode == 'ShowsPrimetime':
            self.LISTSHOWS('primetime')
        elif common.args.mode == 'ShowsDaytime':
            self.LISTSHOWS('daytime')
        elif common.args.mode == 'ShowsLate':
            self.LISTSHOWS('late')
        elif common.args.mode == 'ShowsClassics':
            self.LISTSHOWS('classics')
        elif common.args.mode == 'ShowsSpecials':
            self.LISTSHOWS('specials')

    def LISTSHOWS(self,cat):
        print cat
        url = common.ALL_SHOWS_URL
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="shows" target="_parent">(.+?)</a>').findall(link)
        for url,name in match:
                thumb = "http://www.cbs.com" + url + "images/common/show_logo.gif"
                #Clean names
                name = name.replace("<br>"," ").replace("&reg","")
                #Ignore badshow links & showids
                if "http://" in url:
                        print "Bad Show url :" + url
                elif "/daytime/" == url:
                        print "Bad Show url :" + url
                elif "/primetime/survivor/fantasy/" == url:
                        print "Bad Show url :" + url   
                else:
                        #Fix late show showid & thumb
                        if "/latenight/lateshow/" == url:
                                url = "/late_show/"
                                thumb = "http://www.cbs.com" + url + "images/common/show_logo.gif"
                        #Fix crimetime thumb        
                        elif "/crimetime/" == url:
                                thumb = "http://www.cbs.com" + url + "images/common/show_logo.png"
                        #Fix 48 Hours and Victorias Secret thumb
                        elif "/primetime/48_hours/" == url or "/specials/victorias_secret/" == url:
                                thumb = "http://www.cbs.com" + url + "images/common/show_logo.jpg"
                        #Blank icons for unavailable
                        elif "/primetime/flashpoint/" == url or "/primetime/game_show_in_my_head/" == url or "/specials/grammys/lincoln/" == url or "/primetime/big_brother/housecalls/" == url:
                                thumb = ''
                        #All Categories 
                        if cat == "all":
                            common.addDirectory(name,url,'List',thumb,thumb)
                        #Selected Categories
                        elif cat in url:
                            common.addDirectory(name,url,'List',thumb,thumb)
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
