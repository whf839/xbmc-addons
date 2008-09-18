"""
 A plugin to get videos from UlmenTV
"""

import sys, os, os.path
import xbmc, xbmcgui, xbmcplugin
import urllib, re

__plugin__ = "UlmenTV"
__version__ = '1.1'
__author__ = 'bootsy [bootsy82@gmail.com] with much help from BigBellyBilly'
__date__ = '18-09-2008'

DIR_USERDATA = os.path.join( "T:\\script_data", __plugin__ )
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
		p2=re.compile('class="my_video_headline">(.*?)</.*?(http.*?jpg).*?id=(\d+)" title="(.*?)"', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		chMatches=p1.findall(doc)
		for chname, episodes in chMatches:
			p2Matches=p2.findall(episodes)
			for part,thumbnail,id,name in p2Matches:
				url='http://c11021-o.l.core.cdn.streamfarm.net/1000041copo/ondemand/163840/'+id+'/'+id+'_de.flv'
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
		p=re.compile('url\(\'(.*?)\'.*?href=".*?id=(.*?)".*?title="(.*?)"', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		matches=p.findall(doc)
		for thumbnail,id,name in matches:
			url='http://c11021-o.l.core.cdn.streamfarm.net/1000041copo/ondemand/163840/'+id+'/'+id+'_de.flv'
			res.append(('Neueste Videos','Folge 1/1',thumbnail,url,name))

		log(res)
	log("< getUlmenNewEpisodes()")
	return res

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
	
# - url = sys.argv[ 0 ]
# - handle = sys.argv[ 1 ]
# - params =  sys.argv[ 2 ]
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
	os.makedirs(DIR_USERDATA)
	log("created " + DIR_USERDATA)
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
