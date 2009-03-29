"""

    Script to check for SVN Repo updates of your installed scripts and Plugins

    Written by BigBellyBilly
    Contact me at BigBellyBilly at gmail dot com - Bugs reports and suggestions welcome.

""" 

import sys, os
import os.path
import xbmc, xbmcgui
import urllib, urlparse
import re
import traceback
#from pprint import pprint

# Script constants
__scriptname__ = "Addons Update Checker"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/Addons%20Update%20Checker"
__date__ = '29-03-2009'
__version__ = "1.0"
xbmc.output( "[SCRIPT]: %s v%s Dated: %s started!" % (__scriptname__, __version__, __date__))

def log(msg):
	try:
		xbmc.output("[%s]: %s" % (__scriptname__, msg))
	except: pass

# check if build is special:// aware - set roots paths accordingly
XBMC_HOME = 'special://home'
if not os.path.isdir(xbmc.translatePath(XBMC_HOME)):	# if fails to convert to Q:, old builds
	XBMC_HOME = 'Q:'
log("XBMC_HOME=%s" % XBMC_HOME)

dialogProgress = xbmcgui.DialogProgress()

#############################################################################################################
class Main:

	URL_BASE_SVN_SCRIPTING = "http://xbmc-scripting.googlecode.com/svn"
	URL_BASE_SVN_ADDONS = "http://xbmc-addons.googlecode.com/svn"

	def __init__( self ):
		log("__init__()")

		SVN_BASE_LIST = (self.URL_BASE_SVN_ADDONS, self.URL_BASE_SVN_SCRIPTING)
		self.SVN_URL_LIST = []
		for base_url in SVN_BASE_LIST:
			self.SVN_URL_LIST.append( "/".join( [base_url, "trunk"] ) )  

		# create all XBMC script/plugin paths
		paths = ("plugins/programs","plugins/video","plugins/music","plugins/pictures","scripts")
		self.XBMC_PATHS = []
		for p in paths:
			self.XBMC_PATHS.append( xbmc.translatePath( "/".join( [XBMC_HOME, p] ) ) )

#		if xbmcgui.Dialog().yesno(__scriptname__, "Check for installed Script/Plugin updates?"):
		dialogProgress.create(__scriptname__)
		self.findInstalled()
		if self.INSTALLED:
			self.checkUpdates() 
		dialogProgress.close()

		if self.INSTALLED:
			self.showUpdates()

	#####################################################################################################
	def findInstalled(self):
		log("> findInstalled()")
		
		self.INSTALLED = []
		ignoreList = (".","..",".backups")
		dialogProgress.update(0, "Checking installed ...")
		TOTAL_PATHS = len(self.XBMC_PATHS)
		for count, p in enumerate(self.XBMC_PATHS):
			if not os.path.isdir(p): continue

			files = os.listdir(p)
			for f in files:
				# ignore parent dirs
				if f in ignoreList: continue

				percent = int( count * 100.0 / TOTAL_PATHS )
				dialogProgress.update(percent)

				# extract version
				try:
					filepath = os.path.join( p, f )
					doc = open( os.path.join(filepath, "default.py"), "r" ).read()
					ver = self.parseVersion(doc)
					self.INSTALLED.append({"filepath": filepath, "ver": ver})
				except:
					print str(sys.exc_info()[ 1 ])

#		pprint (self.INSTALLED)
		log("< findInstalled()  installed count=%d" % len(self.INSTALLED))

		
	#####################################################################################################
	def checkUpdates(self):
		log("> checkUpdates()")

		actionMsg = "Checking SVN ..."
		dialogProgress.update(0, actionMsg)

		TOTAL_PATHS = len(self.INSTALLED)
		quit = False
		for count, info in enumerate(self.INSTALLED):
			log("%d checking installed=%s" % (count, info))

			if not info['ver']: continue			# ignore installed without version doc tag

			# find installed category from filepath
			installedCategory  = self.parseCategory(info['filepath'])

			for base_url in self.SVN_URL_LIST:
				# xbmc-scripting has no 'scripts' in svn path, so remove it from installedCategory
				if base_url.startswith(self.URL_BASE_SVN_SCRIPTING):
					installedCategory = installedCategory.replace('scripts/','')
				url = "/".join( [base_url, installedCategory, "default.py"] )
				log("svn url=" + url)

				percent = int( count * 100.0 / TOTAL_PATHS )
				dialogProgress.update(percent, actionMsg, installedCategory, urlparse.urlparse(url)[1])
				if dialogProgress.iscanceled():
					quit = True
					break

				# download default.py
				try:
					sock = urllib.urlopen( url.replace(' ','%20') )
					doc = sock.read()
					sock.close()
				except:
					print str(sys.exc_info()[ 1 ])
				else:
					# check __version__ tag
					svn_ver = self.parseVersion(doc)
					if svn_ver:
						self.INSTALLED[count]['svn_ver'] = svn_ver
						self.INSTALLED[count]['svn_url'] = url
						break # found in svn, move to next installed

			if quit: break

#		pprint (self.INSTALLED)
		log("< checkUpdates() updated count=%d" % len(self.INSTALLED))

	#####################################################################################################
	def parseVersion(self, doc):
		try:
			ver = re.search("__version__.*?[\"'](.*?)[\"']",  doc, re.IGNORECASE).group(1)
		except:
			ver = ""
		log("parseVersion() version=%s" % ver)
		return ver

	#####################################################################################################
	def parseCategory(self, filepath):
		try:
			cat = re.search("(plugins.*|scripts.*)$",  filepath, re.IGNORECASE).group(1)
			cat = cat.replace("\\", "/")
		except:
			ver = ""
		log("parseCategory() cat=%s" % cat)
		return cat

	#####################################################################################################
	def showUpdates(self):
		log("> showUpdates()")

		# create display list
		results = []
		for info in self.INSTALLED:
			ver = info['ver']
			svn_ver = info.get('svn_ver','')
			if not ver:
				verState = "Unknown Version"
				ver = "?"
			elif not svn_ver:
				verState = "Not in SVN"
			elif ver >= svn_ver:
				verState = "OK"
			else:
				verState = "New! v" + svn_ver
			text = "%s v%s  : %s" % (self.parseCategory(info['filepath']), ver, verState)
			results.append(text)

		# show results
		selectedPos = 0
		while selectedPos >= 0:
			selectedPos = xbmcgui.Dialog().select(__scriptname__, results)
			if selectedPos >= 0:
				# call update Plugin
				if "New!" in results[selectedPos]:
					#runPath = "special://home/plugins/Programs/SVN Repo Installer/default.py"
					runPath = "plugin://programs/SVN Repo Installer"
					command = 'XBMC.ActivateWindow(10001,%s)'% (runPath)    # for folder plugins
					#command = 'XBMC.RunPlugin(%s)'% (runPath)
					log(command)
					xbmc.executebuiltin(command)
					break
		
		log("< showUpdates()")

#################################################################################################################
 # Starts here
#################################################################################################################
try:
	Main()
except:
	log( str(sys.exc_info()[ 1 ]) )

# remove globals
try:
	del dialogProgress
except: pass
