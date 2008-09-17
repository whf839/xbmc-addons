#2008091700
"""
    TED Talks
        by rwparris
"""
#imports
import sys

__script__ = "TEDTalks"
__version__ = "1.0"

import xbmc,xbmcgui,xbmcplugin
import urllib,urllib2,re
import resources.lib.feedparser as feedparser


##############################################
def get_settings():
    settings = {}
    try:        
            settings['video_quality'] =  xbmcplugin.getSetting( 'video_quality' )
            return settings
    except:
            print "couldn't load settings"
            pass

def getLink(site):
    req = urllib2.Request(site)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def addFullDir(name,url,mode,plot,thumb):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":plot} )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir(name,url,mode):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,date):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
    liz.setInfo( type="Video", infoLabels={"Title": name,"Date":date } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addFullLink(name,url,plot,date,year,genre,author,episode):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
    liz.setInfo( type="Video", infoLabels={"Title":name,"Studio":"Ted","Writer":author,"Plot":plot,"Date":date,"Year":year,"Genre":genre,"Episode":episode } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def checkHD(vid):
    p = vid.rindex('.')
    vid_tmp=vid[:p] + '_480.' + vid[p+1:]
    for i in range(len(d_HD.entries)):
        if d_HD.entries[i].has_key('enclosures'):
            if vid_tmp==d_HD.entries[i].enclosures[0].href:
                vid=vid_tmp
    return vid

def checkAU(vid):
    try:
        p=vid.rindex('-')
        vid_tmp=vid[:p]+'.mp3'
    except:
        p=vid.rindex('.')
        vid_tmp=vid[:p]+'.mp3'
    for i in range(len(d_AU.entries)):
        if d_AU.entries[i].has_key('enclosures'):
            if vid_tmp==d_AU.entries[i].enclosures[0].href:
                vid=vid_tmp
    return vid

def listMedia(url,mode):
    talks=[]
    talks.append(xbmc.getLocalizedString(30010))
    d=feedparser.parse(url)
    for i in range(len(d.entries)):
        if d.entries[i].has_key('title'):
            p=re.compile('TEDTalks : ') #remove tedtalks from title    
            name=p.sub('',d.entries[i].title)
        else:
            name=''
        if d.entries[i].has_key('enclosures'):
            vid=d.entries[i].enclosures[0].href
            if mode==3 and settings['video_quality']=='0':
                vid=checkHD(vid)
            elif mode==3 and settings['video_quality']=='2':
                vid=checkAU(vid)
        else:
            vid=''
        if d.entries[i].has_key('summary'):
            q=re.compile('<img .* />') #remove useless image tag from summary
            plot=q.sub('',d.entries[i].summary)
            plot=plot+'\n'+vid
            
        else:
            plot=''
        if d.entries[i].has_key('date'):
            date_p=d.entries[i].date_parsed
            date=str(date_p[2])+'/'+str(date_p[3])+'/'+str(date_p[0])#date ==dd/mm/yyyy
        else:
            date_p=''
            date=''
        if d.entries[i].has_key('category'):
            genre=d.entries[i].category
        else:
            genre=''
        if d.entries[i].has_key('author'):
            author=d.entries[i].author
        else:
            author=''
        ep=i+1
        talk=[]
        talk=(name,vid,plot,date,date_p[0],genre,author,ep)
        talks.append(talk)
        addFullLink(name,vid,plot,date,date_p[0],genre,author,ep)
    return talks


        
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

########################################
params=get_params()
url=None
name=None
mode=None
settings=get_settings()
#streams:
themes='http://www.ted.com/index.php/themes/atoz'
hdFeed='http://feeds.feedburner.com/TedtalksHD'
sdFeed='http://feeds.feedburner.com/tedtalks_video'
auFeed='http://feeds.feedburner.com/tedtalks_audio'
try:
    url=urllib.unquote_plus(params["url"])
    print 'url: ',url
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
    print 'name: ',name
except:
    pass
try:
    mode=int(params["mode"])
    print 'mode: ',mode
except:
    pass
if mode==None or url==None or len(url)<1:
    #Browse All
    if(settings['video_quality']=='0'):
        feedUrl=hdFeed
    elif(settings['video_quality']=='1'):
        feedUrl=sdFeed
    elif(settings['video_quality']=='2'):
        feedUrl=auFeed
        #set content info
    d=feedparser.parse(feedUrl)
    plot=xbmc.getLocalizedString(30004)
    thumb='http://images.ted.com/images/ted/474_291x218.jpg'
    addFullDir(xbmc.getLocalizedString(30031),feedUrl,1,plot,thumb)
    #Browse by Theme
    theme_thumb='http://images.ted.com/images/ted/481_291x218.jpg'
    theme_plot=xbmc.getLocalizedString(30003)
    addFullDir(xbmc.getLocalizedString(30030),themes,2,theme_plot,theme_thumb)
if mode==1:
    #list all Talks
    listMedia(url,mode)
if mode==2:
    #list all themes
    link=getLink(themes)
    p=re.compile('<li><a href="(/index\.php/themes.+?)">(.+?)</a></li>')
    items=p.findall(link)
    for i in range(len(items)):
        feedUrl='http://ted.com'+items[i][0]
        addDir(items[i][1],feedUrl,3)
if mode==3:
    #list all talks from a theme
    link=getLink(url)
    p=re.compile('alternate" href="(.*)" type')
    match=p.findall(link)
    p=re.compile('//')
    match=p.sub('//www.',match[0])
    if settings['video_quality']=='0':
        d_HD=feedparser.parse(hdFeed)
    elif settings['video_quality']=='2':
        d_AU=feedparser.parse(auFeed)
    talks=listMedia(match,mode)
##################
xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmcplugin.addSortMethod(int(sys.argv[1]), 20)#episode
xbmcplugin.addSortMethod(int(sys.argv[1]),  3)#date
xbmcplugin.addSortMethod(int(sys.argv[1]), 10)#title
xbmcplugin.endOfDirectory(int(sys.argv[1]))
sys.modules.clear()
