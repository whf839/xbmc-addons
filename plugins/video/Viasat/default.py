import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, time
import cookielib

baseurl = 'http://viastream.player.mtgnewmedia.se'

def getHTML( url, referer, redirect=False):
        try:
                print 'TV3 --> getHTML :: url = ' + url
                cj = cookielib.LWPCookieJar()
                req = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                req.addheaders = [('Referer', referer),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
                response = req.open(url)
                link = response.read()
                response.close()
                reurl = response.geturl()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                if redirect==True:
                        reurl = re.compile('file=(.+?)&').findall(reurl, re.DOTALL)[0]
                        response = req.open(reurl)
                        link = response.read()
                        response.close()
                        return link
                else:
                        return link
def getCHurl(ch, lang):
        furl = 'http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel='
        url = furl + ch + '&country=' +lang
        return url

def CHANNELS():

        nm = 'TV3 Norge'
        tb = 'http://www.carat.no/var/ezflow_site/storage/images/nyheter/tv-kino-radio/tv/fantastisk!!!/1088-4-nor-NO/Fantastisk!!!_articlethumbnail.jpg'
        url = getCHurl('2no', 'no')
        addDir(nm, url, 1, tb)
        nm = 'TV3 Danmark'
        url = getCHurl('2dk', 'dk')
        addDir(nm, url, 1, tb)
        nm = 'TV3 Sverige'
        url = getCHurl('2se', 'se')
        addDir(nm, url, 1, tb)        
        nm = 'Viasat Sport Norge'
        tb = 'http://viastream.player.mtgnewmedia.se/imgbin/territoryimages/noimages/FrontBanners/viasport_front.gif'
        url = getCHurl('1no', 'no')
        addDir(nm, url, 1, tb)
        nm = 'Viasat Sport Danmark'
        tb = 'http://viastream.player.mtgnewmedia.se/imgbin/territoryimages/noimages/FrontBanners/viasport_front.gif'
        url = getCHurl('1dk', 'dk')
        addDir(nm, url, 1, tb)
        nm = 'Viasat Sport Sverige'
        tb = 'http://viastream.player.mtgnewmedia.se/imgbin/territoryimages/noimages/FrontBanners/viasport_front.gif'
        url = getCHurl('1se', 'se')
        addDir(nm, url, 1, tb)
        return
                
def PROGRAMS(url):
        data = getHTML(url,baseurl)
        print 'Fetch program list..'
        programs = re.compile('<siteMapNode title="(.+?)" id="(.+?)" children="(.+?)" articles="(.+?)"/>').findall(data, re.DOTALL)
        for title, progId, children, articles in programs:
                if not children == 'true': continue
                url = url + '&category=' + progId
                addDir(title,url,2,'')
        #return

def EPSGUIDE(url):
        data = getHTML(url,baseurl)
        print 'Fetch navigation..'
        programs = re.compile('<siteMapNode title="(.+?)" id="(.+?)" children="(.+?)" articles="(.+?)"/>').findall(data, re.DOTALL)
        for title, navId, children, articles in programs:
                if int(articles) == 0: continue
                print 'Title: ' + title + ' ID: ' + navId
                url = baseurl + '/xml/xmltoplayer.php?type=Products&category=' + navId
                addDir(title, url,3,'')
        return

def EPISODES(url):
        data = getHTML(url,baseurl)
        print 'Fetch episodes..'
        episodes = re.compile('<ProductId>(.+?)</ProductId>\n\s\s\s\s<Title><!\[CDATA\[(.+?)\]\]></Title>').findall(data, re.DOTALL)
        for epsId, title in episodes:
                url = baseurl + '/xml/xmltoplayer.php?type=Products&clipid=' + epsId
                addDir(title,url,4,'')

def PLAY(url,name):
        data = getHTML(url,baseurl)
        print 'Fetch and play file..'
        videolink = re.compile('<Video>\n.+?\n.+?\n.+?\n.+?<Url>(.+?)</Url>\n.+?</Video>').findall(data, re.DOTALL)[0]
        item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
        item.setInfo( type="Video", infoLabels={ "Title": name})
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(videolink, item)


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
        CHANNELS()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
if mode==1:
        print ""
        PROGRAMS(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        EPSGUIDE(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==3:
        print ""+url
        EPISODES(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==4:
        print ""+url
        PLAY(url,name)




