"""
Update module - PLUGIN VERSION

Changes:
18-11-2007 
 Use language self.pluginName in dialogs instead of __scriptname__
 Used regex to parse svn.
 Added a 'silent' mode.
 Changed to use YES/NO string ids.
02-01-2008 Fixed error in downloadVersion()
06-02-2008 Changed to update into same folder
28-02-2008 removed a syntax error when not isSilent
20-02-2008 Altered to save script backup into Q:\\scripts\\backups subfolder. Makes the scripts folder cleaner.
20-04-2008 Fix makedir of backup folder.
02-05-2008 \backups renamed to \.backups in anticipation of xbmc adopting hidden folder prefixed with '.'
12-09-2008 use os.path.join instead of string +
10-10-2008 Fix: to use xbmc.language from __main__
           Fix: Created folders replaced %20 with a space
11-02-2009 Change: To use xbmc.translatePath() which converts Q: T: etc to their special:// equiv.
            Replace os.path.join with "/".join( [ ] ) as all paths now url form, using '/'
13-02-2009 Change: Plugin version: Using svn xbmc-addons.googlecode.com
"""

import sys
import os
import xbmcgui, xbmc
import urllib
import re
import traceback
from shutil import copytree, rmtree

def log(msg):
	try:
		xbmc.output("[%s]: %s" % (__name__, msg))
	except: pass

# check if build is special:// aware - set roots paths accordingly
XBMC_HOME = 'special://home'
if not os.path.isdir(xbmc.translatePath(XBMC_HOME)):	# if fails to convert to Q:, old builds
	XBMC_HOME = 'Q:'
log("XBMC_HOME=%s" % XBMC_HOME)


class UpdatePlugin:
	""" Update Class: used to update from xbmc google svn repo """

#	URL_BASE = "http://xbmc-scripting.googlecode.com/svn"
	URL_BASE = "http://xbmc-addons.googlecode.com/svn"
	
	def __init__( self, language, pluginName, pluginType ):
		log( "_init_ pluginName=%s pluginType=%s" % (pluginName, pluginType) )

		self._ = language
		self.pluginName = pluginName
		self.pluginType = pluginType

		self.URL_TAGS = "%s/tags/plugins/%s/%s/" % ( self.URL_BASE, pluginType, pluginName)
		local_base_dir = "/".join( [XBMC_HOME,'plugins', pluginType] )
		self.local_dir = xbmc.translatePath( "/".join( [local_base_dir, pluginName] ) )
		self.backup_base_dir = xbmc.translatePath( "/".join( [local_base_dir,'.backups'] ) )
		self.local_backup_dir = os.path.join( self.backup_base_dir, pluginName )

		log("URL_BASE=" + self.URL_BASE)
		log("URL_TAGS=" + self.URL_TAGS)
		log("local_dir=" + self.local_dir)
		log("local_backup_dir=" + self.local_backup_dir)

		self.dialog = xbmcgui.DialogProgress()


	def downloadVersion( self, version ):
		""" main update function """
		log( "> downloadVersion() version=%s" % version)
		success = False
		try:
			self.dialog.create( self.pluginName, self._( 1004 ), self._( 1005 ) )
			folders = [version]
			script_files = []
			# recusivly look for folders and files
			while folders:
				try:
					htmlsource = self.getHTMLSource( '%s%s' % (self.URL_TAGS, folders[0]) )
					if htmlsource:
						# extract folder/files stored in path
						itemList, url = self.parseHTMLSource( htmlsource )

						# append folders to those we're looping throu and store file
						for item in itemList:
							if item[-1] == "/":
								folders.append( ("%s/%s" % (folders[ 0 ], item)) )
							else:
								file = "%s/%s" % (folders[ 0 ], item)
								script_files.append( file.replace('//','/') )
					else:
						log("no htmlsource found")
						raise
					folders = folders[1:]
				except:
					folders = None

			if not script_files:
				log("empty script_files - raise")
				raise
			else:
				success = self.getFiles( script_files, version )
		except:
			traceback.print_exc()
			xbmcgui.Dialog().ok( self.pluginName, self._( 1031 ) )

		self.dialog.close()
		log("< downloadVersion() success = %s" % success)
		return success

	def getLatestVersion( self, silent=True ):
		""" checks for latest tag version """
		version = "-1"
		try:
			if not silent:
				self.dialog.create( self.pluginName, self._( 1001 ) )

			# get version tags
			htmlsource = self.getHTMLSource( self.URL_TAGS )
			if htmlsource:
				tagList, url = self.parseHTMLSource( htmlsource )
				if tagList:
					version = tagList[-1].replace("/","")  # remove trailing /
		except:
			traceback.print_exc()
			xbmcgui.Dialog().ok( self.pluginName, self._( 1031 ), str( sys.exc_info()[ 1 ] ) )
		self.dialog.close()

		log( "getLatestVersion() new version=%s" % version )
		return version

	def makeBackup( self ):
		log("> makeBackup()")
		self.removeBackup()
		# make base backup dir
		try:
			os.makedirs(self.backup_base_dir)
			log("created dirs=%s" % self.backup_base_dir )
		except: pass

		try:
			copytree(self.local_dir, self.local_backup_dir)
		except:
			traceback.print_exc()
			xbmcgui.Dialog().ok( "Error Making Script Backup!", str( sys.exc_info()[ 1 ] ) )
		log("< makeBackup()")

	def issueUpdate( self, version ):
		log("> issueUpdate() version=%s" % version)
		path = os.path.join( self.local_backup_dir, 'resources','lib','update.py' )
		command = 'XBMC.RunScript(%s,%s,%s,%s)'%(path, self.pluginName.replace('%20',' '), self.pluginType, version)
		log(command)
		xbmc.executebuiltin(command)
		log("< issueUpdate() done")
	
	def removeBackup( self ):
		try:
			rmtree(self.local_backup_dir,ignore_errors=True)		
			log("removeBackup() removed OK")
		except: pass
	
	def removeOriginal( self ):
		try:
			rmtree(self.local_dir,ignore_errors=True)
			log("removeOriginal() removed OK")
		except:
			traceback.print_exc()
		
	def backupExists( self ):
		exists = os.path.exists(self.local_backup_dir)
		log("backupExists() %s" % exists)
		return exists

	def getFiles( self, script_files, version ):
		""" fetch the files from svn """
		log( "getFiles() version=%s" % version )
		success = False
		try:
			totalFiles = len(script_files)
			log("getFiles() totalFiles=%d" % totalFiles)
			for cnt, url in enumerate( script_files ):
				items = os.path.split( url )
				path = os.path.join( self.local_dir, items[0] ).replace( version+'/', '' ).replace( version, '' ).replace( '//', '/' ).replace( '%20', ' ' )
				file = items[ 1 ].replace( '%20', ' ' )
				pct = int( ( float( cnt ) / totalFiles ) * 100 )
				self.dialog.update( pct, "%s %s" % ( self._( 1007 ), url, ), "%s %s" % ( self._( 1008 ), path, ), "%s %s" % ( self._( 1009 ), file, ) )
				if ( self.dialog.iscanceled() ): raise
				if ( not os.path.isdir( path ) ):
					os.makedirs( path )
				src = "%s%s" % (self.URL_TAGS, url)
				dest = os.path.join( path, file ).replace( '%20', ' ' )
				src = src.replace(' ','%20')
				log("urlretrieve src=%s dest=%s" % (src, dest))
				urllib.urlretrieve( src,  dest)

			success = True
		except:
			raise
		return success

	def getHTMLSource( self, url ):
		""" read a doc from a url """
		safe_url = url.replace( " ", "%20" )
		log( "getHTMLSource() " + safe_url)
		try:
			sock = urllib.urlopen( safe_url )
			doc = sock.read()
			sock.close()
			return doc
		except:
			traceback.print_exc()
			xbmcgui.Dialog().ok( self.pluginName, "HTTP Error", str( sys.exc_info()[ 1 ] ) )
			return None

	def parseHTMLSource( self, htmlsource ):
		""" parse html source for tagged version and url """
		log( "parseHTMLSource()" )
		try:
			url = re.search('Revision \d+:(.*?)<', htmlsource, re.IGNORECASE).group(1).strip()
			tagList = re.compile('<li><a href="(.*?)"', re.MULTILINE+re.IGNORECASE+re.DOTALL).findall(htmlsource)
			if tagList[0] == "../":
				del tagList[0]
			return tagList, url
		except:
			return None, None

if __name__ == "__main__":
	log("update.py running from __main__")

	# expects lang, pluginName, pluginType
	if len(sys.argv) != 4:
		xbmcgui.Dialog().ok("Update Error",  "Not enough arguments were passed for update")
		sys.exit(1)

	try:
		pluginName = sys.argv[1]
		pluginType = sys.argv[2]
		version = sys.argv[3]
		lang_path = xbmc.translatePath( "/".join( [XBMC_HOME, "plugins", pluginType, pluginName] ) )
		__lang__ = xbmc.Language( lang_path ).getLocalizedString
		up = UpdatePlugin(__lang__, pluginName, pluginType)
		up.removeOriginal()
		up.downloadVersion(version)
#		cmd = "XBMC.RunPlugin(plugin://%s/%s/)" % (pluginType, pluginName )
#		xbmc.output("Updated relaunch cmd=" + cmd)
#		xbmc.executebuiltin(cmd)
		xbmcgui.Dialog().ok(pluginName, __lang__(1010), "v"+version)
	except:
		traceback.print_exc()
		xbmcgui.Dialog().ok( "Update Error", "Failed to start update from backup copy!", str( sys.exc_info()[ 1 ] ))
