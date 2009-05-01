"""
    TED Talks
        by rwparris2
        http://ted.com
"""
__script__ = "TED Talks"
__version__ = "1.6"

#for a clear log:
print '\n'*5,'Start %s Plugin, version %s' %(__script__, __version__)

#main imports
import xbmcplugin
import sys

__plugin__ = "TED Talks"
__author__ = "rwparris2"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/TED%20Talks"
__version__ = "1.5.2"


if ( __name__ == "__main__" ):
    if (sys.argv[2].startswith('?downloadTalk')):
         import resources.lib.download as download
         download.Main()
    else:
        import resources.lib.ted_talks as ted_talks
        ted_talks.Main()
sys.modules.clear()
