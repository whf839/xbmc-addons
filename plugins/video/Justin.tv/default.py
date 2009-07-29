
__scriptname__ = "Justin.tv"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Justin.tv"
__date__ = '2009-07-29'
__version__ = "1.4.9"
__XBMC_Revision__ = "21803"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback, shutil
from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlretrieve, urlcleanup
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://temp/" ), "Justin.tv" )

def temp_dir():
	if os.path.isdir(BASE_CACHE_PATH):
		shutil.rmtree(BASE_CACHE_PATH)
	os.mkdir(BASE_CACHE_PATH)
	dir = "0123456789abcdef"
	for path in dir:
		new = os.path.join( xbmc.translatePath( "special://temp/" ), "Justin.tv", path )
		os.mkdir(new)
			
def _check_compatible():
	xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
	xbmc_rev = int( xbmc_version.split( " " )[ 1 ].replace( "r", "" ) )
	ok = xbmc_rev >= int( __XBMC_Revision__ )
	if ( not ok ):
		xbmcgui.Dialog().ok( "%s - %s: %s" % ( __scriptname__, xbmc.getLocalizedString( 30700 ), __version__, ), xbmc.getLocalizedString( 30701 ) % ( __scriptname__, ), xbmc.getLocalizedString( 30702 ) % ( __XBMC_Revision__, ), xbmc.getLocalizedString( 30703 ) )
	return ok
	
def _check_for_update():
	print "Justin.tv v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/Justin.tv/default.py'
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
			ok = dia.ok("Justin.tv", xbmc.getLocalizedString( 30720 )+'\n\n'+xbmc.getLocalizedString( 30721 )+' '+__version__+'\n'+xbmc.getLocalizedString( 30722 )+' '+newVersion)

def showCategories():
	if xbmcplugin.getSetting('language') == '0':
		idd = 'en'
	elif xbmcplugin.getSetting('language') == '1':
		idd = 'ar'
	elif xbmcplugin.getSetting('language') == '2':
		idd = 'bg'
	elif xbmcplugin.getSetting('language') == '3':
		idd = 'ca'
	elif xbmcplugin.getSetting('language') == '4':
		idd = 'de'
	elif xbmcplugin.getSetting('language') == '5':
		idd = 'el'
	elif xbmcplugin.getSetting('language') == '6':
		idd = 'es'
	elif xbmcplugin.getSetting('language') == '7':
		idd = 'fr'
	elif xbmcplugin.getSetting('language') == '8':
		idd = 'hi'
	elif xbmcplugin.getSetting('language') == '9':
		idd = 'hu'
	elif xbmcplugin.getSetting('language') == '10':
		idd = 'id'
	elif xbmcplugin.getSetting('language') == '11':
		idd = 'is'
	elif xbmcplugin.getSetting('language') == '12':
		idd = 'it'
	elif xbmcplugin.getSetting('language') == '13':
		idd = 'iw'
	elif xbmcplugin.getSetting('language') == '14':
		idd = 'ja'
	elif xbmcplugin.getSetting('language') == '15':
		idd = 'ko'
	elif xbmcplugin.getSetting('language') == '16':
		idd = 'lt'
	elif xbmcplugin.getSetting('language') == '17':
		idd = 'nl'
	elif xbmcplugin.getSetting('language') == '18':
		idd = 'no'
	elif xbmcplugin.getSetting('language') == '19':
		idd = 'pl'
	elif xbmcplugin.getSetting('language') == '20':
		idd = 'pt'
	elif xbmcplugin.getSetting('language') == '21':
		idd = 'ro'
	elif xbmcplugin.getSetting('language') == '22':
		idd = 'ru'
	elif xbmcplugin.getSetting('language') == '23':
		idd = 'sr'
	elif xbmcplugin.getSetting('language') == '24':
		idd = 'tl'
	elif xbmcplugin.getSetting('language') == '25':
		idd = 'tr'
	elif xbmcplugin.getSetting('language') == '26':
		idd = 'uk'
	elif xbmcplugin.getSetting('language') == '27':
		idd = 'zh-TW'
	url='http://www.justin.tv/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<ul class="fp_categories">(.+?)<div id="FPTakeoverSkinv2_holder">', re.DOTALL).findall(a)
	cat=re.compile('<a href="(.+?)"><b>(.+?)</b></a>').findall(match[0])
	name = 'All'
	url='http://www.justin.tv/directory?order=hot&lang='+idd
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	for url,name in cat:
		new=url.replace('/directory','/directory/dropmenu/subcategory')
		url='http://www.justin.tv'+new+'?kind=live&order=hot&lang='+idd
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('(Search)',iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus('(Search)')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('(User Search)',iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus('(User Search)')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showSubCategories(url, name):
	cat_name=name
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	cat=re.compile('<li class="subcategory"><a href="(.+?)">(.+?)</a></li>').findall(a)
	for url,name in cat:
		url='http://www.justin.tv' + url
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(cat_name+' / '+name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showLinks(url, name):
	url=url.replace('kind=live&','')
	cat_name=name
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<ul class="channel_list li_grid clearfix">(.+?)<div id="pagelinks" class="pagelinks clear">', re.DOTALL).findall(a)
	if len(match) == 0:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: No live streams available.')
		showCategories()
		return
	cat=re.compile('<a href="(.+?)" class="title">(.+?)</a>').findall(match[0])
	data=re.compile('<img alt="" class="cap lateload" src1="(.+?)" src').findall(match[0])
	stat1=re.compile('<span class="overlay viewers_count">(.+?)</span>').findall(match[0])
	stat2=re.compile('<span class="small">on <a href="(.+?)">(.+?)</a></span>').findall(match[0])
	x=0
	for url,title in cat:
		url=url.replace('/','')
		name=str(int(x+1)+(36*(page-1)))+')  '+clean(title)+' on '+clean(stat2[x][1])+' - '+stat1[x]
		thumb = get_thumbnail(data[x])
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(cat_name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(data) >= 36:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(cat_name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('&lt;','<'),('&gt;','>')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name

def runKeyboard():
	li=xbmcgui.ListItem('(Enter Search)',iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u=sys.argv[0]+"?mode=9"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	presets = xbmcplugin.getSetting( "presets_search" )
	if presets != '':
		save = presets.split( " | " )
	else:
		save = []
	cm = []
	for query in save:
		url = 'http://www.justin.tv/search?q='+query+'&commit=Search'
		cm = [ ( 'Remove', "XBMC.RunPlugin(%s?mode=7&name=%s&url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus(query), urllib.quote_plus('search') ), ) ]
		cm += [ ( 'Edit', "XBMC.RunPlugin(%s?mode=8&name=%s&url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus(query), urllib.quote_plus('search') ), ) ]
		li=xbmcgui.ListItem(query,iconImage=os.path.join(THUMBNAIL_PATH, 'search_categories.png'),thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_categories.png'))
		li.addContextMenuItems( cm, replaceItems=True )
		u=sys.argv[0]+"?mode=4&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	
def runKeyboard4():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Search")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	presets = xbmcplugin.getSetting( "presets_search" )
	if presets == '':
		save_str = newStr
	else:
		save_str = presets + " | " + newStr
	xbmcplugin.setSetting("presets_search", save_str)
	if len(newStr) != 0:
		url = 'http://www.justin.tv/search?q='+newStr
		runSearch(url)
		
def runSearch(url):
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	titles=re.compile('<a href="(.+?)" class="title bold_results" onclick="(.*?)">(.+?)</a>').findall(a)
	thumbs=re.compile('class="(cap )?lateload" src1="(.+?)" src').findall(a)
	#info=re.compile('<p class="description bold_results">\n            (.*?)\n        </p>', re.DOTALL).findall(a)
	#stat1=re.compile('<span class="overlay viewers_count">(.+?)</span>').findall(a)
	stat2=re.compile('<span class="action">\n                on <a href="(.+?)" class="nick bold_results">(.+?)</a>\n            ', re.DOTALL).findall(a)
	del[titles[0]]
	del[stat2[0]]
	#del[info[0]]
	print len(titles)
	print len(thumbs)
	#print len(stat1)
	print len(stat2)
	x=0
	for url, crap, name in titles:
		thumb = get_thumbnail(thumbs[x][1])
		title=str(int(x+1)+(36*(page-1)))+')  '+clean(name)+' on '+clean(stat2[x][1])#+' ... '+stat1[x]
		url=url.replace('/','')
		li=xbmcgui.ListItem(title, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus('get_cat')+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(titles) >= 10:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def runKeyboard2():
	li=xbmcgui.ListItem('(Enter User)',iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u=sys.argv[0]+"?mode=6"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	presets = xbmcplugin.getSetting( "presets_users" )
	if presets != '':
		save = presets.split( " | " )
	else:
		save = []
	cm = []
	for query in save:
		cm = [ ( 'Remove', "XBMC.RunPlugin(%s?mode=7&name=%s&url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus(query), urllib.quote_plus('users') ), ) ]
		cm += [ ( 'Edit', "XBMC.RunPlugin(%s?mode=8&name=%s&url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus(query), urllib.quote_plus('users') ), ) ]
		li=xbmcgui.ListItem(query,iconImage=os.path.join(THUMBNAIL_PATH, 'search_users.png'),thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_users.png'))
		li.addContextMenuItems( cm, replaceItems=True )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus('get_cat')+"&url="+urllib.quote_plus(query)+"&thumb="+urllib.quote_plus(os.path.join(THUMBNAIL_PATH, 'search_users.png'))
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
		
def removeB(name,url):
	type = 'presets_' + url
	presets = xbmcplugin.getSetting( type )
	save = presets.split( " | " )
	del save[save.index(name)]
	sets = ''
	x=0
	for item in save:
		if x == 0:
			sets = sets + item
		else:
			sets = sets + ' | ' + item
		x=x+1
	xbmcplugin.setSetting(type, sets)
	xbmc.executebuiltin( "Container.Refresh" )

def editB(name,url):
	type = 'presets_' + url
	presets = xbmcplugin.getSetting( type )
	save = presets.split( " | " )
	del save[save.index(name)]
	x=0
	for item in save:
		if x == 0:
			sets = item
		else:
			sets = sets + ' | ' + item
		x=x+1
	searchStr = name
	keyboard = xbmc.Keyboard(searchStr, "Edit user name")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring
	if len(newStr) == 0:
		return
	if len(save) == 0:
		sets = newStr
	else:
		sets = sets + ' | ' + newStr
	xbmcplugin.setSetting(type, sets)
	xbmc.executebuiltin( "Container.Refresh" )
	
def runKeyboard3():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Enter the exact user name")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
			return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
			return
	presets = xbmcplugin.getSetting( "presets_users" )
	if presets == '':
		save_str = newStr
	else:
		save_str = presets + " | " + newStr
	xbmcplugin.setSetting("presets_users", save_str)
	if len(newStr) != 0:
		thumb = xbmc.getInfoImage( "ListItem.Thumb" )
		playVideo(newStr, 'get_cat', thumb)
		
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

def playVideo(url, name, thumb):
	vid='http://usher.justin.tv/find/live_user_' + url + '.xml'
	print vid
	try:
		req = urllib2.Request(vid)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
	except HTTPError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: Invalid user or not a live feed.')
		xbmc.executebuiltin( "Container.Refresh" )
		return
	a=f.read()
	f.close()
	data=re.compile('<play>(.+?)</play><connect>(.+?)</connect>').findall(a)
	if len(data) == 0:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: Invalid user or not a live feed.')
		xbmc.executebuiltin( "Container.Refresh" )
		return
	playpath = data[0][0]
	rtmp_url = data[0][1]
	swf='http://www.justin.tv/meta/'+url+'.xml'
	print swf
	req = urllib2.Request(swf)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data2=re.compile('SWFObject\(\'(.+?)\',').findall(a)
	data4=re.compile('<status>(.+?)</status>').findall(a)
	data5=re.compile('<translated_category>(.*?)</translated_category>').findall(a)
	data6=re.compile('<translated_subcategory>(.*?)</translated_subcategory>').findall(a)
	data7=re.compile('<screen_cap>(.*?)</screen_cap>').findall(a)
	if name == 'get_cat':
		thumb = get_thumbnail(data7[0])
	name = clean(data5[0] + ' / ' + data6[0])
	referer = 'http://www.justin.tv/'+url
	SWFPlayer = data2[0]
	if (len(data4) == 0):
		title = 'Justin.tv'
	else:
		title = clean(data4[0])
		match=re.compile('&#(.+?);').findall(title)
		for trash in match:
			title=title.replace('&#'+trash+';','')
	item = xbmcgui.ListItem(label=title,iconImage="DefaultVideo.png",thumbnailImage=thumb)
	item.setInfo( type="Video", infoLabels={ "Title": title, "Director": url, "Studio": url, "Genre": name } )
	item.setProperty("SWFPlayer", SWFPlayer)
	item.setProperty("PlayPath", playpath)
	item.setProperty("PageURL", referer)
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
		
if mode==None:
	temp_dir()
	_check_for_update()
	_check_compatible()
	name=''
	showCategories()
elif mode==0:
	showSubCategories(url, name)
elif mode==1:
	showLinks(url, name)
elif mode==2:
	playVideo(url, name, thumb)
elif mode==3:
	runKeyboard()
elif mode==4:
	name=''
	runSearch(url)
elif mode==5:
	runKeyboard2()
elif mode==6:
	name=''
	runKeyboard3()
elif mode==7:
	removeB(name,url)
elif mode==8:
	editB(name,url)
elif mode==9:
	name=''
	runKeyboard4()
	
xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
