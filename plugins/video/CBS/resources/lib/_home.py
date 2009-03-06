import xbmc
import xbmcplugin
from xbmcgui import Dialog

import common
import os
import sys

class Main:
    def __init__( self ):
        self.addMainHomeItems()
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )

   
    def addMainHomeItems( self ):
        common.addDirectory("1. Latest Videos",
                            common.ALL_RECENT_URL,
                            "Latest",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "Latest Videos Added to CBS.com")
        common.addDirectory("2. Most Popular",
                            common.ALL_POPULAR_URL,
                            "Popular",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "Most Popular Episodes and Clips from CBS.com")
        common.addDirectory("3. All Shows",
                            common.ALL_SHOWS_URL,
                            "Shows",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("4. Primetime",
                            common.ALL_SHOWS_URL,
                            "ShowsPrimetime",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("5. Daytime",
                            common.ALL_SHOWS_URL,
                            "ShowsDaytime",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("6. Late Night",
                            common.ALL_SHOWS_URL,
                            "ShowsLate",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("7. TV Classics",
                            common.ALL_SHOWS_URL,
                            "ShowsClassics",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("8. Specials",
                            common.ALL_SHOWS_URL,
                            "ShowsSpecials",
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),
                            plot = "")
        common.addDirectory("9. HD Episodes",
                            common.HDVIDEOS_URL,
                            "HD",
                            xbmc.translatePath(os.path.join(common.imagepath,"hd_icon.png")),
                            xbmc.translatePath(os.path.join(common.imagepath,"hd_icon.png")),
                            plot = "")
