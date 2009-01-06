#
#       default.py (SceneReleases)
#		A boxee plugin to list movies from scenereleases.info
#		by riegersn
#
#       Copyright 'riegersn' 2008 BoxeeHQ.com
#
#		All my scripts are free to use and to change. I only ask that you credit
#		my work in anything you use this for. If its not your code, don't say it is.
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

__plugin__ = "SceneReleases"
__author__ = "riegersn"
__url__ = "http://boxeehq.com"
__version__ = "0.5"

import boxeehq_pytools as bhq
import torrent_scrape as trscrape

import urllib, urllib2, re, os
import xbmc, xbmcgui, xbmcplugin

rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
imageDir = os.path.join(rootDir, 'resources', 'thumbnails') + '/'

def init_categories():
	boxee_adddir('Latest Releases','http://scenereleases.info/category/movies', 1 , imageDir+'new.png')
	boxee_adddir('Categories','category', 3 , imageDir+'categories.png')
	boxee_adddir('Search','search', 4 , imageDir+'search.png')

def list_categories():
	break1 = '<li class="cat-item cat-item-28">'
	break2 = '<li class="cat-item cat-item-12">'
	html = bhq.getHTML('http://scenereleases.info/', break1, break2).replace('\n', '')
	cats = re.compile('title=\"View.*?- (.+?)\".+?href=\"(.+?)\"').findall(html)
	for cat,link in cats:
		boxee_adddir(cat,link.replace('/feed', ''),1)

def video_search(url):
	post__links('http://scenereleases.info/?s='+url+'&submit=Search')

def post__pass(html):
	_sitekeys = {
		'Release Group'	: 'group',
		'Release Date'	: 'date',
		'Source'		: 'source',
		'Size'			: 'size',
		'Video'			: 'video',
		'Audio'			: 'audio',
		'Subtitles'		: 'subs'
		}

	_video = {
		'name'	:'Unknown',
		'thumb'	:'',
		'group'	:'Unknown',
		'date'	:'Unknown',
		'source':'Unknown',
		'size'	:'Unknown',
		'video'	:'Unknown',
		'audio'	:'Unknown',
		'subs'	:'Unknown',
		'imdb'	:'',
		'images': []
		}

	try:
		_video['name'] = re.compile('title="(.+?)"').findall(html)[0]
	except: pass

	#nuked image
	#http://farm4.static.flickr.com/3007/2948378240_21821530ca_s.jpg

	try:
		_video['thumb'] = re.compile('href="(.+?)"').findall(html)[1]
		if not bhq.listin(_video.thumb.lower(), ['.jpg', '.jpeg', '.png', '.gif']):
			_video['thumb'] = re.compile(' src="(.+?)"').findall(html)[0]
	except: pass

	for key in _sitekeys:
		try:
			x = bhq.strip_tags(re.compile(key+':(.+?)<br />').findall(html)[0])
			if len(bhq.r_htmlchar(x)) > 2:
				_video[_sitekeys[key]] = bhq.r_htmlchar(x)
				print video[_sitekeys[key]]
		except: pass

	try:
		_video['imdb'] = re.compile('<a href=\".+?(t{2}[0-9]{7})').findall(html)[0]
	except: pass

	try:
		_video['images'] = re.compile('<a .*?href="(?!http://nfo\.)([^"]+?jpg|[^"]+?png)".*?>').findall(html)
	except: pass

	try:
		_video['images'].remove(_video['thumb'])
	except: pass

	return str(_video)

def post__links(url):

	imgnext = imageDir+'next.png'
	_html = bhq.getHTML(url).replace('\n', '')
	_posts = re.compile('id="post-(.+?)".+?>(.+?)<span class="meta-comments">').findall(_html)

	for pnum, html in _posts:
		try:
			title = re.compile('>(.+?)</a>').findall(html)[0]
			thumb = re.compile('src="(.+?)"').findall(html)[0]
			boxee_adddir( title, post__pass(html), 2, thumb )
		except: pass

	try:
		x = re.compile('<div class="wp-pagenavi">(.+?)</div>').findall(_html)[0]
		next = re.compile('<a href=\"(.+?)\".+?</a>').findall(x)[-2]
		boxee_adddir('', next, 1, imgnext)
	except: pass

def post__details(url):
	post = eval(url)
	if post:
		trailer = ''
		if post['imdb']:
			imdb = bhq.imdb__number(post['imdb'])
			trailer = bhq.apple__trailer(imdb.title, imdb.genre)

			if trailer:
				trailer = 'http://movies.apple.com/movies/' +trailer[0]

			plot_f = 'Group: %s, Released: %s\nSource: %s, Video: %s, Audio: %s\nSize: %s, Subs: %s\nPlot: %s'
			plot = plot_f % ( post['group'], post['date'], post['source'], post['video'], post['audio'], post['size'], post['subs'], imdb.plot )

			_listinfo = {
				'Title'		: post['name'],
				'Plot'		: plot,
				'Duration'	: imdb.runtime,
				'Cast'		: imdb.cast,
				'Director'	: imdb.director,
				'Studio'	: imdb.studio,
				'Genre'		: ' / '.join(imdb.genre)
			}

		else:
			plot_f = 'Group: %s, Released: %s\nSource: %s, Video: %s, Audio: %s\nSize: %s, Subs: %s\nPlot: %s'
			plot = plot_f % ( post['group'], post['date'], post['source'], post['video'], post['audio'], post['size'], post['subs'], 'No IMDB link found for this video!' )

			_listinfo = {
				'Title'		: post['name'],
				'Plot'		: plot
			}

		boxee_addlink( trailer, post['thumb'], _listinfo)

		_listinfo = { 'Title':'Screenshot' }

		try:
			for image in post['images']:
				boxee_addlink( image, image, _listinfo )
		except: pass

		boxee_adddir( 'Torrent Search', post['name'], 5 , imageDir+'torrent_search.png')
	else:
		show_ok(['Unable to scrape post', 'Visit #boxee on freenode for help!', ''])

def show_ok(url):
	print 'def::show_ok()'

	msg = url
	if ';' in url:
		msg = url.split(';')
	ok = xbmcgui.Dialog().ok( 'SceneReleases.info', msg[0], msg[1], msg[2] )

def torrent_get(url):
	print 'def::torrent_get()'

	if url.startswith("['torrent://"):
		url = eval(url)
		torrent = url[0].replace('torrent://','http://')
		download = xbmcplugin.getSetting( "download_path" )+url[1]
		if xbmcgui.Dialog().yesno( 'SceneReleases.info', url[2], url[3], url[4] ):
			urllib.urlretrieve( torrent, download )
			show_ok(['Download complete!','',''])
		return 0

	opt_seeds = ['0','1','5','10','15','20']
	minseed = int(opt_seeds[int(xbmcplugin.getSetting( "min_seed" ))])

	_torrents = []
	if xbmcplugin.getSetting( "search_pb" ) == 'true':
		_pb_results = trscrape.piratebay__search(url, minseed)
		if _pb_results:
			_torrents.extend( _pb_results )
	if xbmcplugin.getSetting( "search_mn" ) == 'true':
		_mn_results = trscrape.mininova__search(url, minseed)
		if _mn_results:
			_torrents.extend( _mn_results )
	if xbmcplugin.getSetting( "search_tr" ) == 'true':
		_tr_results = trscrape.reactor__search(url, minseed)
		if _tr_results:
			_torrents.extend( _tr_results )

	if not _torrents:
		show_ok(['ThePirateBay/MiniNova returned 0 Results!', '', ''])
	else:
		for torrent in _torrents:
			_thumb = imageDir+torrent.site+'.png'
			site = 'MiniNova.org'
			if torrent.site == 'thepiratebay':
				site = 'ThePirateBay.org'
			elif torrent.site == 'reactor':
				site = 'Torrent Reactor'

			if xbmcplugin.getSetting( "download" ) == 'true':
				_plot = '%s\nHealth: Seeders %s / Leechers %s\nName: %s\nTorrent: %s' % ( site, torrent.seed, torrent.leech, torrent.title, torrent.file.split('/')[-1] )
				_listinfo = { 'Title':torrent.title, 'Plot':_plot }
				boxee_addlink( torrent.file, _thumb, _listinfo )
			else:
				new_url = [torrent.file, '%s.torrent' % ( urllib.unquote(torrent.title).replace(' ', '.') )]
				new_url.extend([site,'Health: Seeders %s / Leechers %s' % (torrent.seed, torrent.leech),urllib.unquote(torrent.title).replace(' ', '')])
				boxee_adddir( torrent.title, str(new_url), 5, _thumb )

def boxee_addlink( _url, _thumb, _info, _type="Video"):
	ok=True
	liz=xbmcgui.ListItem( _info['Title'], iconImage="DefaultVideo.png", thumbnailImage= _thumb )
	liz.setInfo( type = _type, infoLabels = _info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=_url,listitem=liz)
	return ok

def boxee_adddir( name, url, mode, iconimage=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def _parameters():
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

params = _parameters()

url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass

try: name=urllib.unquote_plus(params["name"])
except: pass

try: mode=int(params["mode"])
except: pass

if mode==None or url==None or len(url)<1:
    init_categories()

elif mode==1:
	post__links(url)

elif mode==2:
	post__details(url)

elif mode==3:
	list_categories()

elif mode==4:
	search = get_keyboard('', 'Search SceneReleases')
	video_search(search)

elif mode==5:
	torrent_get(url)

elif mode==6:
	show_ok(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
