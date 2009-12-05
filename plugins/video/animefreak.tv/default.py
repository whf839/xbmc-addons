import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os

baseurl = 'http://www.animefreak.tv'
showsurl = 'http://www.animefreak.tv/book'


def getHTML( url ):
        try:
                print 'animefreak --> common :: getHTML :: url = '+url
                req = urllib2.Request(url)
                req.addheaders = [('Referer', 'http://www.animefreak.tv'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                return link

def CATEGORIES():
        items = getHTML(showsurl)
        items = re.sub('\r', ' ', items)
        items = re.sub('\n', ' ', items)
        items = re.sub('\t', ' ', items)
        topmenu=re.compile('<h1>Anime List</h1>(.+?)</ul>').findall(items)
        del items
        match=re.compile('<a href="(.+?)">(.+?)</a></li>').findall(topmenu[0])
        del topmenu
        for category,name in match:
                name = name.replace('&amp;','&').replace('&#039;',"'")
                category = baseurl + category
                thumbsplit = name.split(' ')
                thumb = 'http://www.animefreak.tv/infologos/infologo' + thumbsplit[0].lower() + '.jpg'
                addDir(str(name),category,1,thumb)
        return



def INDEX(url,name):
        showname = name
        items = getHTML(url)
        items = re.sub('\r', '', items)
        items = re.sub('\n', '', items)
        items = re.sub('\t', '', items)
        topmenu=re.compile('<ul class="menu"><li class="leaf first">(.+?)</ul>').findall(items)
        if topmenu == []:
                topmenu=re.compile('<ul class="menu"><li class="collapsed first">(.+?)</ul>').findall(items)
                match=re.compile('<a href="(.+?)">(.+?)</a>').findall(topmenu[0])
                for episode,name in match:
                        name = name.replace('&amp;','&').replace('&#039;',"'")
                        if name == 'Blogs':
                                VIDEOLINKS(url,showname)
                                return
                        elif name == 'Extras':
                                pass
                        else:
                                episode = baseurl + episode
                                addDir(str(name),episode,1,'')
                xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        else:
                match=re.compile('<a href="(.+?)">(.+?)</a>').findall(topmenu[0])
                for episode,name in match:
                        name = name.replace('&amp;','&').replace('&#039;',"'")
                        episode = baseurl + episode
                        addDir(str(name),episode,2,'')
                xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))        
        return



def VIDEOLINKS(url,name):
        items = getHTML(url)
        match=re.compile('&captions=.+?(&image=.+?)?&file=(http://.+?vid_.+?)&').findall(items)
        for _,url in match:
                item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
                item.setInfo( type="Video",infoLabels={ "Title": name
                                              #"Season": season,
                                              #"Episode": episode,
                                              #"Duration": duration,
                                              #"Plot": plot,
                                             })
                stream = httpDownload(url,name)
                if stream == 'false':
                        return
                if xbmcplugin.getSetting("dvdplayer") == "true":
                        player_type = xbmc.PLAYER_CORE_DVDPLAYER
                else:
                        player_type = xbmc.PLAYER_CORE_MPLAYER
                ok=xbmc.Player(player_type).play(url, item)
        return


        
def httpDownload( finalurl, name):
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
        if (xbmcplugin.getSetting('download') == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select(xbmc.getLocalizedString( 30011 ),[xbmc.getLocalizedString( 30006 ),xbmc.getLocalizedString( 30007 ),xbmc.getLocalizedString( 30008 ),xbmc.getLocalizedString( 30012 )])
                if (ret == 0):
                        stream = 'true'
                elif (ret == 1):
                        flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                        Download(finalurl,flv_file)
                elif (ret == 2):
                        flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                        Download(finalurl,flv_file)
                        stream = 'true'
                else:
                        return stream
        #Play
        elif (xbmcplugin.getSetting('download') == '1'):
                stream = 'true'
        #Download
        elif (xbmcplugin.getSetting('download') == '2'):
                flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                Download(finalurl,flv_file)
        #Download & Play
        elif (xbmcplugin.getSetting('download') == '3'):
                flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
                Download(finalurl,flv_file)
                stream = 'true'            
        if (flv_file != None and os.path.isfile(flv_file)):
                finalurl =str(flv_file)
        return stream


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


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),cacheToDisc=True)
        
elif mode==1:
        print ""+url
        INDEX(url,name)
                
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)




