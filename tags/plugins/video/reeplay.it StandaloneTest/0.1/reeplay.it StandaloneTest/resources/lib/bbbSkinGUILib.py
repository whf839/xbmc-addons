"""

 bbbSkinGUILib - Skinned (windowXML/dialogXML) objects.

"""
import xbmc, xbmcgui, sys

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__title__ = "bbbSkinGUILib"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '10-02-2009'
xbmc.output("Imported From: " + __scriptname__ + " title: " + __title__ + " Date: " + __date__)

PAD_A                   = 256
PAD_B                   = 257
PAD_X                   = 258
PAD_Y                   = 259
ACTION_A	            = 7
ACTION_X 	            = 18    # X
ACTION_Y 	            = 34	# Y
ACTION_B	            = 9     # B
ACTION_REMOTE_STOP		= 13	# remote
KEYBOARD_X              = 61528
KEYBOARD_A              = 61505
KEYBOARD_B              = 61506
KEYBOARD_Y              = 61529
KEYBOARD_RETURN         = 61453
KEYBOARD_ESC            = 61467
CLICK_A = ( ACTION_A, PAD_A, KEYBOARD_A, KEYBOARD_RETURN, )
CLICK_B = ( ACTION_B, PAD_B, KEYBOARD_B, )
CLICK_X = ( ACTION_X, PAD_X, KEYBOARD_X, ACTION_REMOTE_STOP, )
CLICK_Y = ( ACTION_Y, PAD_Y, KEYBOARD_Y, )
EXIT_CODES = (9, 10, 216, 257, 275, 216, 61506, 61467,)

def log(text):
    try:
        xbmc.output(text)
    except: pass

#################################################################################################################
class TextBoxDialogXML( xbmcgui.WindowXML ):
	""" Create a skinned textbox window """

	XML_FILENAME = "DialogScriptInfo.xml"
	
	def __init__( self, *args, **kwargs):
		pass
		
	def onInit( self ):
		log( "TextBoxDialogXML.onInit()" )
		try:
			self.getControl( 3 ).setLabel( self.title )
		except: pass
		self.getControl( 5 ).setText( self.text )

	def onClick( self, controlId ):
		pass

	def onFocus( self, controlId ):
		pass

	def onAction( self, action ):
		try:
			buttonCode =  action.getButtonCode()
			actionID   =  action.getId()
			if not actionID:
				actionID = buttonCode
		except: return
		if actionID in EXIT_CODES or buttonCode in EXIT_CODES:
			self.close()

	def ask(self, title="", text="", fn=None ):
		log("TextBoxDialogXML.ask()")
		if not title and fn:
			self.title = fn
		else:
			self.title = title
		if fn:
			try:
				self.text = file(xbmc.translatePath(fn)).read()
			except:
				self.text = "Failed to load file: %s" % fn
		else:
			self.text = text

		self.doModal()		# causes window to be drawn
