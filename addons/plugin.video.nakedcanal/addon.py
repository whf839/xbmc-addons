"""
    Plugin for streaming content from NakedCanal.com
"""
# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import re

Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )

def CATEGORIES():
        addDir('All Videos','http://www.nakedcanal.com/videos?c=0',1,'',1)
        addDir('Erotic Videos','http://www.nakedcanal.com/videos?c=1',1,'',1)
        addDir('Hardcore Videos','http://www.nakedcanal.com/videos?c=2',1,'',1)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def SORTMETHOD(url):
        addDir('Most Recent Adult Videos',url+'&o=mr',2,'',1)
        addDir('Being Watched Adult Videos',url+'&o=bw',2,'',1)
        addDir('Most Viewed Adult Videos',url+'&o=mv',2,'',1)
        addDir('Top Rated Adult Videos',url+'&o=tr',2,'',1)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                       
def VIDEOLIST(url,page):
        req = urllib2.Request(url+'&page='+str(page))
        req.add_header('Cookie','splash=1')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="video_box">\s+?<a href="/video/(.+?)/.+?"><img src=".+?" title="(.+?)" alt=".+?" width=".+?" height=".+?" id=".+?" />').findall(link)
        for videoid,name in match:
                videourl=getvideourl(videoid)
                addLink(name,videourl,'http://www.nakedcanal.com/media/videos/tmb/'+videoid+'/1.jpg',len(match))
        if (len(match) == 15):
            addDir('Next Page',url,2,'',page+1)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
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
        liz.setInfo( type="Video", infoLabels={ "Title": name,"MPAA" : "XXX" } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=totalitems)
        return ok


def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "MPAA" : "XXX" } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def getvideourl(videoid):
        url='http://www.nakedcanal.com/media/player/config.php?vkey='+videoid
        req = urllib2.Request(url)
        req.add_header('Cookie','splash=1')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<src>(.+?)\.flv</src>').findall(link)
        videourl = match[0]+'.flv'
        return videourl

def main():
        
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
                CATEGORIES()
               
        elif mode==1:
                SORTMETHOD(url)
                
        elif mode==2:
                VIDEOLIST(url,page)

if __name__ == "__main__":
    main()
