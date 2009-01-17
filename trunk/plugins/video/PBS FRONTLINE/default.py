# XBMC Video Plugin
# PBS FRONTLINE
# Date: 01/17/08
# ver. 1.00
# Author: stacked < http://xbmc.org/forum/member.php?u=26908 >

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

def showCategories():
		url='http://www.pbs.org/wgbh/pages/frontline/view/'
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('xmlfile: (.+?),')
		match=p.findall(a)
		part=match[0]
		part=part.replace('\'','')
		url='http://www.pbs.org/wgbh/pages/frontline/view/xml/'+part+'.xml'
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('<dsc><!\[CDATA\[(.+?)\]\]></dsc>')
		o=re.compile('dat="(.+?)" ext')
		q=re.compile('num="(.+?)" cat')
		r=re.compile('<tit><!\[CDATA\[(.+?)\]\]></tit>')
		name=r.findall(a)
		info=p.findall(a)
		date=o.findall(a)
		num=q.findall(a)
		x=0
		for numid in num:
			name2 = str(int(x+1))+'. '+date[x]+': '+name[x]+' - '+info[x]
			thumb='http://www.pbs.org/frontline/art/viewimages/200/'+numid+'.jpg'
			url='http://www.pbs.org/wgbh/pages/frontline/video/flv/xml/frol/'+numid+'.xml'
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name[x])+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showList(url,name):
		eps=name
		f=urllib2.urlopen(url)
		a=f.read()
		f.close()
		p=re.compile('<description><!\[CDATA\[(.+?)\]\]></description>')
		o=re.compile('package id="(.+?)" airdate')
		r=re.compile('<title><!\[CDATA\[(.+?)\]\]></title>')
		title=r.findall(a)
		info=p.findall(a)
		numid=o.findall(a)
		x=0
		for name in title:
			thumb='http://www.pbs.org/wgbh/pages/frontline/video/flv/thumbs/200/'+numid[0]+'/'+str(int(x+1))+'.jpg'
			url='http://www-tc.pbs.org/wgbh/pages/frontline/video/flv/'+numid[0]+'/ch'+str(int(x+1))+'.flv'
			name1 = str(int(x+1))+'. '+name
			name2 = name1+' - '+info[x]
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name2 } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(eps+' - '+name1)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
			
def playVideo(url, name):
	name = name + '.flv'
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
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
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
	showCategories()
elif mode==1:
	showList(url, name)
elif mode==2:
	playVideo(url, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
