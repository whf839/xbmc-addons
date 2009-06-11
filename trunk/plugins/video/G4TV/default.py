
__scriptname__ = "G4TV"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/G4TV"
__date__ = '2009-06-11'
__version__ = "1.3"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
THUMBNAIL_PATH = os.path.join( os.getcwd(), "thumbnails" )
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
# THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def showRoot():	
		li=xbmcgui.ListItem("TV Shows")
		u=sys.argv[0]+"?mode=1"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li3=xbmcgui.ListItem("G4 Podcasts")
		u3=sys.argv[0]+"?mode=6"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
		li3=xbmcgui.ListItem("G4 Video Index")
		u3=sys.argv[0]+"?mode=10"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)

def videoIn(name,url):
	url='http://g4tv.com/videos/index.html'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	viewstate=re.compile('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />').findall(a)
	validation=re.compile('<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.+?)" />').findall(a)
	drop='-1'
	# if page > 1:
		# results = 'ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$grdSearchResults$ctl103$btnNext'
		# data = urllib.urlencode([('__EVENTTARGET', results),('__EVENTARGUMENT', ''),('__VIEWSTATE', viewstate[0]),('__EVENTVALIDATION', validation[0]),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$ddlCategoryDropDown', drop),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$objSearchWordsTextBox', ''),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$objSearchButton', ''),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$inpSortExpression', '')])
	# else:
	results = 'ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$btnResultsCount4'
	data = urllib.urlencode([('__EVENTTARGET', results),('__EVENTARGUMENT', ''),('__VIEWSTATE', viewstate[0]),('__EVENTVALIDATION', validation[0]),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$ddlCategoryDropDown', drop),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$objSearchWordsTextBox', ''),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$objSearchButton', ''),('ctl00$ctl00$objContentPlaceholder$objContentPlaceholder$inpSortExpression', '')])
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req, data)
	a=f.read()
	f.close()
	data=re.compile('lnkItemTitle" href="javascript:openPile\(\'(.+?)\'\);">(.+?)</a></span>').findall(a)
	thumbs=re.compile('<img src="(.+?)" id="ctl00_ctl00_objContentPlaceholder').findall(a)
	disc=re.compile('lblItemDescription">(.+?)</span>').findall(a)
	show=re.compile('lblShow">(.+?)</span>').findall(a)
	x=0
	for vid,title in data:
		name = str(int(x+1))+'. '+show[x]+': '+title+' - '+disc[x]
		url='http://g4tv.com/xml/broadbandplayerservice.asmx/GetEmbeddedVideo?videoKey='+vid+'&playLargeVideo=true&excludedVideoKeys=&playlistType=normal&maxPlaylistSize=0'
		li=xbmcgui.ListItem(name, iconImage=thumbs[x], thumbnailImage=thumbs[x])
		li.setInfo( type="Video", infoLabels={ "Title": title, "Plot":disc[x] } )
		u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	# if len(data) >= 100:	
		# li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		# u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+str(int(page)+1)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def getID(name,url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('&amp;r=(.+?)</FilePath>')
	data=p.findall(a)
	for flv in data:
		url=flv.replace('%3a', ':')
		url=url.replace('%2f', '/')
	showList2(url)

def showXPLAY():
	links=[
		("Reviews","http://g4tv.com/games/reviews", "http://cache.g4tv.com/images/xplay/logos/xplay_reviews.png"),
		("Previews","http://g4tv.com/games/previews", "http://cache.g4tv.com/images/xplay/logos/xplay_previews.png"),
		("Cheats","http://g4tv.com/games/cheats", "http://cache.g4tv.com/images/xplay/logos/xplay_cheat.png"),
		("Features","http://g4tv.com/games/features", "http://cache.g4tv.com/images/xplay/logos/xplay_features.png"),
		("Trailers","http://g4tv.com/games/trailers", "http://cache.g4tv.com/images/xplay/logos/xplay_trailers.png"),
		("Latest Vidoes","http://g4tv.com/games/videos", "http://cache.g4tv.com/images/xplay/logos/xplay_videos.png")
		]
	for name, url, thumb in links:
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def newShowX(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<div class="thumb">\r\n        <a href="(.+?)" title="(.+?)" rel="(.+?)">\r\n            <img src="(.+?)" alt="(.+?)" />\r\n            <span class="icn-play">', re.DOTALL).findall(a)
		x=0
		for url, name, th, thumb, tras in p:
			name = str(int(x+1))+'. '+name
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus('xplay')+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1

def showCategories():
	url='http://g4tv.com/attackoftheshow/segments.aspx'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('class="thumbnail" href="(.+?)"><img src="(.+?)"')
	thumb=p.findall(a)
	o=re.compile('class="segmentTitle" href="(.+?)">(.+?)</a></div>')
	data=o.findall(a)
	x=0
	for url, name in data:
			thumbs=thumb[x][1]
			#thumbs=thumbs.replace('_LND.jpg', '_HD.jpg')
			li=xbmcgui.ListItem(name, iconImage=thumbs, thumbnailImage=thumbs)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1
	url='http://g4tv.com/attackoftheshow/videos/index.html'
	name='.: Most Recent'
	thumbs='http://media.g4tv.com/podcasts/5_RSS.jpg'
	li=xbmcgui.ListItem(name, iconImage=thumbs, thumbnailImage=thumbs)
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def newShow(url,page):
	#url='http://g4tv.com/attackoftheshow/thefeed/index.html'
	thisurl=url
	find=url
	find=find.rsplit('/')
	test=find[4]
	if (test=='videos'):
		f=urllib2.urlopen(url+'?page='+str(int(page)))
	else:
		url=url.replace('index.html','')
		f=urllib2.urlopen(url+'page'+str(int(page))+'.html')
	#f=urllib2.urlopen(url)
	a=f.read()
	f.close()
	p=re.compile('src="(.+?)" style="height:100px;width:133px;border-width:0px;" /></a>')
	thumb=p.findall(a)
	o=re.compile('href="(.+?)">(.+?)</a></h3>')
	data=o.findall(a)
	x=0
	for url, name in data:
			name = str(int(x+1))+'. '+name[:-3]
			li=xbmcgui.ListItem(name, iconImage=thumb[x], thumbnailImage=thumb[x])
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
			if (x==20):
				break
	li=xbmcgui.ListItem(xbmc.getLocalizedString( 30004 ),iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		
def showList(name, url):
		#url='http://g4tv.com/attackoftheshow/thefeed/65945/The-Daily-Feed-with-Alison-Haislip-122408.html'
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		if name == 'xplay':
			p=re.compile('videokey: \'(.+?)\',')
		else:
			p=re.compile('<input type="hidden" id="entityKey" value="(.+?)" />')
		data=p.findall(a)
		for url in data:
			url='http://g4tv.com/xml/broadbandplayerservice.asmx/GetEmbeddedVideo?videoKey='+url+'&playLargeVideo=true&excludedVideoKeys=&playlistType=normal&maxPlaylistSize=0'
		#url='http://g4tv.com/xml/broadbandplayerservice.asmx/GetEmbeddedVideo?videoKey=35787&playLargeVideo=true&excludedVideoKeys=&playlistType=normal&maxPlaylistSize=0'
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('&amp;r=(.+?)</FilePath>')
		data=p.findall(a)
		for flv in data:
			url=flv.replace('%3a', ':')
			url=url.replace('%2f', '/')
		showList2(url)		

def RSSList():
		url='http://g4tv.com/podcasts/index.html'
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('href="(.+?)"><img title="RSS"')
		o=re.compile('style="background:url(.+?) no-repeat;;')
		q=re.compile('<span>(.+?)</span><br />')
		URLS=p.findall(a)
		thumbs=o.findall(a)
		names=q.findall(a)
		x=0
		for url in URLS:
			thumb=thumbs[x]
			thumb=thumb.replace('(','')
			thumb=thumb.replace('landing.gif)','RSS.jpg')
			thumb=thumb.replace('landing.jpg)','RSS.jpg')
			name = names[x]
			name = name.replace('’', '\'')
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def getRSSLink(url):
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		#p=re.compile('<item>\r\n\t\t\t<title>(.+?)</title>', re.DOTALL)
		p=re.compile('<item>(.+?)<title>(.+?)</title>', re.DOTALL)
		o=re.compile('<link>http://www.podtrac.com/pts/redirect.mp4(.+?)</link>')
		match=p.findall(a)
		URLS=o.findall(a)
		x=0
		for add in URLS:
			names = match[x][1]
			name = str(int(x+1))+'. '+names
			url='http://www.podtrac.com/pts/redirect.mp4'+add
			li=xbmcgui.ListItem(name)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1

def showList2(url):
	date=url
	date=date.rsplit('/')
	name=date[7]
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading','',name)
			urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
	def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
			try:
					percent = min((numblocks*blocksize*100)/filesize, 100)
					dp.update(percent)
			except:
					percent = 100
					dp.update(percent)
			if dp.iscanceled():
					dp.close()
	flv_file = None
	stream = 'false'
	if (xbmcplugin.getSetting('download') == 'true'):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select(xbmc.getLocalizedString( 30005 ), [xbmc.getLocalizedString( 30001 ), xbmc.getLocalizedString( 30007 ), xbmc.getLocalizedString( 30006 )])
		if (ret == 0):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
		elif (ret == 1):
			stream = 'true'
		else:
			pass
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'false'):
		stream = 'true'
	if xbmcplugin.getSetting("dvdplayer") == "true":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
	else:
		player_type = xbmc.PLAYER_CORE_MPLAYER
	if (flv_file != None and os.path.isfile(flv_file)):
		xbmc.Player(player_type).play(str(flv_file))
	elif (stream == 'true'):
		xbmc.Player(player_type).play(str(url))
	xbmc.sleep(200)

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
	showRoot()
elif mode==1:
	#showCategories()
	li=xbmcgui.ListItem("Attack of the Show")
	u=sys.argv[0]+"?mode=9"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li2=xbmcgui.ListItem("X-PLAY")
	u2=sys.argv[0]+"?mode=4"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u2,li2,True)
elif mode==2:
	newShow(url,page)
elif mode==3:
	showList(name,url)
elif mode==4:
	showXPLAY()
elif mode==5:
	newShowX(url)
elif mode==6:
	RSSList()
elif mode==7:
	getRSSLink(url)
elif mode==8:
	showList2(url)
elif mode==9:
	showCategories()
elif mode==10:
	videoIn(name,url)
elif mode==11:
	getID(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
