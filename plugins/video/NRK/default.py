"""
    Plugin for viewing content from nrk.no
"""


#main imports
import os
import sys
import xbmc
from NRK_API.utils import PluginError, PluginScriptError
   
   
#plugin constants
__plugin__         = "NRK"
__author__         = "VictorV"
__version__        = "0.9.1"
__XBMC_Revision__  = "21735"


def _check_compatible():
    #spam plugin statistics to log
    msg = "PLUGIN::INIT -> '%s: version %s'" % (__plugin__, __version__,)
    xbmc.log(msg, xbmc.LOGNOTICE) 
    
    try:
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ] )
        #compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )  
    except:
        #error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
        
    #spam revision info
    xbmc.log( "PLUGIN::COMPABILITY -> Required XBMC Revision: r%s" % (
                 __XBMC_Revision__), 
                 xbmc.LOGNOTICE )
    xbmc.log( "PLUGIN::COMPABILITY -> Found XBMC Revision: r%d [%s]" % ( 
                 xbmc_rev, ("Not Compatible", "Compatible", "Unknown")[ok]), 
                 xbmc.LOGNOTICE )
                 
    #if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        xbmcgui.Dialog().ok( "%s - %s: %s" % (
                 __plugin__, xbmc.getLocalizedString( 30700 ), __version__), 
                 xbmc.getLocalizedString( 30701 ) % (__plugin__),
                 xbmc.getLocalizedString( 30702 ) % (__XBMC_Revision__),
                 xbmc.getLocalizedString( 30703 ) )
                 
    #return result
    return ok



if (__name__ == "__main__"):

    if (not sys.argv[2]):
        ok = _check_compatible()
        if (ok):
            from NRK_API import xbmcplugin_rootmenu as plugin
            
    else:
        if sys.argv[2][1:].startswith('program'):
            from NRK_API import xbmcplugin_program as plugin
            
        elif sys.argv[2][1:].startswith('nrkbeta'):
            from NRK_API import xbmcplugin_nrk_beta_feeds as plugin
            
        elif sys.argv[2][1:].startswith('webradio'):
            from NRK_API import xbmcplugin_webradio as plugin
            
        elif sys.argv[2][1:].startswith('podcast'):
            from NRK_API import xbmcplugin_podcast as plugin
            
        elif sys.argv[2][1:].startswith('text'):
            from NRK_API import xbmcplugin_text as plugin
            
        elif sys.argv[2][1:].startswith('teletext'):
            from NRK_API import xbmcplugin_teletext as plugin
    
        elif sys.argv[2][1:].startswith('kanalene'):
            from NRK_API import chlive as plugin
        
        elif sys.argv[2][1:].startswith('favorites'):
            from NRK_API import favorites as plugin
      
        elif sys.argv[2][1:].startswith('nogui'):
            from NRK_API import nogui as plugin
    try:
        plugin.Main()
    except PluginError:
        print 'Plugin encountered a error retreiving virtual directory'
    
    #Use plugin error class for unknown errors
    except:
        #need a try/except clause to avoid xbmc error dialog
        try:
            raise PluginScriptError
        except: 
            print 'Plugin encountered a error retreiving virtual directory'

        
        
        
        
        
