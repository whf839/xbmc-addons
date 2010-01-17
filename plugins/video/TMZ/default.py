
__scriptname__ = "TMZ"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/TMZ"
__date__ = '01-17-2010'
__version__ = "1.1"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib import urlretrieve, urlcleanup
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7'

def _check_for_update():
	print "TMZ v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/TMZ/default.py'
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
			ok = dia.ok("TMZ", 'Updates are available on SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def showRoot():
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/mostrecent?format=xml"
	li=xbmcgui.ListItem("1. Most Recent")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('Most Recent')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/highestrated?format=xml"
	li=xbmcgui.ListItem("2. Top Rated")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('Highest Rated')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/mostpopular?format=xml"
	li=xbmcgui.ListItem("3. Most Watched")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('Most Popular')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/tmzontv?format=xml"
	li=xbmcgui.ListItem("4. TMZ on TV")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('TMZ on TV')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/sponsoredvideo2?format=xml"
	li=xbmcgui.ListItem("5. TMZ Live")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('TMZ Live')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/fullepisode?format=xml"
	li=xbmcgui.ListItem("6. Full Episodes")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('Full Episodes')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	#
	url="http://metaframe.digitalsmiths.tv/v1/tmzcompany/playlists/tmzbadges?format=xml"
	li=xbmcgui.ListItem("7. TMZ Badges")
	u=sys.argv[0]+"?mode=1&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus('TMZ Badges')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showList(url,name):
	cat_name=name
	req = urllib2.Request(url+'&limit='+str((int(xbmcplugin.getSetting('count'))+1)*24))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	videoURL=re.compile('<videoURL>(.+?)</videoURL>').findall(a)
	stillURL=re.compile('<stillURL>(.+?)</stillURL>').findall(a)
	desc=re.compile('<description>(.*?)</description>', re.DOTALL).findall(a)
	name=re.compile('<name>(.+?)</name>').findall(a)
	date=re.compile('<activationDate>(.+?)T(.+?)</activationDate>').findall(a)
	x=0
	for url in videoURL:
		sum=clean(desc[x].replace('\n',''))
		if cat_name == 'Full Episode' or cat_name == 'TMZ Badges':
			title = str(int(x+1))+'. '+name[x]+' - '+date[x][0]
			plot=''
		else:
			title = str(int(x+1))+'. '+name[x]+' - '+sum+' - '+date[x][0]
			plot=sum+' - '+date[x][0]
		thumb = stillURL[x]
		li=xbmcgui.ListItem(clean(title), iconImage=thumb, thumbnailImage=thumb)
		li.setInfo( type="Video", infoLabels={ "Title": clean(name[x]), "Plot": plot } )
		u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(clean(name[x]))+"&cat="+urllib.quote_plus(cat_name)+"&plot="+urllib.quote_plus(plot)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
		x=x+1
		
def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('&#39;','\'')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name
			
def playVideo(url,name,cat,plot):
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
	listitem.setInfo( type="Video", infoLabels={ "Title": title, "Director": "TMZ", "Studio": "TMZ", "Genre": cat, "Plot": plot } )
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
		cat=urllib.unquote_plus(params["cat"])
except:
        pass
try:
		plot=urllib.unquote_plus(params["plot"])
except:
        pass

if mode==None:
	name=''
	_check_for_update()
	showRoot()
elif mode==1:
	showList(url,name)
elif mode==2:
	playVideo(url,name,cat,plot)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
#xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	