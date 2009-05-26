
__scriptname__ = "Justin.tv"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Justin.tv"
__date__ = '2009-05-26'
__version__ = "r1010"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def showCategories():
	url='http://www.justin.tv/directory?order=hot&lang=en'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div id="category_chooser">(.+?)<div class="section">', re.DOTALL).findall(a)
	cat=re.compile('<a href="(.+?)" class="category_link">(.+?)</a> \n                    (.+?)\n').findall(match[0])
	all=re.compile('<span class=\'not_linked\'>All</span> \n            (.+?)\n').findall(match[0])
	name = 'All '+all[0]
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	for url,name,total in cat:
		url='http://www.justin.tv' + url
		li=xbmcgui.ListItem(name+' '+total.lstrip())
		u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showSubCategories(url, name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div id="subcategory_chooser">(.+?)<div id="category_chooser">', re.DOTALL).findall(a)
	cat=re.compile('<a href="(.+?)" class="category_link">(.+?)</a> \n                    (.+?)\n').findall(match[0])
	all=re.compile('<span class=\'not_linked\'>All</span> \n            (.+?)\n').findall(match[0])
	name = 'All '+all[0].lstrip()
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	for url,name,total in cat:
		url='http://www.justin.tv' + url
		li=xbmcgui.ListItem(name+' '+total.lstrip())
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showLinks(url, name):
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div class="grid_item_container"(.+?)<div id="pagelinks">', re.DOTALL).findall(a)
	cat=re.compile('<h3 class="title"(.+?)<a href="(.+?)">(.*?)</a>', re.DOTALL).findall(match[0])
	data=re.compile('<a href="(.+?)"><img alt="" class="li_pic_125o i125x94 lateload" src1="(.+?)"').findall(a)
	x=0
	for url,thumb in data:
		name=str(int(x+1)+(36*(page-1)))+'. '+cat[x][2]
		url=url.replace('/','')
		url='http://usher.justin.tv/find/live_user_' + url + '.xml'
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(data) >= 36:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			
def playVideo(url, name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<play>(.+?)</play><connect>(.+?)</connect>').findall(a)
	playpath = data[0][0]
	rtmp_url = data[0][1]
	SWFPlayer = "http://www-cdn.justin.tv/widgets/jtv_live.rb118c40399aaad71499b437a1ed952cb396c60d4.swf"
	item = xbmcgui.ListItem("Justin.tv")
	item.setProperty("SWFPlayer", SWFPlayer)
	item.setProperty("PlayPath", playpath)
	item.setProperty("PageURL", "http://www.justin.tv/")
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp_url, item)

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
mode=None
name=None
url=None
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

if mode==None:
	showCategories()
elif mode==0:
	showSubCategories(url, name)
elif mode==1:
	showLinks(url, name)
elif mode==2:
	playVideo(url, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
