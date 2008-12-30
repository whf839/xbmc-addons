# XBMC Video Plugin
# NBA.com Videos
# Updated: 12/18/08 - 1:56PM
# ver. 1.01
# Author: stacked < http://xbmc.org/forum/member.php?u=26908 >

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

def showRoot():
		li=xbmcgui.ListItem("Teams")
		u=sys.argv[0]+"?mode=5"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/video_whatsnew.txt"
		li3=xbmcgui.ListItem("What's New")
		u3=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
		url2="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/video_channel_top_plays.txt"
		li4=xbmcgui.ListItem("Top Plays")
		u4=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url2)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u4,li4,True)

def showTeams():
		li=xbmcgui.ListItem("Team Highlights")
		u=sys.argv[0]+"?mode=1"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li2=xbmcgui.ListItem("Team Originals")
		u2=sys.argv[0]+"?mode=4"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u2,li2,True)
		
def showCategories():
		url="http://www.nba.com/video/teams/index.html"
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('team&amp;q=(.+?)">(.+?)</option>')
		match=p.findall(a)
		for url,name in match:
			url = 'http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/teams/video_nba_'+url+'_tab1.txt'
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showCategories2():
		url="http://www.nba.com/video/teams/index.html"
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('team&amp;q=(.+?)">(.+?)</option>')
		match=p.findall(a)
		for url,name in match:
			url = 'http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/teams/video_nba_'+url+'_tab2.txt'
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showList(url,page):
		thisurl=url
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('<img src="(.+?)"><span class="nbaSpanOverlay"></span></div></a><a href="javascript:changePlaylist(''(.+?)'');" class="nbaVideoGridContentHeader">(.+?)</a><div class="nbaVideoGridTextBlock">(.+?)</div>')
		URLS=p.findall(a)
		x=0
		for thumb, url, url2, name, info in URLS:
			name = str(int(x+1))+'. '+name
			url=url.replace('(','')
			url=url.replace(')','')
			remove = "'"
			url=url.replace(remove,'')
			url=url.replace('/video/','')
			url=url.replace('.json','')
			url = 'http://nba.cdn.turner.com/nba/big/' + url + '_nba_576x324.flv'
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name+' - '+info } )
			u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
			
def playVideo(url, name):
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading','',url)
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
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name + '.flv'))
			Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
		if (ret == 0):
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
	showCategories()
elif mode==2:
	showList(url,page)
elif mode==3:
	playVideo(url, name)
elif mode==4:
	showCategories2()
elif mode==5:
	showTeams()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
