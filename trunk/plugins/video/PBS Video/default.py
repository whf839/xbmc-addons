
__scriptname__ = "PBS Video"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/PBS%20Video"
__date__ = '2009-08-23'
__version__ = "1.3"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib import urlretrieve, urlcleanup
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1'
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "Thumbnails", "Video" )

def _check_for_update():
	print "PBS Video v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/PBS%20Video/default.py'
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
			ok = dia.ok("PBS Video", 'Updates are available on SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def showRoot():
		url='http://video.pbs.org/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<ul id="mainnav">(.+?)<li class="more">', re.DOTALL)
		match=p.findall(a)
		o=re.compile('<li><a href="http://video.pbs.org/program/(.+?)/" title="(.+?)">')
		data=o.findall(match[0])
		x=0
		for url, name in data:
			url='http://www.pbs.org/video/programReleases/' + url + '/start/01/end/999/'
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showList(url, name):
		cat=name
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<p class="info">\n                \n                <a href="http://video.pbs.org/video/(.+?)" class="title" title="(.+?)">(.+?)</a>\n')
		q=re.compile('<span class="list">(.+?)</span>')
		r=re.compile('<img src="(.+?)" alt="(.+?)" />')
		info=p.findall(a)
		disc=q.findall(a)
		img=r.findall(a)
		x=0
		for url,trash,title in info:
			thumb = get_thumbnail( img[x][0] )
			url='http://video.pbs.org/videoPlayerData/' +url
			title=clean(title)
			name = str(int(x+1))+'. '+title+' - '+clean(disc[x])
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name , "Director": "PBS", "Studio": "PBS", "Genre": cat, "Plot": clean(disc[x]) } )
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(title)+"&url="+urllib.quote_plus(url)+"&page="+str(int(page)+1)+"&thumb="+urllib.quote_plus(thumb)+"&plot="+urllib.quote_plus(clean(disc[x]))
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
	
def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('&#39;','\'')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name
	
def get_thumbnail(thumbnail_url):
	try:
		filename = xbmc.getCacheThumbName( thumbnail_url )
		filepath =xbmc.translatePath( os.path.join( BASE_CACHE_PATH, filename[ 0 ], filename ) )
		if not os.path.isfile( filepath ):
			info = urlretrieve( thumbnail_url, filepath )
			urlcleanup()
		return filepath
	except:
		print "Error: get_thumbnail()"
		return thumbnail_url
			
def playVideo(url, name, thumb, plot):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('&releaseURL=http%3A//release.theplatform.com/content.select%3Fpid%3D(.+?)%26UserName')
	info=p.findall(a)
	url='http://release.theplatform.com/content.select?pid='+info[0]+'&format=SMIL'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('<meta base="(.+?)" />').findall(a)
	r=re.compile('<ref src="(.+?)" title="(.+?)" author').findall(a)
	if p[0] == 'http://ad.doubleclick.net/adx/':
		data = r[0][0].split("&lt;break&gt;")
		rtmp_url = data[0]
		playpath = "mp4:"+data[1]
	else:
		rtmp_url = p[0]
		playpath = "mp4:"+r[0][0]
	title = name.split(' | ')
	item = xbmcgui.ListItem(label=name,iconImage="DefaultVideo.png",thumbnailImage=thumb)
	item.setInfo( type="Video", infoLabels={ "Title": title[1] , "Director": "PBS", "Studio": "PBS", "Genre": title[0], "Plot": plot } )
	item.setProperty("PlayPath", playpath)
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
try:
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        pass

if mode==None:
	name = ''
	_check_for_update()
	showRoot()
elif mode==0:
	showList(url, name)
elif mode==1:
	playVideo(url, name, thumb, plot)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
