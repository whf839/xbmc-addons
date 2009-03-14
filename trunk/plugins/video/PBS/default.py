# XBMC Video Plugin
# PBS
# Date: 02/28/08
# Author: stacked < http://xbmc.org/forum/member.php?u=26908 >

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib2 import Request, urlopen, URLError, HTTPError

IMAGE_DIR = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6'

def showRoot():
		thumb=os.path.join(IMAGE_DIR, 'NATURE.gif')
		li=xbmcgui.ListItem("NATURE", iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=1"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		thumb=os.path.join(IMAGE_DIR, 'FRONTLINE.jpg')
		li=xbmcgui.ListItem("FRONTLINE", iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=3"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		thumb=os.path.join(IMAGE_DIR, 'NOVA.jpg')
		li=xbmcgui.ListItem("NOVA", iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=5"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def natureA():
		url='http://www.pbs.org/wnet/nature/category/video/watch-full-episodes/page/'
		thisurl=url
		req = urllib2.Request(url+str(page))
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<a href="(.+?)" rel="bookmark" title="Permanent Link to (.+?): Video: Full Episode"><span class="videodate">(.+?)</span><br />')
		q=re.compile('<span class="videoexcerpt">(.+?)</span></a>')
		r=re.compile('<span class="videoimage"><img src="(.+?)"')
		info=p.findall(a)
		disc=q.findall(a)
		img=r.findall(a)
		x=0
		for url,title,date in info:
			title=clean(title)
			name2 = str(int(x+1+12*int(page-1)))+'. '+date+': '+title+' - '+disc[x]
			thumb='http://www.pbs.org'+img[x]
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(title)+"&url="+urllib.quote_plus(url)+"&page="+str(int(page)+1)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1
		if x == 12:
			li=xbmcgui.ListItem("Next Page", iconImage="DefaultVideo.png", thumbnailImage=os.path.join(IMAGE_DIR, 'next.png'))
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(title)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def natureB(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('class="wordtube playlist(.+?)"')
		numid=p.findall(a)
		url='http://www.pbs.org/wnet/nature/wp-content/plugins/wordtube/myextractXML.php?id='+numid[0]
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		o=re.compile('<creator>(.+?)</creator>')
		w=re.compile('<title>(.+?)</title>')
		r=re.compile('<location>(.+?)</location>')
		q=re.compile('<image>(.+?)</image>')
		title=o.findall(a)
		info=w.findall(a)
		link=r.findall(a)
		img=q.findall(a)
		x=0
		for name in title:
			disc=clean(info[x+1])
			name1 = name+': '+disc
			url='http://www.pbs.org'+link[x]
			thumb=img[x]
			li=xbmcgui.ListItem(name1, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name1 } )
			u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			if name != 'NATURE':
				xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1

def frontlineA():
		url='http://www.pbs.org/wgbh/pages/frontline/view/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('xmlfile: (.+?),')
		match=p.findall(a)
		part=match[0]
		part=part.replace('\'','')
		url='http://www.pbs.org/wgbh/pages/frontline/view/xml/'+part+'.xml'
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<dsc><!\[CDATA\[(.+?)\]\]></dsc>')
		o=re.compile('dat="(.+?)" ext')
		q=re.compile('<sh url="(.+?)" num="(.+?)" cat')
		r=re.compile('<tit><!\[CDATA\[(.+?)\]\]></tit>')
		name=r.findall(a)
		info=p.findall(a)
		date=o.findall(a)
		num=q.findall(a)
		x=0
		for link,numid in num:
			name2 = str(int(x+1))+'. '+date[x]+': '+name[x]+' - '+info[x]
			thumb='http://www.pbs.org/frontline/art/viewimages/200/'+numid+'.jpg'
			url='http://www.pbs.org/wgbh/pages/frontline'+link
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name[x]+'-'+numid)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def frontlineB(url,name):
		x=0
		junk=name
		grab=junk.rsplit('-')
		numid=grab[1]
		eps=grab[0]
		saveurl=url
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		if (a.find('CLICK ON A CHAPTER TO START') > 0 ) or (a.find('videoside') > 0) or (a.find('javascript:void') > 0) :
			url='http://www.pbs.org/wgbh/pages/frontline/video/flv/xml/frol/'+numid+'.xml'
			try:
				req = urllib2.Request(url)
				req.add_header('User-Agent', HEADER)
				f=urllib2.urlopen(req)
			except HTTPError, e:
				for i in range(1,16):
					thumb='http://www.pbs.org/wgbh/pages/frontline/video/flv/thumbs/200/'+numid+'/'+str(int(x+1))+'.jpg'
					try:
						req = urllib2.Request(thumb)
						req.add_header('User-Agent', HEADER)
						f=urllib2.urlopen(req)
					except HTTPError, e:
						dialog = xbmcgui.Dialog()
						ok = dialog.ok('PBS', 'Sorry, this video is not available.\nFind the program at:\n'+saveurl)
						dialog.close()
						break
					else:
						url='http://www-tc.pbs.org/wgbh/pages/frontline/video/flv/'+numid+'/ch'+str(int(x+1))+'.flv'
						name = eps+' - '+'Chapter '+str(int(x+1))
						li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
						li.setInfo( type="Video", infoLabels={ "Title": name } )
						u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
						xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
						x=x+1
			else:
				a=f.read()
				f.close()
				p=re.compile('<description><!\[CDATA\[(.+?)\]\]></description>')
				o=re.compile('package id="(.+?)" airdate')
				r=re.compile('<title><!\[CDATA\[(.+?)\]\]></title>')
				title=r.findall(a)
				info=p.findall(a)
				numid=o.findall(a)
				for name in title:
					thumb='http://www.pbs.org/wgbh/pages/frontline/video/flv/thumbs/200/'+numid[0]+'/'+str(int(x+1))+'.jpg'
					url='http://www-tc.pbs.org/wgbh/pages/frontline/video/flv/'+numid[0]+'/ch'+str(int(x+1))+'.flv'
					name1 = str(int(x+1))+'. '+name
					name2 = name1#+' - '+info[x]
					li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
					li.setInfo( type="Video", infoLabels={ "Title": name2 } )
					u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(eps+' - '+'Chapter '+str(int(x+1)))+"&url="+urllib.quote_plus(url)
					xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
					x=x+1
		elif a.find('videogen') > 0 :
			link=url.rsplit('/')
			urlid=link[6]
			url='http://www.pbs.org/wgbh/pages/frontline/video/flv/xml/frol/'+numid+'.xml'
			req = urllib2.Request(url)
			req.add_header('User-Agent', HEADER)
			f=urllib2.urlopen(req)
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
				url='http://www-tc.pbs.org/wgbh/pages/frontline/video/flv/'+numid[0]+'/'+urlid+'_ch'+str(int(x+1))+'.flv'
				name1 = str(int(x+1))+'. '+name
				name2 = name1+' - '+info[x]
				li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
				li.setInfo( type="Video", infoLabels={ "Title": name2 } )
				u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(eps+' - '+'Chapter '+str(int(x+1)))+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
				x=x+1
		elif a.find('video220detect') > 0 :
			p=re.compile('alt="low" border=(.+?) name')
			info=p.findall(a)
			if len(info) == 0:
				dialog = xbmcgui.Dialog()
				ok = dialog.ok('PBS', 'Sorry, this video is not available.\nFind the program at:\n'+saveurl)
				dialog.close()
			x=0
			for test in info:
				#thumb='http://www.pbs.org/wgbh/pages/frontline/video/flv/thumbs/200/'+numid[0]+'/'+str(int(x+1))+'.jpg'
				url='http://media.pbs.org/asxgen/general/windows/media4/frontline/'+numid+'/windows/'+numid+'ch'+str(int(x+1))+'_hi.wmv.asx'
				name = eps+' - '+'Chapter '+str(int(x+1))
				li=xbmcgui.ListItem(name)#, iconImage=thumb, thumbnailImage=thumb)
				li.setInfo( type="Video", infoLabels={ "Title": name } )
				u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(eps+' - '+'Chapter '+str(int(x+1)))+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
				x=x+1
		# else:
			# dialog = xbmcgui.Dialog()
			# ok = dialog.ok('PBS', 'Sorry, this video is not available.\nFind the program at:\n'+saveurl)
			# dialog.close()
				
def novaA():
		url='http://www.pbs.org/wgbh/nova/programs/'
		thisurl=url
		if page == 1:
			req = urllib2.Request(url)
		elif (page > 1) and (page < 10):
			req = urllib2.Request(url+'0'+str(page)+'.html')
		else:
			req = urllib2.Request(url+str(page)+'.html')
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<tr><td width="184" valign="top" align="left"><a href="(.+?)"><img src="(.+?)" alt')
		o=re.compile('class="progtext"> <b>(.+?)</b> \((.+?)\)<br /><br />(.+?) <a href')
		links=p.findall(a)
		info=o.findall(a)
		x=0
		for link,img in links:
			name2 = str((x+1)+5*(page-1))+'. '+clean(info[x][1])+': '+clean(info[x][0])+' - '+clean(info[x][2])
			thumb='http://www.pbs.org'+img
			url='http://www.pbs.org'+link
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(clean(info[x][0]))+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1
		if x == 5:
			li=xbmcgui.ListItem("Next Page", iconImage="DefaultVideo.png", thumbnailImage=os.path.join(IMAGE_DIR, 'next.png'))
			u=sys.argv[0]+"?mode=5&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def novaB(url, name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('class="videohour1" width="184" valign="top"><img src="(.+?)" alt="(.+?) thumbnail"')
		o=re.compile('<h2 class="video">(.+?)</h2>', re.DOTALL)
		#q=re.compile('<p class="tight-top">\n(.+?)\n<br /><i>')
		q=re.compile('<p class="tight-top">(.+?)<br /><i>', re.DOTALL)
		i=re.compile('<a href="/wgbh/nova/transcripts/(.+?)_(.+?).html">Program Transcript</a>')
		links=p.findall(a)
		info=o.findall(a)
		disc=q.findall(a)
		ids=i.findall(a)
		x=0
		if len(links) == 0:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('PBS', 'Sorry, this video is not available.\nURL: '+url)
			dialog.close()
		for img,title in links:
			name=title+' - '+info[x]
			name=clean(name)
			name2 = clean(title)+': '+clean(info[x])+' - '+clean(disc[x])
			thumb='http://www.pbs.org'+img
			url='http://media.pbs.org/asxgen/general/windows/wgbh/nova/'+ids[0][1]+'-'+ids[0][0]+'-c0'+str(x+1)+'-350.wmv.asx'
			li=xbmcgui.ListItem(name2, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
		
def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('’','\''),('&#8217;','\''),('&#8212;','-'),('<i>','"'),('</i>','"'),('\n',' '),('<br>',''),('<br />','')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name
	
def Update():
	def downloadFile(url):
		drive = xbmc.translatePath( ( "U:\\" , "Q:\\" )[ os.environ.get( "OS", "xbox" ) == "xbox" ] )
		tempDir = os.path.join( drive, 'cache' )
		temp = os.path.join( drive, 'cache' ,'PBS_'+newVersion+'.zip')
		if not os.path.isdir( tempDir) :
			os.makedirs( tempDir )
		dp = xbmcgui.DialogProgress()       
		dp.create("Please Wait","Downloading Update...",url)
		urllib.urlretrieve(url,temp,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
		path = os.path.join( drive,'plugins','Video') 
		xbmc.executebuiltin("XBMC.Extract("+temp+","+path+")")
		
	def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
		try:
			percent = min((numblocks*blocksize*100)/filesize, 100)
			dp.update(percent)
		except:
			percent = 100
			dp.update(percent)
		if dp.iscanceled():  
			dp.close()
	version='b3'
	req = urllib2.Request('http://code.google.com/p/plugin/downloads/list?q=label:Featured')
	response = urllib2.urlopen(req)
	page = response.read()
	response.close()
	ALL = re.compile('http://plugin.googlecode.com/files/PBS_(.+?).zip').findall(page)
	for link in ALL :
		if link.find(version) != 0:
			newVersion=link
			dia = xbmcgui.Dialog()
			if dia.yesno('Update Available', 'There is an update available, would you like to update?\nCurrent Version: '+version+'\nUpdate Version: '+newVersion):
				url='http://plugin.googlecode.com/files/PBS_'+newVersion+'.zip'
				downloadFile(url)
				ok = dia.ok('Update Complete', 'Restart this plugin to take effect.')
			
def playVideo(url, name):
	name = name + '.flv'
	if url.find('wmv') > 0:
		if xbmcplugin.getSetting("dvdplayer") == "true":
			player_type = xbmc.PLAYER_CORE_DVDPLAYER
		else:
			player_type = xbmc.PLAYER_CORE_MPLAYER
		xbmc.Player(player_type).play(str(url))
	else:
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
	Update()
	showRoot()
elif mode==0:
	playVideo(url, name)
elif mode==1:
	natureA()
elif mode==2:
	natureB(url, name)
elif mode==3:
	frontlineA()
elif mode==4:
	frontlineB(url, name)
elif mode==5:
	novaA()
elif mode==6:
	novaB(url, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
