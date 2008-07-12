import urllib,urllib2,re,xbmcplugin,xbmcgui
#SWEDISH MEDIA PLUGIN V2008.

def INDEXCATS():
        addDir("1. TV3","http://www.noneed.com",1,"http://upload.wikimedia.org/wikipedia/en/thumb/5/59/Tv3sweden.svg/150px-Tv3sweden.svg.png")
        addDir( "2. TV6","http://www.noneed.com",2,"http://www.lyngsat-logo.com/logo/tv/vv/viasat_tv6_se.jpg")
        addDir( "3. TV8","http://www.noneed.com",3,"http://www.lyngsat-logo.com/logo/tv/vv/viasat_tv8.jpg")
        addDir("4. SPORT SWEDEN","http://www.noneed.com",4,"http://www.goalzz.com/images/tv/viasat.jpg")
        addDir("5. SING-A-LONG","http://www.noneed.com",5,"http://www.viasat-uk.net/viasat.jpg")

def INDEXTV3():
        res=[]
        channels = open ('Q:/plugins/video/Viasat/channels.ini')
        link=channels.read()
        channels.close() 
        p=re.compile('<STATION>TV3<STATION><SHOWNAME>(.+?)<SHOWNAME><URL>(.+?)<URL><THUMBNAIL>(.+?)<THUMBNAIL>\n')
        match=p.findall(link)
        for showname,url,thumbnail in match:
                res.append((showname,url,thumbnail))
        for showname,url,thumbnail in res:
                addDir(showname,url,6,thumbnail)
def INDEXTV6():
        res=[]
        channels = open ('Q:/plugins/video/Viasat/channels.ini')
        link=channels.read()
        channels.close() 
        p=re.compile('<STATION>TV6<STATION><SHOWNAME>(.+?)<SHOWNAME><URL>(.+?)<URL><THUMBNAIL>(.+?)<THUMBNAIL>\n')
        match=p.findall(link)
        for showname,url,thumbnail in match:
                res.append((showname,url,thumbnail))
        for showname,url,thumbnail in res:
                addDir(showname,url,6,thumbnail)

def INDEXTV8():
        res=[]
        channels = open ('Q:/plugins/video/Viasat/channels.ini')
        link=channels.read()
        channels.close() 
        p=re.compile('<STATION>TV8<STATION><SHOWNAME>(.+?)<SHOWNAME><URL>(.+?)<URL><THUMBNAIL>(.+?)<THUMBNAIL>\n')
        match=p.findall(link)
        for showname,url,thumbnail in match:
                res.append((showname,url,thumbnail))
        for showname,url,thumbnail in res:
                addDir(showname,url,6,thumbnail)

def INDEXSPORT():
        res=[]
        channels = open ('Q:/plugins/video/Viasat/channels.ini')
        link=channels.read()
        channels.close() 
        p=re.compile('<STATION>SPORT<STATION><SHOWNAME>(.+?)<SHOWNAME><URL>(.+?)<URL><THUMBNAIL>(.+?)<THUMBNAIL>\n')
        match=p.findall(link)
        for showname,url,thumbnail in match:
                res.append((showname,url,thumbnail))
        for showname,url,thumbnail in res:
                addDir(showname,url,6,thumbnail)
                
def INDEXSING():
        res=[]
        channels = open ('Q:/plugins/video/Viasat/channels.ini')
        link=channels.read()
        channels.close() 
        p=re.compile('<STATION>SING<STATION><SHOWNAME>(.+?)<SHOWNAME><URL>(.+?)<URL><THUMBNAIL>(.+?)<THUMBNAIL>\n')
        match=p.findall(link)
        for showname,url,thumbnail in match:
                res.append((showname,url,thumbnail))
        for showname,url,thumbnail in res:
                addDir(showname,url,6,thumbnail)
                
def EPISODES(url):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        fix=re.sub('\xc3\xb6','o',link)
        fix2=re.sub('&ouml;','',fix)
        fix3=re.sub('&nbsp;',' ',fix2)
        fix4=re.sub('&auml;','a',fix3)
        response.close()
        p=re.compile('<a href=".+?href = \'(.+?)\'.+?href = \'.+?\';">(.+?)</a></td>\r\n\t\t\t\t\t\t<td align="right"><img src=".+?" alt=".+?" hspace="2"> </td>\r\n\t\t\t\t\t</tr>\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<td valign="top" class="verdana10" style=" padding-left:5px">\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t<br/>\t\t\t\t\t\t  \r\n\t\t\t\t\t\t(.+?)<br/>')
        match=p.findall(fix4)
        for urla,name1,name2 in match:
                code=re.sub('episode.php','video.php',urla)
                url='http://viastream.player.mtgnewmedia.se/'+code
                res.append((name1+' '+name2,url))
        for name,url in res:
                addDir(name,url,7,"")

def VIDEOLINKS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\n\t\t\t\t\tpluginspage="http://www.microsoft.com/Windows/MediaPlayer/"\n\t\t\t\t\tsrc="(.+?)"\n\t\t\t\t\t')
        match=p.findall(link)
        for link1 in match:
                main="http://viastream.player.mtgnewmedia.se/"+link1
        req = urllib2.Request(main)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link2=response.read()
        response.close()
        p=re.compile('<Ref HREF = "mms://(.+?)"/>\n')
        match=p.findall(link2)
        for vid in match:
                final="http://"+vid
        addLink("WATCH PROGRAM",final,"")


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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


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
        print "index of categories"
        INDEXCATS()
elif mode==1:
        print "CATEGORY INDEX : "
        INDEXTV3()
elif mode==2:
        print "CATEGORY INDEX : "
        INDEXTV6()
elif mode==3:
        print "CATEGORY INDEX : "
        INDEXTV8()
elif mode==4:
        print "CATEGORY INDEX : "
        INDEXSPORT()
elif mode==5:
        print "CATEGORY INDEX : "
        INDEXSING()
elif mode==6:
        print "GET VIDEO LINK: "+url
        EPISODES(url)
elif mode==7:
        print "GET VIDEO LINK: "+url
        VIDEOLINKS(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
