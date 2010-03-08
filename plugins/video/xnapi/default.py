##############################################################################
#
# xnapi - XBMC video plugin
# http://www.napiprojekt.pl/
#
# Version 0.1 
# 
# Coding by gregd
# http://greg.pro
# License: GPL v2
#
# Credits:
#   * Team XBMC @ XBMC.org                                      [http://xbmc.org/]
#   * Dan Dar3                                                  [http://dandar3.blogspot.com]  
#   * gim,krzynio,dosiu,hash                                    [http://hacking.apcoh.com/]
#   * Igor Pavlov                                               [http://www.7-zip.org]
#   * multiplatform compatibility by pajretX
# 
# Constants
#
__plugin__  = "xnapi"
__author__  = "gregd"
__url__     = "http://greg.pro/xnapi"
__date__    = "08 September 2009"
__version__ = "0.1"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

if ( "action=search" in sys.argv[ 2 ] ):
    import xnapi_search as plugin
    plugin.Main()    
else:
    import xnapi_main as plugin
    plugin.Main()
