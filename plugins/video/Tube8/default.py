import sys
import xbmc, xbmcgui, xbmcplugin 
import urllib2, urllib, re


# plugin constants
__plugin__ = "Tube 8"
__author__ = "The BIT Jockey"
__url__ = "http://www.tube8.com/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Tube8"
__version__ = "1.4.1"
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "19457"

NB_ITEM_PAGE = 28

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def showRoot(localpath, handle):
		ri=[
			("Latest","http://www.tube8.com/latest/"),
			("Most Viewed","http://www.tube8.com/most-viewed/"),
			("Top Rated","http://www.tube8.com/top/"),
			("Most Favorited","http://www.tube8.com/most-favorited/"),
			("Most Discussed","http://www.tube8.com/most-discussed/"),
			("Most Voted","http://www.tube8.com/most-voted/"),
			("Longest","http://www.tube8.com/longest/"),
			]
		
		li=xbmcgui.ListItem("Search")
		u=localpath+"?mode=4"
		xbmcplugin.addDirectoryItem(handle,u,li,True)
			
		li=xbmcgui.ListItem("Categories")
		u=localpath+"?mode=1"
		xbmcplugin.addDirectoryItem(handle,u,li,True)
		
		for name, url in ri:
			li=xbmcgui.ListItem(name)
			u=localpath+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(handle,u,li,True, NB_ITEM_PAGE)
		
		xbmcplugin.endOfDirectory(handle)

def showCategories(localpath, handle):
		url="http://www.tube8.com/categories.html"
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		
		catMenuRE = re.compile('<ul class="categories-menu">(.+?)</ul>',re.DOTALL)
		match = catMenuRE.search(a)
		if match:
			catMenu = match.group(0)
			p=re.compile('<a href="(http://www\.tube8\.com/cat/.+?)">(.+?)</a>')
			match=p.findall(catMenu)
			for url,name in match:
				li=xbmcgui.ListItem(name)
				u=localpath+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle,u,li,True,NB_ITEM_PAGE)
		xbmcplugin.endOfDirectory(handle)

def showSearchList(localpath, handle, url, page):
	pageUrl = url+"&page="+str(int(page))
	showListCommon(localpath, handle, pageUrl)
	name = "Next Page"
	li=xbmcgui.ListItem(name)
	u=localpath+"?mode=5&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+str(int(page)+1)
	xbmcplugin.addDirectoryItem(handle,u,li,True, NB_ITEM_PAGE)
	xbmcplugin.endOfDirectory(handle)
	
def showCatList(localpath, handle, url, page):
	pageUrl = url+"page/"+str(int(page))+"/"
	showListCommon(localpath, handle, pageUrl)
	name = "Next Page"
	li=xbmcgui.ListItem(name)
	u=localpath+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+str(int(page)+1)
	xbmcplugin.addDirectoryItem(handle,u,li,True, NB_ITEM_PAGE)
	xbmcplugin.endOfDirectory(handle)

def showListCommon(localpath, handle, pageUrl):
		print "Opening page: " + pageUrl
		f=urllib2.urlopen(pageUrl)
		a=f.read()
		f.close()
		
		videosRE = '<img .+? class="videoThumbs".+?src="(.+?)".+?<h2><a href="(.+?)" title="(.+?)">.+?</a></h2>.*?<span.*?>(([0-9]{2}:)?[0-9]{2}:[0-9]{2})</span>'
		videoPattern = re.compile(videosRE, re.DOTALL)
#		videosRE = '<img width="160" height="120" .+?src="(.+?)" /></a>\n\t\t\t\t\t<h2><a href="(.+?)" title="(.+?)">'
#		videoPattern = re.compile(videosRE)
		
		match=videoPattern.findall(a)
		for thumb, url, name, duration,_ in match:
			li=xbmcgui.ListItem(name,name,thumb,thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name, "Duration": duration  } )
			u=localpath+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(handle,u,li, False, NB_ITEM_PAGE)

def playVideo(localpath, handle, url):
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		
		p=re.compile("flashvars.videoUrl = '(.+?)';")
		match=p.search(a)
		if match:
			video = match.group(1)
			print "Playing: " + video
			if xbmcplugin.getSetting("dvdplayer") == "true":
				xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(video)
			else:
				xbmc.Player().play(video)
		
def get_params(args):
	param=[]
	print "Parsing arguments: " + str(args)
	paramstring=args[2]
	if len(paramstring)>=2:
		params=args[2]
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

def search_videos(localpath, handle):
	searchUrl = "http://www.tube8.com/search.html?q="
	vq = _get_keyboard( heading="Enter the query" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title
	print "Searching URL: " + searchUrl
	showSearchList(localpath, handle, searchUrl, 1)

if __name__ == "__main__":
	params=get_params(sys.argv)
	mode=None
	name=None
	url=None
	page=1
	search = False
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
	try:
		search=bool(params["search"])
	except:
		pass
	
	if mode==None:
		showRoot(sys.argv[0],int(sys.argv[1]))
	elif mode==1:
		showCategories(sys.argv[0],int(sys.argv[1]))
	elif mode==2:
		showCatList(sys.argv[0], int(sys.argv[1]), url, page)
	elif mode==5:
		showSearchList(sys.argv[0], int(sys.argv[1]), url, page)
	elif mode==3:
		playVideo(sys.argv[0], int(sys.argv[1]), url)
	elif mode==4:
		search_videos(sys.argv[0], int(sys.argv[1]))
