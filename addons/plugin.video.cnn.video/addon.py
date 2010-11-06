## Plugin for streaming video content from CNN

# main imports
import sys


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] or "category=" in sys.argv[ 2 ] ):
        import resources.lib.categories as plugin
        plugin.Main()
    else:
        import resources.lib.videos as plugin
        plugin.Main()
