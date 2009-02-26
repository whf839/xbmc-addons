"""
 A plugin to get videos from UlmenTV
"""

import sys, os, os.path
import xbmc, xbmcgui, xbmcplugin
import urllib, re
from shutil import rmtree

__plugin__ = "UlmenTV"
__version__ = '1.34'
__author__ = 'bootsy [bootsy82@gmail.com] with much help from BigBellyBilly'
__date__ = '12-02-2009'

#DIR_USERDATA = "/".join( ["special://masterprofile","plugin_data", __plugin__] )      # T:// - new drive
DIR_USERDATA = "/".join( ["T:","plugin_data","video", __plugin__] )  # translatePath() will convert to new special://
DIR_USERDATA_OLD = "/".join( ["T:","plugin_data", __plugin__] )  # translatePath() will convert to new special://
BASE_URL = 'http://www.myspass.de'

def log(msg):
	if isinstance(msg,list):
		for i in msg:
			xbmc.output(str(i))
	else:
		xbmc.output(str(msg))

dialogProgress = xbmcgui.DialogProgress()

# Get all Categories.
def getUlmenCats():
	log("> getUlmenCats()")
	res=[]
	url = BASE_URL + "/de/ulmentv/index.html"
	doc = fetchText(url)
	if doc:
		p=re.compile('class="(?:active|inactive).*?href="(.*?)">(.*?)</a', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		matches=p.findall(doc)
		for url,name in matches:
			res.append((url, name.replace('<br />',' ')))

		log(res)
	log("< getUlmenCats()")
	return res

# Get all episodes for a cat.
def getUlmenepisodes(url,name):
	log("> getUlmenepisodes()")
	res=[]
	doc = fetchText(url)
	if doc:
		p1=re.compile('class="my_chapter_headline">(.*?)</div>(.*?)<!--my_videoslider_line', re.DOTALL + re.MULTILINE + re.IGNORECASE)				# bbb
		p2=re.compile('class="my_video_headline">(.*?)</.*?(http.*?jpg).*?href="(.*?)" title="(.*?)"', re.DOTALL + re.MULTILINE + re.IGNORECASE)		
		chMatches=p1.findall(doc)
		for chname, episodes in chMatches:
			p2Matches=p2.findall(episodes)
			for part,thumbnail,id,name in p2Matches:
				if thumbnail=='':
					thumbnail='http://xbmc.svn.sourceforge.net/svnroot/xbmc/trunk/XBMC/skin/Project%20Mayhem%20III/media/defaultVideoBig.png'
					name='Unbekannt'
				url='http://www.myspass.de'+id
				res.append((chname,part,thumbnail,url,name))

		log(res)
	log("< getUlmenepisodes()")
	return res

# Get all newest episodes.
def getUlmenNewEpisodes(name):
	log("> getUlmenNewEpisodes()")
	res=[]
	url = BASE_URL + '/de/ajax/utv/utv_videolist_newest.html?owner=UlmenTV'
	doc = fetchText(url)
	if doc:
		p=re.compile('url\(\'(.*?)\'.*?href="(.*?)".*?title="(.*?)"', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		matches=p.findall(doc)
		for thumbnail,id,name in matches:
			if thumbnail=='':
				thumbnail='http://xbmc.svn.sourceforge.net/svnroot/xbmc/trunk/XBMC/skin/Project%20Mayhem%20III/media/defaultVideoBig.png'
			if name=='':
				name='Unbekannt'
			url='http://www.myspass.de'+id
			res.append(('Neueste Videos','Folge 1/1',thumbnail,url,name))

		log(res)
	log("< getUlmenNewEpisodes()")
	return res
	
#fetch videolinks
def fetchVideoLink(url):
	url='http://www.degrab.de/?url='+url
	f=urllib.urlopen(url)
	doc=f.read()
	f.close()
	if doc:
		p=re.compile('<div style=.+? <a href="(.+?)" rel="nofollow".+?">.+?</a></div>', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		matches=p.findall(doc)
		url=matches[0]
	return url	

# fetch webpage
def fetchText(url):
	doc = ""
	try:
		log('fetchText() url=%s' % url)
		f=urllib.urlopen(url)
		doc=f.read()
		f.close()
		doc=unicode(doc, 'UTF-8')
	except:
		msg = sys.exc_info()[ 1 ]
		print msg
		xbmcgui.Dialog().ok("WebPage Download failed!", msg)
	return doc

# fetch media file
def fetchBinary(url):
	fn = ''
	try:
		fn = os.path.join(DIR_USERDATA, os.path.basename(url))
		fn = xbmc.translatePath(fn)
		fn = xbmc.makeLegalFilename(fn)
		log('fetchBinary() url=%s fn=%s' % (url,fn))
		if not os.path.isfile(fn):
			opener = urllib.FancyURLopener()
			fn, resp = opener.retrieve(url, fn)
			opener.close()
			os.path.isfile(fn)
	except:
		msg = sys.exc_info()[ 1 ]
		print msg
		xbmcgui.Dialog().ok("Media Download failed!", msg)
		fn = ''

	if fn and os.path.isfile(fn):
		return fn
	else:
		return ''
	
def get_params():
	""" extract params from argv[2] to make a dict (key=value) """
	log("get_params() argv[2]=%s" % sys.argv[2])
	paramDict = {}
	if sys.argv[2]:
		paramPairs=sys.argv[2][1:].split( "&" )
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits))==2:
				paramDict[paramSplits[0]] = paramSplits[1]

	return paramDict

# add a link to directory
def addLink(name, url, img):
	log("addLink() url=%s" % url)
	liz=xbmcgui.ListItem(name, '', img, img)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	url = fetchVideoLink(url)
	log("addLink() videourl=%s" % url)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

# add a folder to directory
def addDir(name,url,mode):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	log("addDir() url=%s" % u)
	liz=xbmcgui.ListItem(name)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

# fetch Cats and add to directory
def showCats(url,name):
	cat=getUlmenCats()
	for url,name in cat:
		addDir(name,url,1)

# fetch Episodes for a Cat. and add to directory
def showShows(url,name):
	if not url.startswith(BASE_URL):
		url = BASE_URL+url
	if url.endswith('ulmentv/index.html'):
		shows=getUlmenNewEpisodes(name)
	else:
		shows=getUlmenepisodes(url,name)
	dialogProgress.create("Downloading Shows ...")
	for chname,part,thumbnail,url,name in shows:
		ep = "%s - %s" % (part, name)
		dialogProgress.update(0, chname, ep, os.path.basename(thumbnail))
		img = fetchBinary(thumbnail)
		if not img:
			img = "DefaultVideo.png"
		if (chname=='Neueste Videos'):
			show=name
		else:
			show = "%s - %s - %s" % (chname, part, name)
		addLink(show,url,img)
	dialogProgress.close()

#######################################################################################################################    
# BEGIN !
#######################################################################################################################
try:
	# used to save thumbnail images
	d = xbmc.translatePath(DIR_USERDATA)
	os.makedirs( d )
	log("created " + d)
except: pass
			
try:
	# used to remove old thumbnails + folder
	d = xbmc.translatePath(DIR_USERDATA_OLD)
	rmtree(d, ignore_errors=True)
	log("removed " + d)
except: pass


params=get_params()
url=None
name=None
mode=None
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
log("Mode: "+str(mode))
log("URL: "+str(url))
log("Name: "+str(name))
if mode==None or url==None or len(url)<1:
		log("categories")
		showCats(url,name)
elif mode==1:
		log("shows")
		showShows(url,name)
elif mode==2:
		log("Next: "+url)
		#showVidlinks(url)
elif mode==3:
		log("show eps: "+url+" - "+name)
		showEpisodes(url)
elif mode==4:
		log("show vidlinks")
		showVidLinks(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
