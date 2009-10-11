import sys
import xbmc
import runscript

# Script constants
scriptname = sys.modules['runscript'].__scriptname__
version = sys.modules['runscript'].__version__

print '[PLUGIN][%s] version %s initialized!' % (scriptname, version)

if (__name__ == '__main__'):
    if sys.argv[0].startswith('plugin://'):
        foldername = sys.argv[0].split('/')[-2] #check in case user renamed folder
        scriptPath = '/'.join(['special://home/plugins/pictures', foldername, 'runscript.py'])
        xbmc.executebuiltin('RunScript(%s,-runscript)' % (scriptPath))

sys.modules.clear()