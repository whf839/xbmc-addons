"""
 Supporting shared functions for Plugin
"""

import os, sys, traceback, os.path, re
from urllib import quote_plus, unquote_plus, unquote, urlretrieve, urlcleanup
from string import find
import xbmc, xbmcgui, xbmcplugin

from pluginAPI.xbmcplugin_const import *

__plugin__ = sys.modules[ "__main__" ].__plugin__
xbmc.output("Loading from: %s Module: %s" % (__plugin__, __name__))

#################################################################################################################
def log(msg):
	try:
		xbmc.output("[%s]: %s" % (__plugin__, msg))
	except: pass

#################################################################################################################
def logError():
	log("ERROR: %s" % sys.exc_info()[ 1 ])

#################################################################################################################
def messageOK(title='', line1='', line2='',line3=''):
	xbmcgui.Dialog().ok(title ,line1,line2,line3)

#################################################################################################################
def handleException(msg=''):
	traceback.print_exc()
	messageOK(__plugin__ + " ERROR!", msg, str(sys.exc_info()[ 1 ]) )

#################################################################################################################
def xbmcBuildError():
	messageOK(__plugin__,"XBMC Builtin Error", "Please update your XBMC build.", str(sys.exc_info()[ 1 ]))

#################################################################################################################
def loadFileObj( filename, dataType={} ):
	log( "loadFileObj() " + filename)
	try:
		file_handle = open( xbmc.translatePath(filename), "r" )
		loadObj = eval( file_handle.read() )
		file_handle.close()
	except:
		# reset to empty according to dataType
		if isinstance(dataType, dict):
			loadObj = {}
		elif isinstance(dataType, list) or isinstance(dataType, tuple):
			loadObj = ()
		else:
			loadObj = None
	return loadObj

#################################################################################################################
def saveFileObj( filename, saveObj ):
	log( "saveFileObj() " + filename)
	try:
		file_handle = open( xbmc.translatePath(filename), "w" )
		file_handle.write( repr( saveObj ) )
		file_handle.close()
		return True
	except:
		handleException( "_save_file_obj()" )
		return False

#################################################################################################################
# delete a single file
def deleteFile(filename):
	try:
		os.remove(xbmc.translatePath(filename))
		log("deleteFile() deleted: " + filename)
	except: pass

#################################################################################################################
# look for html between < and > chars and remove it
def cleanHTML(data, breaksToNewline=True):
	if not data: return ""
	try:
		if breaksToNewline:
			data = data.replace('<br>','\n').replace('<p>','\n')
		reobj = re.compile('<.+?>', re.IGNORECASE+re.DOTALL+re.MULTILINE)
		return decodeText(re.sub(reobj, '', data)).replace('\n\n','\n')
	except:
		logError()
		return data

#################################################################################################################
def findImgSrc(text):
	try:
		return re.search('src="(.*?(?:.png|.jpg))"', text, re.IGNORECASE).group(1)
	except:
		return ''

#################################################################################################################
def encodeText(text):
	""" convert chars to make suitable for url """
	return repr( quote_plus(text.replace("'", "\\u0027")) )

#################################################################################################################
def decodeText(text):
	""" convert chars from url encoding to normal chars """
	text = text.replace("\\u0027", "'").replace("\\u0022",'"').replace("\\u0026","&").replace("&quot;","'").replace("&#39;","'").replace("&amp;","&")
	text = text.replace("&lt;","<").replace("&gt;",">")
	return unquote_plus(text)


########################################################################################################################
def get_thumbnail(thumbnail_url, allowDownload=True ):
	# make the proper cache filename and path so duplicate caching is unnecessary
	if ( not thumbnail_url.startswith( "http://" ) ): return thumbnail_url
	try:
		filename = xbmc.getCacheThumbName( thumbnail_url )
		filepath =xbmc.translatePath( os.path.join( BASE_CACHE_PATH, filename[ 0 ], filename ) )
		# if the cached thumbnail does not exist fetch the thumbnail
		if not os.path.isfile( filepath ):
			if allowDownload:
				# fetch thumbnail and save to filepath
				log("get_thumbnail() downloading from=%s to %s" % (thumbnail_url, filepath))
				info = urlretrieve( thumbnail_url, filepath )
				# cleanup any remaining urllib cache
				urlcleanup()
			else:
				return thumbnail_url
		else:
			log("get_thumbnail() use existing=" + filepath)
		return filepath
	except:
		# return empty string if retrieval failed
		handleException()
		return ""        

########################################################################################################################
def checkBuildDate(scriptName, minDate):
	""" Check if XBMC build is new enough to run script """
	log( "> checkBuildDate() minDate=%s" % minDate )
	import time

	# get system build date info
	buildDate = xbmc.getInfoLabel( "System.BuildDate" )
	curr_build_date_t = time.strptime(buildDate,"%b %d %Y")			# create time_t
	curr_build_date_secs = time.mktime(curr_build_date_t)				# convert to epoc secs
	curr_build_date_formated  = time.strftime("%d-%m-%Y", curr_build_date_t)	# format to text date

	# compare with required min date
	min_build_date_t = time.strptime(minDate,"%d-%m-%Y")				# DD-MM-YYYY to time_t
	min_build_date_secs = time.mktime(min_build_date_t)				# convert to epoc secs

	log("XBMC Date: %s secs: %s    Required Date: %s secs: %s" % \
		(buildDate, curr_build_date_secs, minDate, min_build_date_secs))
	
	if curr_build_date_secs < min_build_date_secs:							# No new build
		messageOK(scriptName, "Your XBMC build is older than required.", "Required: " + minDate, "Current: " + curr_build_date_formated)
		ok = False
	else:
		ok = True

	log("< checkBuildDate() ok=%s" % ok)
	return ok

######################################################################################
def checkUpdate( currVersion, silent=False, notifyNotFound=False):
	log( "> checkUpdate()")

	try:
		updated = False
		import update
		__lang__ = xbmc.Language( os.getcwd() ).getLocalizedString
		up = update.UpdatePlugin(__lang__, __plugin__, "programs")      # svn folder for plugin type is case sensitive
		version = up.getLatestVersion(silent)
		log("Current Version: %s Tag Version: %s" % (currVersion, version))
		if version and version != "-1":
			if currVersion < version:
				if xbmcgui.Dialog().yesno( __plugin__, \
									"%s %s %s." % ( __lang__(1006), version, __lang__(1002) ), \
									__lang__(1003)):
					up.makeBackup()
					up.issueUpdate(version)
					updated = True
			elif notifyNotFound:
				messageOK(__plugin__, __lang__(1000))
		elif not silent:
			messageOK(__plugin__, __lang__(1030))				# no tagged ver found

		del up
	except:
		handleException("checkUpdate()")
	log( "< checkUpdate() updated=%s" % updated)
	return updated

