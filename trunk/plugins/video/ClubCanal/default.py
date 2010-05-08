__plugin__ = "ClubCanal"
__authors__ = "thebitjockey"
__credits__ = ""
__version__ = "1.0.1"

import urllib,urllib2,re,xbmcplugin,xbmcgui

def CATEGORIES():
        addDir('All Music Videos','http://www.clubcanal.com/videos?c=0',1,'',1)
        addDir('Dance and Electronic Music Videos','http://www.clubcanal.com/videos?c=1',1,'',1)
        addDir('Russian Dance Music Vide','http://www.clubcanal.com/videos?c=2',1,'',1)
        addDir('Live Dance Music Videos','http://www.clubcanal.com/videos?c=3',1,'',1)
        addDir('Chillout and Lounge Music Videos','http://www.clubcanal.com/videos?c=4',1,'',1)
        addDir('How To and Interviews Videos','http://www.clubcanal.com/videos?c=5',1,'',1)

def SORTMETHOD(url):
        addDir('Most Recent Music Videos',url+'&o=mr',2,'',1)
        addDir('Being Watched Music Videos',url+'&o=bw',2,'',1)
        addDir('Most Viewed Music Videos',url+'&o=mv',2,'',1)
        addDir('Top Rated Music Videos',url+'&o=tr',2,'',1)
        addDir('Most Commented Music Videos',url+'&o=md',2,'',1)
        addDir('Top Favorite Music Videos',url+'&o=tf',2,'',1)
        
                       
def VIDEOLIST(url,page):
        req = urllib2.Request(url+'&page='+str(page))
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="video_box">\s+?<a href="/video/(.+?)/.+?"><img src=".+?" title="(.+?)" alt=".+?" width=".+?" height=".+?" id=".+?" />').findall(link)
        for videoid,name in match:
                addLink(name,'http://www.clubcanal.com/media/videos/flv/'+videoid+'.flv','http://www.clubcanal.com/media/videos/tmb/'+videoid+'/1.jpg',len(match))
        if (len(match) == 15):
            addDir('Next Page',url,2,'',page+1)
        
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
    
def addLink(name,url,iconimage,totalitems):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=totalitems)
        return ok


def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None
name=None
mode=None
page=1

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
try:
        page=int(params["page"])
except:
        pass

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        SORTMETHOD(url)
        
elif mode==2:
        print ""+url
        VIDEOLIST(url,page)



xbmcplugin.endOfDirectory(int(sys.argv[1]))

