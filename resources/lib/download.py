import urllib, urllib2, os, traceback, sys, socket
import xbmcgui

socket.setdefaulttimeout(30)

class _urlopener( urllib.URLopener ):
    version =  "QuickTime/7.6.5 (qtver=7.6.5;os=Windows NT 5.1Service Pack 3)"

urllib._urlopener = _urlopener()

def download( url_path, download_path, file_tag = "" ):
    ''' retrieves files from url_path to download_path.
        pulls filename from url_path
        requirements:
            url_path - where to download from
            download_path - where to save file
        optional:
            file_tag - add a tag to the filename, ie "-trailer"
    '''
    try:
        try:
            url_path = url_path.split("|")[0]
        except:
            url_path = url_path
        if file_tag:
            filename, ext = os.path.splitext( os.path.basename( url_path.replace( "?","" ) ) )
            filename = filename + file_tag + ext
        else:
            filename = os.path.basename( url_path.replace( "?","" ) )
        destination = os.path.join( download_path, filename ).replace( "\\\\", "\\" )
        urllib.urlretrieve( url_path, destination, _report_hook )
        success = True
    except:
        traceback.print_exc()
        destination = ""
        success = False
    return success, destination
        
def _report_hook( count, blocksize, totalsize ):
    percent = int( float( count * blocksize * 100) / totalsize )
    try:
        xbmcgui.DialogProgress().update( percent )
    except:
        # DialogProgress must not be open
        pass