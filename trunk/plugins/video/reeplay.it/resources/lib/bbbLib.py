"""
 bbbLib.py

 General functions.

 Cutdown version for reeplay.it
 
"""

import sys, os.path
import xbmc, xbmcgui
import os, re, unicodedata, traceback
from string import strip, replace, find, rjust
from shutil import rmtree

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__title__ = "bbbLib"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '25-02-2009'
xbmc.output("Imported From: " + __scriptname__ + " title: " + __title__ + " Date: " + __date__)

global dialogProgress
dialogProgress = xbmcgui.DialogProgress()

#################################################################################################################
def log(msg):
	try:
		xbmc.output("[%s]: %s" % (__scriptname__, msg))
	except: pass

def debug(msg):
    log(msg)

#################################################################################################################
def logError():
	log("ERROR: %s" % sys.exc_info()[ 1 ])

#################################################################################################################
def messageOK(title='', line1='', line2='',line3=''):
	xbmcgui.Dialog().ok(title ,line1,line2,line3)

#################################################################################################################
def handleException(txt=''):
	try:
		title = "EXCEPTION: " + txt
		e=sys.exc_info()
		list = traceback.format_exception(e[0],e[1],e[2],3)
		text = ''
		for l in list:
			text += l
		traceback.print_exc()
		messageOK(title, text)
	except: pass

#################################################################################################################
def xbmcBuildError():
	messageOK(__scriptname__,"XBMC Builtin Error", "Please update your XBMC build.", str(sys.exc_info()[ 1 ]))

#############################################################################################################
def makeDir(dir):
	try:
		d = xbmc.translatePath(dir)
		os.makedirs( d )
		log("bbbLib.makeDir() " + d)
		return True
	except:
		return False

#################################################################################################################
# delete a single file
def deleteFile(filename):
	try:
		f = xbmc.translatePath(filename)
		os.remove( f )
		log("bbbLib.deleteFile() " + f)
	except: pass

#################################################################################################################
def readFile(filename):
	try:
		f = xbmc.translatePath(filename)
		log("bbbLib.readFile() " + f)
		return file(f).read()
	except:
		return ""

#################################################################################################################
def fileExist(filename):
	exists = False
	try:
		f = xbmc.translatePath(filename)
		if os.path.isfile(f) and os.path.getsize(f) > 0:
			exists = True
	except: pass
	log("bbbLib.fileExist() %s  %s" % (f, exists))
	return exists


#################################################################################################################
# Thanks to Arboc for this
#################################################################################################################
def unicodeToAscii(text, charset='utf8'):
	if not text: return ""
	try:
		newtxt = text.decode(charset)
		newtxt = unicodedata.normalize('NFKD', newtxt).encode('ASCII','replace')
		return newtxt
	except:
		return text

##############################################################################################################    
def playMedia(source, li=None):
	log("> playMedia()")
	isPlaying = False

	try:
		if li:
			log("player source fn/url with li")
			xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(source, li)
		else:
			log("player source PlayList")
			xbmc.Player().play(source)
		isPlaying = xbmc.Player().isPlaying()
	except:
		traceback.print_exc()
		log('xbmc.Player().play() failed trying xbmc.PlayMedia() ')
		try:
			cmd = 'xbmc.PlayMedia(%s)' % source
			xbmc.executebuiltin(cmd)
			isPlaying = True
		except:
			handleException('playMedia()')

	log("< playMedia() isPlaying=%s" % isPlaying)
	return isPlaying

#################################################################################################################
def searchRegEx(data, regex, flags=re.IGNORECASE):
	try:
		value = re.search(regex, data, flags).group(1)
	except:
		value = ""
	return value

#################################################################################################################
def findAllRegEx(data, regex, flags=re.MULTILINE+re.IGNORECASE+re.DOTALL):
	try:
		matchList = re.compile(regex, flags).findall(data)
	except:
		matchList = []

	if matchList:
		sz = len(matchList)
	else:
		sz = 0
	debug ("findAllRegEx() matches=%s" % sz)
	return matchList

##############################################################################################################
def saveData(data, fn, mode="w"):
    """ Save data to a file """
    if not data or not fn or not mode: return False
    log("saveData() fn=%s" % fn)
    try:
        f = open(xbmc.translatePath(fn), mode)
        f.write(data)
        f.flush()
        f.close()
        del f
        return True
    except:
        traceback.print_exc()
        return False

######################################################################################
def bbbTranslatePath(partsList):
    return xbmc.translatePath( "/".join(partsList) )

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

