"""
    This plugin streams video from NZBs and a fast Usenet account.
    NZBs can be retrieved from Usenet searches or from RSS feeds.
    The frontend of this plugin is adapted from switch's SABnzbd+ plugin.
    I replaced the backend with in-process nntplib for better status callbacks.
"""

# main imports
import sys

# plugin constants
__plugin__ = "NZB Streamer"
__author__ = "Frontend: switch; Backend: Matt Chambers"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://code.google.com/p/xbmc-addons/source/browse/trunk#trunk/plugins/video/NZB Streamer"
__credits__ = "Team XBMC"
__version__ = "0.1"


if ( __name__ == "__main__" ):
    print 'arguments:%s' % sys.argv[1:]
    from nzb import item_list as plugin
    plugin.Main()
