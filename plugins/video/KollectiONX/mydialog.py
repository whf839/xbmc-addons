# -- coding: cp1252 -*-

import os
import sys
from traceback import print_exc

import xbmc
import xbmcgui
import xbmcplugin

CWD = os.getcwd().rstrip( ";" )

SPECIAL_PROFILE_DIR = xbmc.translatePath( "special://profile/" )
GET_LOCALIZED_STRING = xbmc.Language( CWD ).getLocalizedString

ACTION_PREVIOUS_MENU = 10


class MainGui( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        self.genre_list = kwargs['genre_list']
        
 
    def onInit(self):
      self.title = self.getControl(210)
      self.title.setLabel( GET_LOCALIZED_STRING( 32000 ) )
      #On identifie la liste par son id
      self.xml_list = self.getControl(200)
      
      #Création du dictionnaire
      #self.liste_equipe = self.genre_list
      #if self.liste_equipe == []:self.liste_equipe = [ {'sport': GET_LOCALIZED_STRING( 32100 ), 'A_name': '', 'B_name': ''} ]
      self.list_items= []
      ignore_list=xbmcplugin.getSetting('genreignore').split(",")
      for row in self.genre_list[0]:
          if str(row['genreid']) in ignore_list:
              sel = 'true'
          else:
              sel = 'false'

          self.list_items.append({'displayname': "%s (%d movies)" % (row['displayname'], row['moviecount']),
                                    'genreid': row['genreid'],
                                    "selection": sel})


      #for equipe in self.liste_equipe :
      #    equipe['selection'] = 'false'
      self.listItems(self.list_items)
      
      
      ######PLACE LE CODE A EXECUTER AU DEMARRAGE ICI
        
        
    ######PLACE TES DEF ICI

    
      
    def listItems(self, items):
      self.xml_list.reset()  
      for item in items:
            #On crée un element de liste, avec son label
            listitem = xbmcgui.ListItem(item['displayname'])
            #On définit la variable clicked de l'élément liste
            listitem.setProperty( "clicked", item['selection'] )
            #On injecte l'élément liste à la liste xml
            self.xml_list.addItem( listitem )

            
    # Cette def permet de gérer les actions en fonctions de la touche du clavier pressée
    def onAction(self, action):
        #Close the script
        if action == ACTION_PREVIOUS_MENU :
            self.close()

    def onClick(self, controlID):
        """
            Notice: onClick not onControl
            Notice: it gives the ID of the control not the control object
        """
        #action sur la liste
        print "Control %d clicked" % controlID
        if controlID == 200 :
            print "Processing control 200"
            #Renvoie le numéro de l'item sélectionné
            num = self.xml_list.getSelectedPosition()
            print "got xml list"
            #Traitement de l'information
            if self.list_items[num]['selection'] == "false" :
                self.list_items[num]['selection'] = "true"
            else :
                self.list_items[num]['selection'] = "false"

            print "updating list"
            self.listItems(self.list_items)
            print "list updated"
            self.xml_list.selectItem(num)
            print "done processing 200"
            
        if controlID == 9001 :
            print "processing 9001"
            matchfilter=[]
            for item in self.list_items:
                if item['selection'] == "true" :
                    matchfilter.append(str(item['genreid']))

            xbmcplugin.setSetting('genreignore', ",".join(matchfilter))
            self.close()
            print "done with 9001"
        print "done with control"
        
  
    def onFocus(self, controlID):
        pass


def getUserSkin():
    current_skin = xbmc.getSkinDir()
    force_fallback = os.path.exists( os.path.join( CWD, "resources", "skins", current_skin ) )
    if not force_fallback: current_skin = "DefaultSkin"
    return current_skin, force_fallback


def MyDialog(g_list):
    print "In mydialog"
    genre_list = g_list
    current_skin, force_fallback = getUserSkin()
    w = MainGui("MyDialog.xml",
         CWD,
         current_skin,
         force_fallback,
         genre_list=g_list)
    w.doModal()
    del w


def test():
    MyDialog()
