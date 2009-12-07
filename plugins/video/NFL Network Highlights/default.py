
__plugin__ = "NFL Network"
__author__ = "MDPauley"
__url__ = ""
__version__ = "2.0.0"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

def catInitial():
	addDir('Shows','http://www.mdpauley.com/feeds/nfl/show_names?shows=1', 10 , '')
	addDir('Teams','http://www.mdpauley.com/feeds/nfl/show_names?teams=1', 20 , '')
	addDir('Spotlight', 'http://www.mdpauley.com/feeds/nfl/show_names?spotlight=1', 40, '')
	addDir('Events', 'http://www.mdpauley.com/feeds/nfl/show_names?events=1', 50, '')
	
def catShows():
	req = urllib2.Request('http://www.mdpauley.com/feeds/nfl/show_names?shows=1')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	response.close()
	p=re.compile('<item><title>(.+?)</title><description>(.+?)</description><media:content url="(.+?)" type="video/mp4" /><media:thumbnail url="" /><boxee:property name="Image0"></boxee:property></item>')
	match=p.findall(link)
        for title, description, url in match:
        	url=re.sub('rss://', 'http://', url)
        	addDir(title, url, 500 , '')	

def catTeams():
	req = urllib2.Request('http://www.mdpauley.com/feeds/nfl/show_names?teams=1')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	response.close()
	p=re.compile('<item><title>(.+?)</title><description>(.+?)</description><media:content url="(.+?)" type="video/mp4" /><media:thumbnail url="(.+?)" /><boxee:property name="Image0">(.+?)</boxee:property></item>')
	match=p.findall(link)
        for title, description, url, image0, image1 in match:
        	url=re.sub('rss://', 'http://', url)
        	addDir(title, url, 500 , '')

def catSpotlight():
	req = urllib2.Request('http://www.mdpauley.com/feeds/nfl/show_names?spotlight=1')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	response.close()
	p=re.compile('<item><title>(.+?)</title><description>(.+?)</description><media:content url="(.+?)" type="video/mp4" /><media:thumbnail url="" /><boxee:property name="Image0"></boxee:property></item>')
	match=p.findall(link)
        for title, description, url in match:
        	url=re.sub('rss://', 'http://', url)
        	addDir(title, url, 500 , '')

def catEvents():
	req = urllib2.Request('http://www.mdpauley.com/feeds/nfl/show_names?events=1')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	response.close()
	p=re.compile('<item><title>(.+?)</title><description>(.+?)</description><media:content url="(.+?)" type="video/mp4" /><media:thumbnail url="" /><boxee:property name="Image0"></boxee:property></item>')
	match=p.findall(link)
        for title, description, url in match:
        	url=re.sub('rss://', 'http://', url)
        	addDir(title, url, 500 , '')

def listvideos(data):
	res=[]
        req = urllib2.Request(data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<item><title>(.+?)</title><description>(.+?)</description><media:content url="(.+?)" type="video/mp4" /><media:thumbnail url="(.+?)" /><boxee:property name="Image0">(.+?)</boxee:property></item>')
        match=p.findall(link)
        for title, description, url, thumbnail, image0 in match:   
		videoinfo = {'Title': title, "Date": "2009-01-01", 'Plot': description, 'Genre': 'Sports'}
		addLink(url, image0, title, videoinfo)

def addLink(url, thumb, name, info):
	ok=True
	liz=xbmcgui.ListItem( name, iconImage="DefaultVideo.png", thumbnailImage= thumb )
	liz.setInfo( type="Video", infoLabels=info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage, plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	if plot:
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def getParams():
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

#grab params and assign them if found
params=getParams()
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

#check $mode and execute that mode
if mode==None or url==None or len(url)<1:
    print "CATEGORY INDEX : "
    catInitial()
elif mode==10:
    catShows()
elif mode==20:
    catTeams()
elif mode==30:
    catHighlights()
elif mode==40:
    catSpotlight()
elif mode==50:
    catEvents()
elif mode==500:
    listvideos(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
