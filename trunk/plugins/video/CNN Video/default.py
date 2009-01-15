"""
    Plugin for streaming content from CNN
"""

# main imports
import sys
import os

# plugin constants
__plugin__ = "CNN Video"
__author__ = "nuka1195"
__credits__ = "Team XBMC"
__version__ = "1.0"

# base urls
BASE_URL = "http://www.cnn.com/"

# base paths
BASE_PATH = os.getcwd().replace( ";", "" )


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        from cnnAPI import xbmcplugin_categories as plugin
    else:
        from cnnAPI import xbmcplugin_videos as plugin
    plugin.Main()
