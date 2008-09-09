"""
 A plugin to get videos from UlmenTV
"""

import sys, os, os.path
import xbmc, xbmcgui, xbmcplugin
import urllib, re

__plugin__ = "UlmenTV"
__version__ = '1.0'
__author__ = 'bootsy [bootsy82@gmail.com] with much help from BigBellyBilly'
__date__ = '09-09-2008'

DIR_USERDATA = os.path.join( "T:\\script_data", __plugin__ )

def log(msg):
    xbmc.output(str(msg))

dialogProgress = xbmcgui.DialogProgress()


#[(url,show)]
def getUlmenCats():
	log("> getUlmenCats()")
	res=[]
	url = "http://www.myspass.de/de/ulmentv/index.html"
	doc = fetchText(url)
	if doc:
		doc = doc.replace('<br />', ' ').replace('Neueste Videos', '')
		p=re.compile('"others"><a href="(/de/ulmentv/.+?/index.html\?id=\d+)">(.*?)</a')
		matches=p.findall(doc)
		for url,name in matches:
			res.append((url,name))

		for item in res:
			log(item)

	log("< getUlmenCats()")
	return res

#[(url,show)]
def getUlmenepisodes(url,name):
	log("> getUlmenepisodes()")
	res=[]
	base_url = 'http://www.myspass.de'
	if not url.startswith(base_url):
		url = base_url+url
	doc = fetchText(url)
	if doc:
		p1=re.compile('class="my_chapter_headline">(.*?)</div>(.*?)<!--my_videoslider_line', re.DOTALL + re.MULTILINE + re.IGNORECASE)				# bbb
		p2=re.compile('class="my_video_headline">(.*?)</.*?(http.*?jpg).*?id=(\d+)" title="(.*?)"', re.DOTALL + re.MULTILINE + re.IGNORECASE)
		chMatches=p1.findall(doc)
#		print "chMatches=", chMatches
		for chname, episodes in chMatches:
			p2Matches=p2.findall(episodes)
#			print "p2Matches=", p2Matches
			for part,thumbnail,id,name in p2Matches:
				url='http://c11021-o.l.core.cdn.streamfarm.net/1000041copo/ondemand/163840/'+id+'/'+id+'_de.flv'
				res.append((chname,part,thumbnail,url,name))

		for item in res:
			log(item)

	log("< getUlmenepisodes()")
	return res

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
		xbmcgui.Dialog().ok("Page Download failed!", msg)
	return doc

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
		xbmcgui.Dialog().ok("Download failed!", msg)
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

def addLink(name, url, img):
	log("addLink() url=%s" % url)
	liz=xbmcgui.ListItem(name, '', img, img)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	log("addDir() url=%s" % u)
	liz=xbmcgui.ListItem(name)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

def showCats(url,name):
	cat=getUlmenCats()
	for url,name in cat:
		addDir(name,url,1)

def showShows(url,name):
	shows=getUlmenepisodes(url,name)
	dialogProgress.create("Downloading Shows ...")
	for chname,part,thumbnail,url,name in shows:
		ep = "%s - %s" % (part, name)
		dialogProgress.update(0, chname, ep, os.path.basename(thumbnail))
		img = fetchBinary(thumbnail)
		if not img:
			img = "DefaultVideo.png"
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
