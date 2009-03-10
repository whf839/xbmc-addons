import xbmcplugin
import xbmc
import xbmcgui
import urllib
import urllib2
import sys
import os


"""
    PARSE ARGV
"""

class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )

exec "args = _Info(%s)" % (urllib.unquote_plus(sys.argv[2][1:].replace("&", ", ").replace('"','\'')) , )



"""
    DEFINE URLS
"""
ALL_RECENT_URL   = "http://www.cbs.com/sitefeeds/all/recent.js"
ALL_POPULAR_URL  = "http://www.cbs.com/sitefeeds/all/popular.js"
ALL_SHOWS_URL    = "http://www.cbs.com/video/"
HDVIDEOS_URL     = "http://www.cbs.com/sitefeeds/hd/hd.js"
SITEFEED_URL     = "http://www.cbs.com/sitefeeds"

imagepath   = os.path.join(os.getcwd().replace(';', ''),'resources','images')
cachepath   = os.path.join(os.getcwd().replace(';', ''),'resources','cache')


"""
    GET SETTINGS
"""

settings={}
#settings general
#ADD SETTINGS



"""
    Clean Non-Ascii characters from names for XBMC
"""

def cleanNames(string):
    try:
        string = string.replace("'","").replace(unicode(u'\u201c'), '"').replace(unicode(u'\u201d'), '"').replace(unicode(u'\u2019'),'\'').replace('&amp;','&').replace('&quot;','"')
        return string
    except:
        return string

"""
    ADD DIRECTORY
"""

def addDirectory(name, url='', mode='default', thumb='', icon='', plot=''):
    ok=True
    u = sys.argv[0]+'?url="'+urllib.quote_plus(url)+'"&mode="'+mode+'"&name="'+urllib.quote_plus(cleanNames(name))+'"&plot="'+urllib.quote_plus(cleanNames(plot))+'"&thumbnail="'+urllib.quote_plus(cleanNames(thumb))+'"'
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo( type="Video",
                 infoLabels={ "Title":name,
                              "Plot":cleanNames(plot)
                            })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


def getHTML( url ):
    try:
        print 'CBS --> common :: getHTML :: url = '+url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except urllib2.URLError, e:
        print 'Error code: ', e.code
        return False
    else:
        return link
    



