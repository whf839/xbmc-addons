#############################################################################
#
# Navi-X Playlist browser
# by rodejo (rodejo16@gmail.com)
#############################################################################

#############################################################################
#
# CDownloader:
# This class handles user login to the Navi-Xtreme website.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import os
from libs2 import *
from settings import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

LABEL_USRNAME = 141
LABEL_PASSWORD = 142
BUTTON_USRNAME = 143
BUTTON_PASSWORD = 144
BUTTON_LOGIN = 145
BUTTON_CANCEL = 146

class CDialogLogin(xbmcgui.WindowXMLDialog): 
    def __init__(self, strXMLname, strFallbackPath):#, strDefaultName, forceFallback):
        self.setCoordinateResolution(PAL_4x3)

        #user background image
#        self.bg = xbmcgui.ControlImage(100,100,520,376, imageDir + "background_txt.png")
#        self.addControl(self.bg)

        #read user ID from file
        self.username = ''
        self.password = ''
        self.state = 0 #success

    def onInit( self ):        
        control=self.getControl(BUTTON_USRNAME)
        self.setFocus(control)       

    def onAction(self, action):
        #select item is handled via other onClick().
        if not action.getId() == ACTION_SELECT_ITEM:
            self.onAction1(action)

    def onAction1(self, action):
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_PARENT_DIR):
            self.state = -1
            self.close()
        
        if action == ACTION_SELECT_ITEM:         
            if self.getFocus() == self.getControl(BUTTON_USRNAME):
                keyboard = xbmc.Keyboard(self.username)
                keyboard.doModal()
                
                if (keyboard.isConfirmed() == True):
                    self.username = keyboard.getText()    
                    control = self.getControl(BUTTON_USRNAME)    
                    control.setLabel(self.username)            
            elif self.getFocus() == self.getControl(BUTTON_PASSWORD):
                keyboard = xbmc.Keyboard(self.password)
                keyboard.doModal()
                
                if (keyboard.isConfirmed() == True):
                    self.password = keyboard.getText()    
                    control = self.getControl(BUTTON_PASSWORD)    
                    control.setLabel(self.password)                
            elif self.getFocus() == self.getControl(BUTTON_LOGIN):
                self.state = 0
                self.close()
            elif self.getFocus() == self.getControl(BUTTON_CANCEL):
                self.state = -1
                self.close()

    def onFocus( self, controlId ):
        pass
            
    def onClick( self, controlId ):
        if controlId == BUTTON_CANCEL:          
            self.onAction1(ACTION_PREVIOUS_MENU)
        else:
            self.onAction1(ACTION_SELECT_ITEM)   
        pass
   
    def onControl(self, control):
        #self.setFocus(control)
        pass
          
        
    #end of class    
        