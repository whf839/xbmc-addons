
__scriptname__ = "ChannelSurfing.net"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/ChannelSurfing.net"
__date__ = '2009-11-09'
__version__ = "1.0.3"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback, shutil
from urllib import urlretrieve, urlcleanup
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1'
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://temp/" ), "ChannelSurfing.net" )

def check_for_update():
	print "ChannelSurfing.net v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/ChannelSurfing.net/default.py'
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
			ok = dia.ok("ChannelSurfing.net", 'Updates are available on the SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def check_for_jtv():
	if os.path.isdir('special://home/plugins/video/Justin.tv') == False:
		dia = xbmcgui.Dialog()
		ok = dia.ok("ChannelSurfing.net", 'Please install the Justin.tv plugin.\nIt is required to run this plugin.' )
		return

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', HEADER)
    content=urllib2.urlopen(req)
    data=content.read()
    content.close()
    return data

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

def temp_dir():
	if os.path.isdir(BASE_CACHE_PATH):
		shutil.rmtree(BASE_CACHE_PATH)
	os.mkdir(BASE_CACHE_PATH)
	dir = "0123456789abcdef"
	for path in dir:
		new = os.path.join( xbmc.translatePath( "special://temp/" ), "ChannelSurfing.net", path )
		os.mkdir(new)

def get_links():
	data=open_url('http://www.channelsurfing.net')
	info=re.compile('<td (.+?)">\n\t\t\t\t<img border="0" src="(.+?)"(.+?)align="right"></td>\n\t\t\t\t<td width="(.+?)"><a href="(.+?)"( onclick="doPop\(this\.href\); return false;")?>\n\t\t(.+?)</a>', re.DOTALL).findall(data)
	count=0
	for a,thumb,c,d,url,f,title in info:
		url='http://www.channelsurfing.net/'+url
		label=str(count+1)+') '+title.replace('\t','').replace('\n','')
		item=xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(title.replace('\t',''))+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,item)
		count=count+1

def play_video(name,url):
	data=open_url(url)
	if data.find('justin.tv') != -1:
		justintv=re.compile('"http://www\.justin\.tv/widgets/live_embed_player\.swf\?channel=(.+?)"').findall(data)
		justintv2=re.compile('"http://www\.justin\.tv/(.+?)/popout"').findall(data)
		if len(justintv) == 0:
			channel = justintv2[0]
		else:
			channel = justintv[0].rsplit('&')[0]
		thumb='http://static-cdn.justin.tv/previews/live_user_'+channel+'-320x240.jpg'
		img=get_thumbnail( thumb )
		path = 'plugin://video/Justin.tv/'+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(channel)+"&thumb="+urllib.quote_plus(img)
		command = 'XBMC.RunPlugin(%s)' % path
		xbmc.executebuiltin(command)
	elif data.find('rtmp') != -1:
		rtmp_id=re.compile('file=(.+?)&amp;id=(.+?)&').findall(data)
		rtmp_id2=re.compile('streamer=(.+?)&amp;file=(.+?)&').findall(data)
		if len(rtmp_id) == 0:
			rtmp_url = rtmp_id2[0][0]
			rtmp_url2 = rtmp_id2[0][1]
		else:
			rtmp_url = rtmp_id[0][0]
			rtmp_url2 = rtmp_id[0][1]
		thumb = xbmc.getInfoImage( "ListItem.Thumb" )
		swfUrl = 'http://cdn1.ustream.tv/swf/4/viewer.rsl.210.swf'
		item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		item.setInfo( type="Video", infoLabels={ "Title": name, "Director": 'USTREAM.tv', "Studio": 'USTREAM.tv' } )
		item.setProperty("SWFPlayer", swfUrl)
		item.setProperty("PlayPath", rtmp_url2)
		item.setProperty("IsLive", "true")
		item.setProperty("tcUrl", rtmp_url)
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp_url, item)
	elif data.find('mms') != -1:
		mms=re.compile('"mms://(.+?)"').findall(data)
		thumb = xbmc.getInfoImage( "ListItem.Thumb" )
		item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		item.setInfo( type="Video", infoLabels={ "Title": name, "Director": 'ChannelSurfing.net', "Studio": 'ChannelSurfing.net' } )
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play('mms://'+mms[0], item)
	else:
		print url
		print data
		dia = xbmcgui.Dialog()
		ok = dia.ok("ChannelSurfing.net", 'Error 1: The stream is either offline or\nusing an unsupported protocol.')

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

if mode==None:
	check_for_update()
	temp_dir()
	check_for_jtv()
	get_links()
elif mode==1:
	play_video(name,url)

xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
