import urllib,urllib2,re,xbmcplugin,xbmcgui

#CBS plugin by BlueCop

def CATEGORIES():
        addDir('TV Shows','http://www.cbs.com/video/',1,'')
        addDir('Most Popular','http://www.cbs.com/sitefeeds/all/popular.js',4,'')
        addDir('Latest Videos','http://www.cbs.com/sitefeeds/all/recent.js',4,'')
        #Add HD feeds http://www.cbs.com/sitefeeds/hd/hd.js
                       
def INDEX(url):
        print "INDEX " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="shows" target="_parent">(.+?)</a>').findall(link)
        for url,name in match:
                addDir(name,url,2,'')

def VIDEOSHOWIDS(showid,name):
        #All Videos
        #url = "http://www.cbs.com/sitefeeds" + showid + "all.js"
        #Most Popular
        #url = "http://www.cbs.com/sitefeeds" + showid + "popular.js"
        #Latest Videos
        #url = "http://www.cbs.com/sitefeeds" + showid + "recent.js"
        #Full Episodes
        url = "http://www.cbs.com/sitefeeds" + showid + "episodes.js"
        #Clips
        #url = "http://www.cbs.com/sitefeeds" + showid + "clips.js"
        #Seasons
        #url = "http://www.cbs.com/sitefeeds" + showid + "seasons.js"
        #Season Filter
        #"http://www.cbs.com/sitefeeds" + showid + season# + ".js"
        #addDir("Clips",pid,3,thumbnail)
        VIDEOLINKS(url,name)

def VIDEOLINKS(url,name):
        print "VideoLinks " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('videoProperties(.+?);').findall(link)
        for url in match:
                breakurl = url.split("','")
                #  0 = empty
                #  1 = title1
                #  2 = title2
                #  3 = series_title
                #  4 = season_number
                #  5 = description
                #  6 = episode_number
                #  7 = primary_cid
                #  8 = category_type
                #  9 = runtime
                # 10 = pid
                # 11 = marker_thumb 
                # 12 = marker_full
                # 13 = the current category value for the existing show pages
                # 14 = site name in xml, lowercased and trimmed to match the value passed from the left menu
                # 15 = empty
                pid = breakurl[10]
                thumbnail = breakurl[11]
                if breakurl[8] == "Full Episode":
                        finalname = breakurl[3] + " - S" + breakurl[4] + "E" + breakurl[6] + " - " + breakurl[2]
                elif breakurl[8] == "Clip":
                        finalname = breakurl[3] + " - " + breakurl[2] + "(Clip)"
                else:
                        finalname = breakurl[2]
                addDir(finalname,pid,3,thumbnail)

def VIDEORTMP(pid,name):
        url = "http://release.theplatform.com/content.select?format=SMIL&Tracking=true&balance=true&pid=" + pid
        print "VideoLinks " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        if "rtmp://" in link:
                stripurl = re.compile('<ref src="rtmp://(.+?)" ').findall(link)
                cleanurl= stripurl[0].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').split('<break>')
                finalurl = "rtmp://" + cleanurl[0]
                playsplit = cleanurl[1].split('.flv')
                playpath = playsplit[0]
        elif "http://" in link:
                stripurl = re.compile('<ref src="http://(.+?)" ').findall(link)
                finalurl = "http://" + stripurl[0]
                playpath = ""
        print finalurl
        addLink(name,finalurl,'',playpath)


def addLink(name,url,iconimage,playpath):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        swfUrl = "http://www.cbs.com/thunder/player/1_0/chromeless/cbs/CAN.swf"
        liz.setProperty("SWFPlayer", swfUrl)
        liz.setProperty("PlayPath", playpath)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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
        CATEGORIES()
#Series List       
elif mode==1:
        INDEX(url)
#Episode List        
elif mode==2:
        VIDEOSHOWIDS(url,name)
#Episode Play
elif mode==3:
        VIDEORTMP(url,name)
#Most Popular and Recent
elif mode==4:
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
