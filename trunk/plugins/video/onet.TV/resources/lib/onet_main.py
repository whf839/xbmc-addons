#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
	def __init__( self ):
        # Constants
#		IMAGES_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )        
        
        #
        # Wiadomości
        #
		listitem = xbmcgui.ListItem( "Wiadomości", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?wiado&po_co=%s' % ( sys.argv[ 0 ], "Wiadomości" ), listitem=listitem, isFolder=True)		
        #
        # Religia
        #
		listitem = xbmcgui.ListItem( "Religia", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?rel&po_co=%s' % ( sys.argv[ 0 ], "Religia" ), listitem=listitem, isFolder=True)
		
        #		
        # Rozrywka
        #
		listitem = xbmcgui.ListItem( "Rozrywka", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?rozr&po_co=%s' % ( sys.argv[ 0 ], "Rozrywka" ), listitem=listitem, isFolder=True)

        #
        # Film
        #
		listitem = xbmcgui.ListItem( "Film", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?film&po_co=%s' % ( sys.argv[ 0 ], "Film" ), listitem=listitem, isFolder=True)

        #
        # Gry
        #
		listitem = xbmcgui.ListItem( "Gry", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?gry&po_co=%s' % ( sys.argv[ 0 ], "Gry" ), listitem=listitem, isFolder=True)

        #
        # Biznes
        #
		listitem = xbmcgui.ListItem( "Biznes", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?biz&po_co=%s' % ( sys.argv[ 0 ], "Biznes" ), listitem=listitem, isFolder=True)
        
        #
        # Gotowanie
        #
		listitem = xbmcgui.ListItem( "Gotowanie", iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?got&po_co=%s' % ( sys.argv[ 0 ], "Gotowanie" ), listitem=listitem, isFolder=True)

        #
        # Plajada talentów
        #
		listitem = xbmcgui.ListItem( "Plejada talentów", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?plej&po_co=%s' % ( sys.argv[ 0 ], "Plejada Talentów" ), listitem=listitem, isFolder=True)
        
        #
        #  Sport
        #
		listitem = xbmcgui.ListItem( "Sport", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?sport&po_co=%s' % ( sys.argv[ 0 ], "Sport" ), listitem=listitem, isFolder=True)

        #
        #  Styl życia
        #
		listitem = xbmcgui.ListItem( "Styl życia", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?styl&po_co=%s' % ( sys.argv[ 0 ], "Styl życia" ), listitem=listitem, isFolder=True)

        #
        #  Muzyka
        #
		listitem = xbmcgui.ListItem( "Muzyka", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?muz&po_co=%s' % ( sys.argv[ 0 ], "Muzyka" ), listitem=listitem, isFolder=True)

        #
        #  Podróże
        #
		listitem = xbmcgui.ListItem( "Podróże", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?pod&po_co=%s' % ( sys.argv[ 0 ], "Podróże" ), listitem=listitem, isFolder=True)

        #
        #  Edukacja
        #
		listitem = xbmcgui.ListItem( "Edukacja", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?edu&po_co=%s' % ( sys.argv[ 0 ], "Edukacja" ), listitem=listitem, isFolder=True)

        #
        #  Moto
        #
		listitem = xbmcgui.ListItem( "Moto", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?moto&po_co=%s' % ( sys.argv[ 0 ], "Moto" ), listitem=listitem, isFolder=True)

        #
        #  Świat dziecka
        #
		listitem = xbmcgui.ListItem( "Świat dziecka", iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?swiat&po_co=%s' % ( sys.argv[ 0 ], "Świat dziecka" ), listitem=listitem, isFolder=True)

        # Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
