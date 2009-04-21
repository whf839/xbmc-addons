"""
 Supporting shared functions for Plugin
"""

import os, sys, os.path, re
from urllib import quote_plus, unquote_plus, urlretrieve, urlcleanup
from string import find
import xbmc, xbmcgui

from pluginAPI.xbmcplugin_const import *

__plugin__ = sys.modules[ "__main__" ].__plugin__

#################################################################################################################
def log(msg, loglevel=xbmc.LOGDEBUG):
	try:
		xbmc.log("[%s]: %s" % (__plugin__, msg), loglevel)
	except: pass

#################################################################################################################
def logError():
	log("ERROR: %s" % sys.exc_info()[ 1 ])

#################################################################################################################
def messageOK(title='', line1='', line2='',line3=''):
	xbmcgui.Dialog().ok(title ,line1,line2,line3)

#################################################################################################################
def handleException(msg=''):
	import traceback
	traceback.print_exc()
	messageOK(__plugin__ + " ERROR!", msg, str(sys.exc_info()[ 1 ]) )

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
		data = decodeText(data)
		if breaksToNewline:
			data = data.replace('<br>','\n').replace('<p>','\n')
		reobj = re.compile('<.+?>', re.IGNORECASE+re.DOTALL+re.MULTILINE)
		return re.sub(reobj, '', data).replace('\n\n','\n')
	except:
		logError()
		return data

#################################################################################################################
def findImgSrc(text):
	try:
		return re.search('src="(.*?(?:.png|.jpg))"', text, re.IGNORECASE).group(1)
	except:
		try:
			return re.search('(http://.*?(?:.png|.jpg))"', text, re.IGNORECASE).group(1)
		except:
			return ''

#################################################################################################################
def encodeText(text):
	""" convert chars to make suitable for url """
	return repr( quote_plus(text.replace("'", '"')) )

#################################################################################################################
def decodeText(text):
	""" convert chars from url encoding to normal chars """
	text = text.replace("\\u0027", "'").replace("\\u0022",'"').replace("\\u0026","&").replace("&quot;","'").replace("&#39;","'").replace("&amp;","&")
	text = text.replace("&lt;","<").replace("&gt;",">").replace('\\003c','<').replace('\\u003e','>')
	try:
		return unquote_plus(text).decode("unicode-escape")
	except:
		return unquote_plus(text)

########################################################################################################################
def get_thumbnail(thumbnail_url, allowDownload=True ):
	log("get_thumbnail() %s" % thumbnail_url)
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
		print str(sys.exc_info()[ 1 ])
		return thumbnail_url       
