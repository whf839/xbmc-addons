"""
	Category module: list of categories to use as folders
"""

# main imports
import os, sys, traceback
from urllib import urlretrieve, urlcleanup
from string import find
import xbmc, xbmcgui, xbmcplugin

from pluginAPI.xbmcplugin_const import *
from pluginAPI.bbbLib import get_thumbnail, log, handleException, loadFileObj, decodeText
  
#################################################################################################################
class DialogVideoInfo( xbmcgui.WindowXMLDialog ):
	""" Show skin DialogVideoInfo with our information """

	XML_FILENAME = "script-GoogleReader-iteminfo.xml"
	EXIT_CODES = (9, 10, 216, 257, 275, 216, 61506, 61467,)
	
	def __init__( self, *args, **kwargs):
		pass
		
	def onInit( self ):
		log( "DialogVideoInfo.onInit()" )
		title = self.info['title']
		image = self.info['image']
		updated = self.info['updated']
		content = self.info['content']
		author = self.info['author']

		self.getControl( 4 ).setLabel( title )
		self.getControl( 5 ).setText( content )
		self.getControl( 6 ).setImage( image )
		self.getControl( 21 ).setLabel( updated )
		self.getControl( 23 ).setLabel( author )
		
	def onClick( self, controlId ):
		pass

	def onFocus( self, controlId ):
		pass

	def onAction( self, action ):
		try:
			buttonCode =  action.getButtonCode()
			actionID   =  action.getId()
		except: return
		if actionID in self.EXIT_CODES or buttonCode in self.EXIT_CODES:
			self.close()

	def ask(self, info ):
#		pprint (info)
		self.info = info
		self.doModal()

#################################################################################################################
class _Info:
	def __init__(self, *args, **kwargs ):
		self.__dict__.update( kwargs )
		log( "Info() self.__dict__=%s" % self.__dict__ )
	def has_key(self, key):
		return self.__dict__.has_key(key)


#################################################################################################################
#################################################################################################################
class Main:
	def __init__( self ):
		self._parse_argv()                      # parse sys.argv

		exec "ok = self.%s()" % ( self.args.category, )

		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok)

	########################################################################################################################
	def _parse_argv(self):
		if ( not sys.argv[ 2 ] ):
			self.args = _Info( title="" )
		else:
			# call Info() with our formatted argv to create the self.args object
			# replace & with , first as they're the args split char.  Then decode.
			exec "self.args = _Info(%s)" % ( decodeText( (sys.argv[ 2 ][ 1 : ]).replace( "&", ", " ) ), )

	########################################################################################################################
	def show_item(self):
		log("> show_item()")
		ok = False

		try:
			continuation = self.args.continuation
			# load items file and get reqd item using google_id
			item = loadFileObj(ITEMS_FILENAME % continuation)[self.args.google_id]

			# download image if not exist (may not have been fetched when item list made as per settings)
			item['image'] = get_thumbnail(item['image'])

			# show item
			DialogVideoInfo(DialogVideoInfo.XML_FILENAME,HOME_DIR, "Default", False ).ask(item)
			ok = True
		except:
			handleException(self.__class__.__name__)

		log("< show_item()  ok=%s" % ok)
		return ok
