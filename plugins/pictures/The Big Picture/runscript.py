import os
import sys
import default

# Script constants
__scriptname__ = sys.modules['default'].__scriptname__
__version__ = sys.modules['default'].__version__

print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)

if (__name__ == '__main__'):
    if sys.argv[1] == '-runscript':
        import resources.lib.gui as gui

        ui = gui.GUI( 'main.xml', os.getcwd(), 'default' )
        ui.doModal()
        del ui

        sys.modules.clear()
