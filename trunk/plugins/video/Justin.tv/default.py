
__scriptname__ = "Justin.tv"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Justin.tv"
__date__ = '2009-05-26'
__version__ = "r1012"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib2 import Request, urlopen, URLError, HTTPError
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
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
	li=xbmcgui.ListItem('(Search)')
	u=sys.argv[0]+"?mode=3"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('(User Search)')
	u=sys.argv[0]+"?mode=5"
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
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(data) >= 36:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		
def runKeyboard():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Search")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	url = 'http://www.justin.tv/search?q='+newStr+'&commit=Search'
	runSearch(url)
		
def runSearch(url):
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	title=re.compile('<a href="(.+?)" class="bold_results">(.+?)</a>\n            \n        </h3>').findall(a)
	thumbs=re.compile('class="li_pic_125o i125x94 lateload" src1="(.+?)" src').findall(a)
	info=re.compile('<p class="description bold_results">\n            (.*?)\n        </p>\n\n        <div class="stats">', re.DOTALL).findall(a)
	x=0
	for url, name in title:
		thumb=thumbs[x]
		name=str(int(x+1)+(10*(page-1)))+'. '+name+' - '+info[x]
		url=url.replace('/','')
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(title) >= 10:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def runKeyboard2():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Enter the exact user name")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	li=xbmcgui.ListItem(newStr)
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(newStr)+"&url="+urllib.quote_plus(newStr)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			
def playVideo(url, name):
	vid='http://usher.justin.tv/find/live_user_' + url + '.xml'
	try:
		req = urllib2.Request(vid)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
	except HTTPError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: Invalid user or not a live feed.')
		return
	a=f.read()
	f.close()
	data=re.compile('<play>(.+?)</play><connect>(.+?)</connect>').findall(a)
	playpath = data[0][0]
	rtmp_url = data[0][1]
	swf='http://www.justin.tv/meta/'+url+'.xml'
	req = urllib2.Request(swf)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data2=re.compile('SWFObject\(\'(.+?)\',').findall(a)
	data3=re.compile('<title>(.*?)</title>').findall(a)
	data4=re.compile('<status>(.*?)</status>').findall(a)
	referer = 'http://www.justin.tv/'+url
	SWFPlayer = data2[0] + '?referer=' + referer + '&userAgent=' + HEADER
	if len(data4) == 0:
		item = xbmcgui.ListItem(data3[0])
	else:
		item = xbmcgui.ListItem(data3[0]+': '+data4[0])
	item.setProperty("SWFPlayer", SWFPlayer)
	item.setProperty("PlayPath", playpath)
	item.setProperty("PageURL", referer)
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
elif mode==3:
	runKeyboard()
elif mode==4:
	runSearch(url)
elif mode==5:
	runKeyboard2()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
