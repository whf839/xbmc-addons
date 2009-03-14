# XBMC Video Plugin
# ESPN Video
# Date: 02/01/09
# Author: stacked < http://xbmc.org/forum/member.php?u=26908 >
# Changelog & More Info: http://xbmc.org/forum/showthread.php?p=277591

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

def showRoot():
		li=xbmcgui.ListItem("Categories")
		u=sys.argv[0]+"?mode=3"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("Original Digitals")
		u=sys.argv[0]+"?mode=4"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("TV Shows")
		u=sys.argv[0]+"?mode=5"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem("PodCenter")
		u=sys.argv[0]+"?mode=6"
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
		print thumbs
		for url in urls:
			name1=names[x]
			name = str(int(x+1))+'. '+name1
			thumb=thumbs[x]
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def RSS(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<item>(.+?)<title>(.+?)</title>', re.DOTALL)
		o=re.compile('<enclosure url="(.+?)"')
		match=p.findall(a)
		URLS=o.findall(a)
		x=0
		for title in match:
			name1 = match[x][1]
			name = str(int(x+1))+'. '+name1
			url=URLS[x]
			li=xbmcgui.ListItem(name)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
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
			name=test[:-4]
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
			if (name=='The Latest '):
				name = '> The Latest'
			name=name.replace('<BR>',' ')
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showListB(url,name):
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
			url='http://sports.espn.go.com/broadband/mpf/config/player/playlist.xml?id=' + thumbs[x][1]
			thumb=thumbs[x][3]
			name1 = str(int(x+1))+'. '+name
			li=xbmcgui.ListItem(name1, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name1 } )
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
		li=xbmcgui.ListItem(xbmc.getLocalizedString( 30004 ))
		u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showList(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<headline><!\[CDATA\[(.+?)\]\]></headline>')
		o=re.compile('<caption><!\[CDATA\[(.+?)\]\]></caption>')
		q=re.compile('<asseturl ><!\[CDATA\[(.+?)\]\]></asseturl>')
		r=re.compile('<thumbnailurl  onError="/broadband/video/images/thumb_default.gif"><!\[CDATA\[(.+?)\]\]></thumbnailurl>')
		title=p.findall(a)
		info=o.findall(a)
		flv=q.findall(a)
		thumbs=r.findall(a)
		url='http://seavideo-ak.espn.go.com/motion/' + flv[0]
		name=title[0]
		playVideo(url, name)
			
def playVideo(url, name):
	vid = url
	vid2 = vid
	vid = vid.rsplit('/')
	ck = vid2.rsplit('.')
	if (ck[0] == 'http://podloc'):
		name = vid[12]
	else:
		name = vid[4]
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

if mode==None:
	showRoot()
elif mode==1:
	showList(url, name)
elif mode==2:
	playVideo(url, name)
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

xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
