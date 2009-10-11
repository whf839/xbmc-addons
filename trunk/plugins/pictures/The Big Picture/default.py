import sys
import xbmc

# Script constants
__scriptname__ = 'The Big Picture'
__author__ = 'rwparris2'
__url__ = 'http://code.google.com/p/xbmc-addons/'
__credits__ = 'Team XBMC'
__version__ = '1.1.2'

if (__name__ == '__main__'):
    if sys.argv[0].startswith('plugin://') and sys.argv[1] != '-runscript':
        print '[PLUGIN][%s] version %s initialized!' % (__scriptname__, __version__)

        foldername = sys.argv[0].split('/')[-2] #check in case user renamed folder
        scriptPath = '/'.join(['special://home/plugins/pictures', foldername, 'runscript.py'])
        xbmc.executebuiltin('RunScript(%s,-runscript)' % (scriptPath))

        sys.modules.clear()