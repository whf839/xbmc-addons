"""
 A plugin to get videos from UlmenTV
"""

import sys, os, os.path
import xbmc, xbmcgui, xbmcplugin
import urllib, re, time
from shutil import rmtree, copy
import traceback

__plugin__ = "UlmenTV"
__version__ = '1.36'
__author__ = 'bootsy [bootsy82@gmail.com] with much help from BigBellyBilly'
__date__ = '26-04-2009'

#DIR_USERDATA = "/".join( ["special://masterprofile","plugin_data","video", __plugin__] )      # T:// - new drive
DIR_USERDATA = "/".join( ["T:"+os.sep,"plugin_data","video", __plugin__] )  # translatePath() will convert to new special://
DIR_USERDATA_OLD = "/".join( ["T:"+os.sep,"plugin_data", __plugin__] )  # translatePath() will convert to new special://
BASE_URL = 'http://www.myspass.de'
SVN_URL = 'http://xbmc-addons.googlecode.com/svn/tags/plugins/video/' + __plugin__

# TODO: use special:// equiv. - for now stick with translatePath() cos it converts to special:// equiv.
local_base_dir = "/".join( ['Q:','plugins', 'video'] )
local_dir = xbmc.translatePath( "/".join( [local_base_dir, __plugin__] ) )
backup_base_dir = xbmc.translatePath( "/".join( [local_base_dir,'.backups'] ) )
local_backup_dir = os.path.join( backup_base_dir, __plugin__ )

#print 'local dir: ' + local_dir
#print 'backup dir: ' + local_backup_dir

def log(msg):
	if isinstance(msg,list):
		for i in msg:
			xbmc.output(str(i))
	else:
		xbmc.output(str(msg))

def errorOK(title="", msg=""):
	e = str( sys.exc_info()[ 1 ] )
	log(e)
	if not title:
		title = __plugin__
	if not msg:
		msg = "ERROR!"
	xbmcgui.Dialog().ok( title, msg, e )
	
dialogProgress = xbmcgui.DialogProgress()

def updateCheck(version=""):
	""" update plugin from svn - only works against a single file """
	log("> updateCheck() version=" + version)

	isUpdating = False

	def _parseHTMLSource( htmlsource ):
		""" parse html source for tagged version and url """
		log( "_parseHTMLSource()" )
		try:
			url = re.search('Revision \d+:(.*?)<', htmlsource, re.IGNORECASE).group(1).strip()
			tagList = re.compile('<li><a href="(.*?)"', re.MULTILINE+re.IGNORECASE+re.DOTALL).findall(htmlsource)
			if tagList[0] == "../":
				del tagList[0]
			return tagList, url
		except:
			return None, None

	def _getLatestVersion():
		""" checks for latest tag version """
		version = "-1"
		try:
			# get version tags
			htmlsource = getURL( SVN_URL )
			if htmlsource:
				tagList, url = _parseHTMLSource( htmlsource )
				if tagList:
					version = tagList[-1].replace("/","")  # remove trailing /
		except:
			errorOK()
		log( "_getLatestVersion() version=%s" % version )
		return version


	# main processing of checking
	try:
		dialogProgress.create(__plugin__)
		path = os.getcwd().replace(';','')
		log('current path:' + path)
		if not version or path == local_dir:
			dialogProgress.update(0, "Checking for new version...")
			# get svn version and check if newer
			SVN_V = _getLatestVersion()

			currVerMsg = 'Current Version: ' + __version__
			newVerMsg = 'SVN Version: ' + SVN_V

			if SVN_V != -1 and SVN_V > __version__ and \
				xbmcgui.Dialog().yesno(__plugin__,"New version available! ",  currVerMsg, newVerMsg, "Cancel", "Update"):
				dialogProgress.update(0, "Making backup ...")

				file = 'default.py'
				dest = os.path.join( local_backup_dir,file )
				src = os.path.join( local_dir,file )

				try:
					os.makedirs( local_backup_dir )
					log("created " + local_backup_dir)
				except:
					# exists, remove file
					try:
						os.remove(dest)
						log("removed " + dest)
					except: pass

				try:
					# copy to backup
					log("copy file from=" + src)
					copy(src, dest)
				except:
					errorOK(msg="Failed to backup file")
				else:
					dialogProgress.update(100, "Issuing update ...")
					cmd = "XBMC.RunPlugin(plugin://%s/%s/%s?updating=%s)" % ('video', '.backups', __plugin__,SVN_V )
					log("cmd=" + cmd)
					xbmc.executebuiltin(cmd)
					isUpdating = True
		elif version or path == local_backup_dir:
			dialogProgress.update(0, "Installing update ...")
			file = 'default.py'
			src = "/".join( [SVN_URL,version,file] )
			dest = os.path.join( local_dir,file )

			try:
				# remove orig
				os.remove(dest)
				log("remove orig dir=" + dest)
			except: pass

			log("urlretrieve src=%s dest=%s" % (src, dest))
			urllib.urlretrieve( src,  dest)

			dialogProgress.update(100)
			xbmcgui.Dialog().ok(__plugin__, "Update completed!", 'Please restart plugin')
			log('Update complete')
			isUpdating = True

		dialogProgress.close()
	except:
		dialogProgress.close()
		errorOK(msg="Update Failed!")

	log("< updateCheck() isUpdating=%s" % isUpdating)
	return isUpdating

# Get all Categories.
def getUlmenCats():
	log("> getUlmenCats()")
	res=[]
	url = BASE_URL + "/de/ulmentv/index.html"
	doc = getURL(url)
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
	doc = getURL(url)
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
	doc = getURL(url)
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
def getURL(url):
	""" read a doc from a url """
	try:
		safe_url = url.replace( " ", "%20" )
		log('getURL() url=%s' % safe_url)
		sock = urllib.urlopen( safe_url )
		doc = sock.read()
		sock.close()
		return unicode(doc, 'UTF-8')
	except:
		errorOK()
		return None

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
		url = 'http://xbmc.svn.sourceforge.net/svnroot/xbmc/trunk/XBMC/skin/Project%20Mayhem%20III/media/defaultVideoBig.png'
		fn = os.path.join(DIR_USERDATA, 'defaultVideoBig.png')
		fn = xbmc.translatePath(fn)
		if not os.path.isfile(fn):
			opener = urllib.FancyURLopener()
			fn, resp = opener.retrieve(url, fn)
			opener.close()
			os.path.isfile(fn)

	if fn and os.path.isfile(fn):
		return fn
	else:
		return ''
	
def get_params():
    """ extract params from argv[2] to make a dict (key=value) """
    paramDict = {}
    try:
        print "get_params() argv=", sys.argv
        if sys.argv[2]:
            paramPairs=sys.argv[2][1:].split( "&" )
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits))==2:
                    paramDict[paramSplits[0]] = paramSplits[1]
    except:
        errorOK()
    return paramDict
    
# add a link to directory
def addLink(name, url, img, mode):
	log("addLink() url=%s" % url)
	liz=xbmcgui.ListItem(name, '', img, img)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	url = fetchVideoLink(url)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	log("addLink() videourl=%s" % url)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

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
		infolabels = {}
		if not img:
			img = "DefaultVideo.png"
		if chname=='Neueste Videos':
			show = name
		else:
			show = "%s - %s - %s" % (chname, part, name)
		addLink(show,url,img,2)
	dialogProgress.close()
	
def playVideo(url,name):
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(str(url))

#######################################################################################################################    
# BEGIN !
#######################################################################################################################

updating = False
params=get_params()
if not params:
	# first run, check for update
	updating = updateCheck()
else:
	version = params.get("updating", None)
	if version:
		updating = updateCheck(version)

if not updating:
	try:
		# used to save thumbnail images
		d = xbmc.translatePath(DIR_USERDATA)
		os.makedirs( d )
		log("created " + d)
	except: pass

	try:
		# used to remove old thumbnails + folder
		d = xbmc.translatePath(DIR_USERDATA_OLD)
		if os.path.exists( d ):
			rmtree( d )
			log("removed " + d)
	except: pass

	url=urllib.unquote_plus(params.get("url", ""))
	name=urllib.unquote_plus(params.get("name",""))
	mode=int(params.get("mode","0"))
	log("Mode: "+str(mode))
	log("URL: "+str(url))
	log("Name: "+str(name))

	if mode==0 or not url:
		showCats(url,name)
	elif mode==1:
		showShows(url,name)
	elif mode==2:
		playVideo(url,name)
	ok = True
	xbmcplugin.endOfDirectory(int(sys.argv[1]), ok)
