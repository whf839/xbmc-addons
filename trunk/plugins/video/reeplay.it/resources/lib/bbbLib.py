"""
 bbbLib.py

 General functions.

 Cutdown version for reeplay.it
 
"""

import sys, os.path
import xbmc, xbmcgui
import os, re, unicodedata, traceback
from string import strip, replace, find, rjust, capwords
from shutil import rmtree

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__title__ = "bbbLib"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '25-02-2009'
xbmc.output("Imported From: " + __scriptname__ + " title: " + __title__ + " Date: " + __date__)

global dialogProgress
dialogProgress = xbmcgui.DialogProgress()

#######################################################################################################################    
# DEBUG - display indented information
#######################################################################################################################    
DEBUG = True
debugIndentLvl = 0	# current indentation level
def debug( value ):
	global debugIndentLvl
	if (DEBUG and value):
		try:
			if find(value,">") >= 0: debugIndentLvl += 2
			pad = rjust("", debugIndentLvl)
			print pad + str(value)
			if find(value,"<") >= 0: debugIndentLvl -= 2
		except:
			try:
				print value
			except:
				print "Debug() Bad chars in string"

#################################################################################################################
def messageOK(title='', line1='', line2='',line3=''):
#	debug("%s\n%s\n%s\n%s" % (title, line1,line2,line3))
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

#############################################################################################################
def makeDir(dir):
	try:
		d = xbmc.translatePath(dir)
		os.makedirs( d )
		debug("bbbLib.makeDir() " + d)
		return True
	except:
		return False

#################################################################################################################
# delete a single file
def deleteFile(filename):
	try:
		f = xbmc.translatePath(filename)
		os.remove( f )
		debug("bbbLib.deleteFile() " + f)
	except: pass

#################################################################################################################
def readFile(filename):
	try:
		f = xbmc.translatePath(filename)
		debug("bbbLib.readFile() " + f)
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
	debug("bbbLib.fileExist() %s  %s" % (f, exists))
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
	debug("> playMedia()")
	isPlaying = False

	try:
		if li:
			debug("player source fn/url with li")
			xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(source, li)
		else:
			debug("player source PlayList")
			xbmc.Player().play(source)
		isPlaying = xbmc.Player().isPlaying()
	except:
		traceback.print_exc()
		debug('xbmc.Player().play() failed trying xbmc.PlayMedia() ')
		try:
			cmd = 'xbmc.PlayMedia(%s)' % source
			xbmc.executebuiltin(cmd)
			isPlaying = True
		except:
			handleException('playMedia()')

	debug("< playMedia() isPlaying=%s" % isPlaying)
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
    debug("saveData() fn=%s" % fn)
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