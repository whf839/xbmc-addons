
__scriptname__ = "ATDHE.Net"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/ATDHE.Net"
__date__ = '2009-09-27'
__version__ = "1.0.1"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib import urlretrieve, urlcleanup
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1'
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "Thumbnails", "Video" )

def _check_for_jtv():
	if os.path.isdir('special://home/plugins/video/Justin.tv') == False:
		dia = xbmcgui.Dialog()
		ok = dia.ok("ATDHE.Net", 'Please install the Justin.tv plugin.\nIt is required to run this plugin.' )
		return

def _check_for_update():
	print "ATDHE.Net v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/ATDHE.Net/default.py'
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
			ok = dia.ok("ATDHE.Net", 'Updates are available on SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def showRoot():
	url='http://atdhe.net/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	content=urllib2.urlopen(req)
	data=content.read()
	content.close()
	time=re.compile('<td align="right"><b>(.*?)</b></td><td align="left"><b>(.*?)</b></td>').findall(data)
	image=re.compile('<td width="26px" height="13px"><img src="(.+?)" width="13" height="13" /></td>').findall(data)
	url_title=re.compile('<td width="450px"  align="left"><b><a href="(.+?)" onClick="newwindow\(\'(.+?)\', \'(.+?)\'\); return false;">(.+?)</a></b><font style="font-size: 8px;"> </font></td>').findall(data)
	count=0
	x=0
	for url,trash1,trash2,name in url_title:
		if len(time[x][0]) == 0:
			label=' '+str(count+1)+') '+name
		else:
			label=str(count+1)+') '+time[x][0]+' '+'ET'+' - '+name
		url='http://atdhe.net/' + url
		thumb=image[count]
		item=xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,item)
		count=count+1
		x=x+2

def showList(url, name):
	cat=name
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	content=urllib2.urlopen(req)
	data=content.read()
	content.close()
	#ustreamcode2=re.compile('embed type="application/x-shockwave-flash" src="http://www\.ustream\.tv/flash/live/1/(.+?)"').findall(data)
	#ustreamcode=re.compile('<center>\n<script language="javascript">document\.write\(unescape\( \'(.+?)\' \)\);</script>').findall(data)
	code=re.compile('<script language="javascript">document\.write\(unescape\( \'(.+?)\' \)\);</script>').findall(data)
	code2=re.compile('<script language="javascript">document\.write\(\'(.+?)\'\);</script>').findall(data)
	print len(code)
	print len(code2)
	if len(code) == 1:
		info=code[0].replace('%', '').replace('\u00', '').decode('hex')
		if info.find('justin.tv') != -1:
			channel=re.compile('id="jtv_player_flash" data="http://www\.justin\.tv/widgets/live_embed_player\.swf\?channel=(.+?)" bgcolor').findall(info) 
			thumb='http://static-cdn.justin.tv/previews/live_user_'+channel[0]+'-320x240.jpg'
			img=get_thumbnail( thumb )
			path = 'plugin://video/Justin.tv/'+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(channel[0])+"&thumb="+urllib.quote_plus(img)
			command = 'XBMC.RunPlugin(%s)' % path
			xbmc.executebuiltin(command)
		else:
			dia = xbmcgui.Dialog()
			ok = dia.ok("ATDHE.Net", 'Error 1: The stream is either offline or\nusing an unsupported protocol.')
	elif len(code2) != 0:
		info=code2[0].replace('%', '').replace('\u00', '').decode('hex')
		if info.find('justin.tv') != -1:
			channel=re.compile('id="jtv_player_flash" data="http://www\.justin\.tv/widgets/live_embed_player\.swf\?channel=(.+?)" bgcolor').findall(info) 
			thumb='http://static-cdn.justin.tv/previews/live_user_'+channel[0]+'-320x240.jpg'
			img=get_thumbnail( thumb )
			path = 'plugin://video/Justin.tv/'+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(channel[0])+"&thumb="+urllib.quote_plus(img)
			command = 'XBMC.RunPlugin(%s)' % path
			xbmc.executebuiltin(command)
		else:
			dia = xbmcgui.Dialog()
			ok = dia.ok("ATDHE.Net", 'Error 2: The stream is either offline or\nusing an unsupported protocol.')				
	elif len(code) == 2:
		info=code[1].replace('%', '').replace('\u00', '').decode('hex')
		if info.find('ustream') != -1:
			rtmp_id=re.compile('&file=(.+?)&id=(.+?)&').findall(info)
			rtmp_url = rtmp_id[0][0]
			rtmp_url2 = rtmp_id[0][0]
			thumb = xbmc.getInfoImage( "ListItem.Thumb" )
			swfUrl = 'http://cdn1.ustream.tv/swf/4/viewer.rsl.210.swf'
			item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			item.setInfo( type="Video", infoLabels={ "Title": name, "Director": 'USTREAM.tv', "Studio": 'USTREAM.tv' } )
			#item.setProperty("PageURL", pageUrl)
			item.setProperty("SWFPlayer", swfUrl)
			item.setProperty("PlayPath", rtmp_id[0][1])
			item.setProperty("IsLive", "true")
			item.setProperty("tcUrl", rtmp_url2)
			xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp_url, item)
		else:
			dia = xbmcgui.Dialog()
			ok = dia.ok("ATDHE.Net", 'Error 3: The stream is either offline or\nusing an unsupported protocol.')
	else:
		print code
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('ATDHE.Net', 'Error 3: No live streams available.')
	
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
	_check_for_jtv()
	showRoot()
elif mode==0:
	showList(url, name)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
