"""
	SVN Repo Installer - Actions
"""

import sys, os
import os.path
import re
import xbmc, xbmcgui
from xbmcplugin_lib import *
from shutil import rmtree, copytree

__plugin__ = sys.modules["__main__"].__plugin__
__date__ = '22-04-2009'
log("Module: %s Dated: %s loaded!" % (__name__, __date__))

class Main:

	INSTALLED_ITEMS_FILENAME = os.path.join( os.getcwd(), "installed_items.dat" )
	
	def __init__( self ):
		log(__name__ + " started!")
		try:
			self._parse_argv()
			if ( self.args.has_key("delete") ):
				self.delete_update_item()
		except Exception, e:
			xbmcgui.Dialog().ok(__plugin__ + " ERROR!", str(e))

	########################################################################################################################
	def _parse_argv(self):
		# call Info() with our formatted argv to create the self.args object
		exec "self.args = Info(%s)" % ( unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )

	########################################################################################################################
	def delete_update_item(self):
		log("delete_update_item()")

		if xbmcgui.Dialog().yesno(__plugin__, self.args.title,"", "", xbmc.getLocalizedString( 30020 ), xbmc.getLocalizedString( 30022 )):	# Delete, Skip
			items = loadFileObj(self.INSTALLED_ITEMS_FILENAME)
			filepath = self.args.delete
			# find addon from installed list
			for i, item in enumerate(items):
				if item['filepath'] == filepath:
					log("addon details: %s" % item)
					# make backup - if not deleting a backup copy
					if ".backup" not in filepath:
						backupPath, category = self.makeBackup(filepath)
						removeList = False
					else:
						category = self.parseCategory(filepath)
						backupPath = filepath
						removeList = True
					if backupPath and category:
						# remove addon dir tree
						try:
							rmtree(filepath)
							log("dir deleted: " + filepath)

							# update list with new filepath, or remove from list if delting backup
							if removeList:
								del items[i]
							else:
								# update filepath to indicated Deleted
								items[i]['filepath'] = backupPath
							saveFileObj(self.INSTALLED_ITEMS_FILENAME, items)
							if not removeList:
								xbmcgui.Dialog().ok(__plugin__, xbmc.getLocalizedString( 30018 ), xbmc.getLocalizedString( 30004 ), category)
							else:
								xbmcgui.Dialog().ok(__plugin__, xbmc.getLocalizedString( 30018 ), category)	 # no backup
							# force list refresh
							xbmc.executebuiltin('Container.Refresh')
						except:
							handleException("delete_update_item()")
					break

	#####################################################################################################
	def parseCategory(self, filepath):
		try:
			cat = re.search("(plugins.*|scripts.*)$",  filepath, re.IGNORECASE).group(1)
			cat = cat.replace("\\", "/")
		except:
			cat = ""
		log("parseCategory() cat=%s" % cat)
		return cat

	########################################################################################################################
	def makeBackup( self, installedPath ):
		""" copy addon to <addon_category>/.backups """
		log("> makeBackup() installedPath=%s" % installedPath)

		try:
			category = ""
			if installedPath[-1] == os.sep:
				installedPath = installedPath[:-1]

			# extract rootpath , addon name
			matches = re.search("(.*)[\\\/](.*?)$", installedPath)
			rootpath = matches.group(1)
			name = matches.group(2)
			log("rootpath=%s name=%s" % (rootpath, name))

			# create root backup path
			backupPath = os.path.join(rootpath, ".backups")
			log("backupPath=%s" % backupPath)
			# make root backup dir
			try:
				os.makedirs(backupPath)
				log("created dir " + backupPath )
			except: pass

			# remove any existing backup
			try:
				backupPath = os.path.join(backupPath, name)
				rmtree( backupPath, ignore_errors=True )		
				log("removed existing dir " + backupPath)
			except: pass

			# copy to backup path
			copytree(installedPath, backupPath)
			log("copytree success")

			# extract category in .backups
			category = re.search("(plugins.*|scripts.*)$", backupPath).group(1)
			# check file exists in backup
			if not os.path.exists(os.path.join(backupPath, "default.py")):
				xbmcgui.Dialog().ok(__plugin__, "Make backup failed!", category)
				backupPath = ""
		except:
			handleException("makeBackup()")
			backupPath = ""
		log("< makeBackup() backupPath=%s category=%s" % (backupPath, category))
		return (backupPath, category)

	def _parseCategoryPath(self):
			# extract category in .backups
			category = re.search("(plugins.*|scripts.*)$", backupPath).group(1)


	
#def deleteInstalledFile():
#	try:
#		os.remove(Main.INSTALLED_ITEMS_FILENAME)
#		log("deleteInstalledFile() deleted: " + Main.INSTALLED_ITEMS_FILENAME)
#	except: pass

if ( __name__ == "__main__" ):
	Main()

