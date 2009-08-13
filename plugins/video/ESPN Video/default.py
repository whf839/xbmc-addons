
__scriptname__ = "XBMC Video Plugin"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/ESPN%20Video"
__date__ = '08-08-2009'
__version__ = "1.2"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'

def showRoot():
		li=xbmcgui.ListItem("Categories")
		u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus("Categories")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("Original Digitals")
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus("Original Digitals")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("TV Shows")
		u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus("TV Shows")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("PodCenter")
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus("PodCenter")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showCategoriesC():
	url='http://espnradio.espn.go.com/espnradio/podcast/index'
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('<div id="videoPodcasts_page1" style="display: block">(.+?)<div id="featuredvideoPodcasts" class="featured-events">', re.DOTALL)
	o=re.compile('<a href="(.+?)"><img src="http://a.espncdn.com/i/espnradio/podcast/images/button_rss.gif"')
	r=re.compile('<img src="(.+?)" width="90"')
	q=re.compile('<div class="playlist-item"><h4>(.+?)</h4>')
	title=p.findall(a)
	urls=o.findall(title[0])
	thumbs=r.findall(title[0])
	names=q.findall(title[0])
	x=0
	count=0
	print thumbs
	for url in urls:
		if url != 'http://sports.espn.go.com/espnradio/podcast/index':
			name1=names[x]
			name = str(int(count+1))+'. '+name1
			thumb=thumbs[x]
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			count=count+1
		x=x+1


def RSS(url):
		print url
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<item>(.+?)<title>(.+?)</title>', re.DOTALL)
		thumbs=re.compile('<url>(.+?)jpg</url>').findall(a)
		o=re.compile('<enclosure url="http://(.+?)\?prm=(.+?)x(.+?)"')
		match=p.findall(a)
		URLS=o.findall(a)
		x=0
		thumb=thumbs[0]+'jpg'
		for title in match:
			name1 = clean(match[x][1])
			name = str(int(x+1))+'. '+name1
			url=URLS[x][2]
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url)+"&plot="+urllib.quote_plus('')+"&cat="+urllib.quote_plus('RSS')
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
		
def showCategoriesB():
		url='http://espn.go.com/video/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('class="expandable">TV Shows</a>(.+?)<a id="link3385449"', re.DOTALL)
		o=re.compile('<a href="javascript:showChannel((.+?))">(.+?)</a></li>')
		title=p.findall(a)
		info=o.findall(title[0])
		x=0
		for url in info:
			num=info[x][0]
			num=num.replace('\'','')
			num=num.replace('(','')
			num=num.replace(')','')
			url='http://espn.go.com/video/beta/libraryPlaylist?categoryid='+num
			test=info[x][2]
			test=test.replace('<img src="http://assets.espn.go.com/i/in.gif"> ','')
			name=test[:-4]
			name=name.replace('(','')
			if (name=='The Latest'):
				name = '> The Latest'
			name=name.replace('<BR>',' ')
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1


def showCategoriesA():
		url='http://espn.go.com/video/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('class="expandable">Original Digitals</a>(.+?)<a id="link2949049"', re.DOTALL)
		o=re.compile('<a href="javascript:showChannel((.+?))">(.+?)</a></li>')
		title=p.findall(a)
		info=o.findall(title[0])
		x=0
		for url in info:
			num=info[x][0]
			num=num.replace('\'','')
			num=num.replace('(','')
			num=num.replace(')','')
			url='http://espn.go.com/video/beta/libraryPlaylist?categoryid='+num
			test=info[x][2]
			test=test.replace('<img src="http://assets.espn.go.com/i/in.gif"> ','')
			name=test[:-3]
			name=name.replace('(','')
			if (name=='The Latest'):
				name = '> The Latest'
			name=name.replace('<BR>',' ')
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showCategories():
		url='http://espn.go.com/video/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('class="expandable">Categories</a>(.+?)<!-- end toc-->', re.DOTALL)
		o=re.compile('<a href="javascript:showChannel((.+?))">(.+?)</a></li>')
		title=p.findall(a)
		info=o.findall(title[0])
		x=0
		for url in info:
			num=info[x][0]
			num=num.replace('\'','')
			num=num.replace('(','')
			num=num.replace(')','')
			url='http://espn.go.com/video/beta/libraryPlaylist?categoryid='+num
			test=info[x][2]
			name=test[:-4]
			name=name.replace('(','')
			if (name=='The Latest'):
				name = '> The Latest'
			name=name.replace('<BR>',' ')
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showListB(url,name):
		print url
		cat_title=name
		thisurl=url
		req = urllib2.Request(url+'&pageNum='+str(int(page))+'&assetURL=http://assets.espn.go.com')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<h5>(.+?)</h5>')
		r=re.compile('<a href="http://(insider.)?espn.go.com/video/clip\?id=(.+?)&categoryid=(.+?)"><img src="(.+?)"')
		title=p.findall(a)
		thumbs=r.findall(a)
		x=0
		for url2 in thumbs:
			name=title[x]
			url='http://sports.espn.go.com/videohub/mpf/config/player/playlist.xml?id=' + thumbs[x][1] + '&player=videoHub09'
			thumb=thumbs[x][3]
			name1 = str(int(x+1+12*int(page)))+'. '+name
			li=xbmcgui.ListItem(name1, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name1 } )
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
		li=xbmcgui.ListItem(xbmc.getLocalizedString( 30004 ),iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(cat_title)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showList(url,name):
		print url
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<headline><!\[CDATA\[(.+?)\]\]></headline>')
		o=re.compile('<caption><!\[CDATA\[(.+?)\]\]></caption>')
		#q=re.compile('<!\[CDATA\[(.+?)\]\]></asseturl>')
		q=re.compile('<mediaid >(.+?)</mediaid>')
		tags=re.compile('<contentcat><!\[CDATA\[(.*?)\]\]></contentcat>').findall(a)
		r=re.compile('<thumbnailurl  onError="/broadband/video/images/thumb_default.gif"><!\[CDATA\[(.+?)\]\]></thumbnailurl>')
		title=p.findall(a)
		info=o.findall(a)
		flv=q.findall(a)
		thumbs=r.findall(a)
		url='http://seavideo-ak.espn.go.com/motion/' + flv[0] + '.flv'
		name=title[0]
		plot=info[0]
		cat=tags[0]
		cat=cat.replace('|',' / ')
		playVideo(url, name, plot, cat)
		
def Update(__version__):
	print "ESPN Video v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/ESPN%20Video/default.py'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	ALL = re.compile('<td class="source">__version__ = &quot;(.+?)&quot;<br></td>').findall(a)
	for link in ALL :
		if link.find(__version__) != 0:
			newVersion=link
			dia = xbmcgui.Dialog()
			ok = dia.ok("ESPN Video", 'Updates are available on SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def clean(name):
    remove=[('&amp;','&'),('&quot;','\"')]
    for old, new in remove:
        name=name.replace(old,new)
    return name
	
def playVideo(url,name,plot,cat):
	title=name
	name=clean_file(name)
	name=name[:+32]
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading',title,'Filename: '+name+ '.flv')
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
		if (xbmcplugin.getSetting('ask_filename') == 'true'):
			searchStr = name
			keyboard = xbmc.Keyboard(searchStr, "Save as:")
			keyboard.doModal()
			if (keyboard.isConfirmed() == False):
				return
			searchstring = keyboard.getText()
			name=searchstring
		flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name + '.flv' ))
		Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
		if (ret == 0):
			if (xbmcplugin.getSetting('ask_filename') == 'true'):
				searchStr = name
				keyboard = xbmc.Keyboard(searchStr, "Save as:")
				keyboard.doModal()
				if (keyboard.isConfirmed() == False):
					return
				searchstring = keyboard.getText()
				name=searchstring
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name + '.flv'))
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
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	listitem=xbmcgui.ListItem(title ,iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	listitem.setInfo( type="Video", infoLabels={ "Title": title, "Director": 'ESPN', "Studio": 'ESPN', "Genre": cat, "Plot": plot } )
	if (flv_file != None and os.path.isfile(flv_file)):
		xbmc.Player(player_type).play(str(flv_file), listitem)
	elif (stream == 'true'):
		xbmc.Player(player_type).play(str(url), listitem)
	xbmc.sleep(200)
	
def clean_file(name):
    remove=[(':',' - '),('\"',''),('|',''),('>',''),('<',''),('?',''),('*','')]
    for old, new in remove:
        name=name.replace(old,new)
    return name

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
page=0
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
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:
		cat=urllib.unquote_plus(params["cat"])
except:
        pass

if mode==None:
	name=''
	if xbmcplugin.getSetting("update") == "true":
		Update(__version__)
	showRoot()
elif mode==1:
	showList(url, name)
elif mode==2:
	playVideo(url, name, plot, cat)
elif mode==3:
	showCategories()
elif mode==4:
	showCategoriesA()
elif mode==5:
	showCategoriesB()
elif mode==6:
	showCategoriesC()
elif mode==7:
	RSS(url)
elif mode==8:
	showListB(url, name)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
