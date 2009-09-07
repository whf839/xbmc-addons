#from xmlrpclib import Server,Transport
#from httplib import HTTP
import locale
import os
#from urlparse import urlparse
from types import UnicodeType
#import re
#import struct
#import base64
#import pickle
##import imdb
#import urllib

#TESTS
defaultavi = "" 
disable_osdb = True
debugmode = True
use_threads = True
check_update = True
doing_login = False

#CONFIGS
videos_ext = ["avi","mpg","mpeg","wmv","divx","mkv","ogm","asf", "mov", "rm", "vob", "dv", "3ivx"]
subs_ext = ["srt","sub","txt","ssa","tmp"]
videos_wildcards = "All videos|*.avi;*.mpg;*.mpeg;*.wmv;*.asf;*.divx;*.mov;*.m2p;*.moov;*.omf;*.qt;*.rm;*.vob;*.dat;*.dv;*.3ivx;*.mkv;*.ogm|ALL files (*.*)|*.*"
    
##LOCAL_ENCODING = locale.getpreferredencoding(do_setlocale=False);
##if not LOCAL_ENCODING or LOCAL_ENCODING == "ANSI_X3.4-1968":
LOCAL_ENCODING = 'latin1'

version = ""
date_released = ""


update_address = ""


preferences_list = {}
sublanguages = {}
update_list = {}

##imdbserver = imdb.IMDb()

#GLOBAL NEEDED(don't change)
cookiefile = "conf/.cookie"
sourcefolder = ""
app_parameteres = ""

param_function = ""
param_files = []


osdb_token = ""
logged_as = ""
user_has_uploaded = False
xmlrpc_server = ""
proxy_address = None
text_log = False

subdownloader_pointer = None



def CleanString(s):
    garbage = ['_',' ','.',',','(',')']
    for char in garbage:
	s = s.replace(char,'')
    return s

def CleanTagsFile(texto):
    p = re.compile( '<.*?>')
    return p.sub('',texto)

def DeleteExtension(file):
    lastpointposition = file.rfind(".")
    return file[:lastpointposition]
		
def GetFpsAndTimeMs(path):
    fps = ""
    time_ms = ""
    try: 
	    avi_info = parse(path)
	    if avi_info.video[0].fps > 0:
		   fps = avi_info.video[0].fps

	    if avi_info.length > 0:
		    time_ms = avi_info.length * 1000
		    
	    return fps,time_ms 
    except:
	   return fps,time_ms 
	    

    
def Log(message):
    string_message = str(message)
    subdownloader_pointer.log_memory.append(string_message)
        
    if text_log:
	try:
	    for line in subdownloader_pointer.log_memory:
		text_log.AppendText("\n" + line)
	except:
	    pass
	
	subdownloader_pointer.log_memory = []
    
    




def EncodeLocale(phrase):
    #if not isinstance(phrase, UnicodeType):
    phrase = unicode(phrase.encode("iso-8859-1"),errors='ignore')
    return phrase


    
