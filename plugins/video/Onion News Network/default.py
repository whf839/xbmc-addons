#The Onion News Network (tv.theonion.com)default.py
#by rwparris2

import urllib,urllib2,re
import xbmcplugin,xbmcgui,xbmc
from random import choice
from BeautifulSoup import BeautifulStoneSoup,BeautifulSoup

def getLink(site):
    req = urllib2.Request(site)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def addDir(name,url,mode):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addThumbDir(name,url,mode,thumb):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,date,thumb):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png",thumbnailImage="http://www.theonion.com/content/themes/onion/assets/onn/itunes_large.jpg")
    liz.setInfo( type="Video", infoLabels={"Title": name,"Date":date } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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

def showMP4Links(site):
    tree=BeautifulStoneSoup(getLink(site))
    videos=tree.findAll('item')
    for i in range(len(videos)):
        name=videos[i].title.contents[0]
        date=videos[i].pubdate.contents[0]
        p=re.compile('<feedburner:origenclosurelink>.+?file=(.+?)&amp;title.+?</feedburner:origenclosurelink>')
        match=p.findall(str(videos[i]))
        for temp in match:
            url=temp.replace('%2F','/').replace('%3A',':')
            print url
        addLink(str(i+1)+'. '+name,url,date,'')
def showList(url):
    addDir('Play Random',url,8)
    tree=BeautifulSoup(getLink(url))
    videos=tree.findAll('li')
    for i in range(len(videos)):
        li=BeautifulSoup(''.join(str(videos[i])))
        thumb=li('img')[0]['src']
        title=li('a')[1].contents[0].string
        page='http://www.theonion.com'+li('a')[0]['href']
        addThumbDir(str(i+1)+'. '+title,page,2,thumb)

def playRandom(url):
    tree=BeautifulSoup(getLink(url))
    videos=tree.findAll('li')
    li=BeautifulSoup(''.join(str(choice(videos))))
    #li=BeautifulSoup(''.join(str(videos[0])))
    title=li('a')[1].contents[0].string
    page='http://www.theonion.com'+li('a')[0]['href']
    thumb=li('img')[0]['src']
    playItem(page,title,thumb)

def playItem(url,name,thumb):
    b=[]
    link=getLink(url)
    p=re.compile('flashvars=&quot;file=(.*embedded_video)&quot;&gt;')
    match=p.findall(link)
    for a in match:
        link=getLink(a)
    p=re.compile('<enclosure url="(.+?)" type')
    match=p.findall(link)
    for a in match:
        b.append(a)
    for i in range(len(b)):
	p=b[i].rindex('.')
	q=b[i].rindex('/')
	#if (b[i][q:p].isupper()):
        url=b[i]
    addLink(name,url,'',thumb)
	    
        
########################################
params=get_params()
url=None
name=None
mode=None
thumb=None

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
    name=urllib.unquote_plus(params["thumb"])
except:
    pass
if mode==None or url==None or len(url)<1:
    addDir('1. All Videos','http://theonion.com/content/onn/ajax_videolist/onn',1)
    addDir('2. Most Viewed','http://theonion.com/content/onn/ajax_videolist/most_viewed',1)
    addDir('3. O-Span','http://theonion.com/content/onn/ajax_videolist/ospan',1)
    addDir('4. In The Know','http://theonion.com/content/onn/ajax_videolist/in_the_know',1)
    addDir('5. Election \'08','http://theonion.com/content/onn/ajax_videolist/wftwh',1)
    addDir('6. Today Now','http://theonion.com/content/onn/ajax_videolist/today_now',1)
    addDir('7. 25 Most Recent (mp4)','http://feeds.theonion.com/onionnewsnetwork',7)
if mode==1:
    showList(url)
if mode==2:
    playItem(url,name,thumb)
if mode==7:
    showMP4Links(url)
if mode==8:
    playRandom(url)


##################
xbmcplugin.addSortMethod(int(sys.argv[1]), 10)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
