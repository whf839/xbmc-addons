import os, sys
import xbmc, xbmcgui

# Script constants
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '16-06-2009'
xbmc.log( "[PLUGIN] Module: %s Dated: %s loaded!" % (__name__, __date__), xbmc.LOGDEBUG)

#################################################################################################################
class TextViewDialog( xbmcgui.WindowXMLDialog ):
	""" A TextView window """

	XML_FILENAME = "DialogScriptInfo.xml"
	EXIT_CODES = (9, 10, 216, 257, 275, 216, 61506, 61467,)

	def __init__( self, *args, **kwargs):
		xbmc.log( "[PLUGIN] %s __init__!" % (self.__class__), xbmc.LOGDEBUG )
		self.text = ""
		self.title = ""

	def onInit( self ):
		try:
			self.getControl( 5 ).setText( "[I]%s[/I]\n%s" % (self.title, self.text) )
			self.getControl( 3 ).setLabel( self.title )
		except: pass

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

	def ask(self, title="", text="", fn=None ):
		if not title and fn:
			self.title = os.path.basename(fn)
		else:
			self.title = title
		if fn:
			try:
				self.text = file(xbmc.translatePath(fn)).read()
			except:
				self.text = "Failed to load file: %s" % fn
		else:
			self.text = text

		self.doModal()

def Main():
	# called from a Plugin to view local Readme/Changelog
	if sys.argv[ 2 ] and "info=" in sys.argv[ 2 ]:
		filename = sys.argv[ 2 ].split('=')[1]      # get filename
		filepath = os.path.join( os.getcwd(),"resources", filename )
	else:
		fn = None

	TextViewDialog( TextViewDialog.XML_FILENAME, os.getcwd(), "Default" ).ask( fn=filepath )

if ( __name__ == "__main__" ):
	Main()    
