"""
 Shared global values for Plugin
 """
import os, sys

HOME_DIR = os.getcwd()
TEMP_DIR = "special://temp"
__plugin__ = sys.modules[ "__main__" ].__plugin__

BASE_CACHE_PATH = "/".join( [ "special://profile", "Thumbnails", "Pictures" ] )
ITEMS_FILENAME = "/".join( [TEMP_DIR, __plugin__+"_items_%s.dat"] )
