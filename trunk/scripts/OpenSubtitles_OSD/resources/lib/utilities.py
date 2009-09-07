import sys
import os
import xbmc
#import xbmcgui
#import md5
#import time
#import array
#import httplib
#import xml.dom.minidom
import struct
DEBUG_MODE = 10

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__ = sys.modules[ "__main__" ].__version__

# comapatble versions
SETTINGS_VERSIONS = ( "1.0", )
# base paths
BASE_DATA_PATH = os.path.join( "special://temp", "script_data", __scriptname__ )
BASE_SETTINGS_PATH = os.path.join( "special://profile", "script_data", __scriptname__ )

BASE_RESOURCE_PATH = sys.modules[ "__main__" ].BASE_RESOURCE_PATH
# special action codes
SELECT_ITEM = ( 11, 256, 61453, )
EXIT_SCRIPT = ( 6, 10, 247, 275, 61467, 216, 257, 61448, )
CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, )
GET_EXCEPTION = ( 216, 260, 61448, )
SELECT_BUTTON = ( 229, 259, 261, 61453, )
MOVEMENT_UP = ( 166, 270, 61478, )
MOVEMENT_DOWN = ( 167, 271, 61480, )
# Log status codes
LOG_INFO, LOG_ERROR, LOG_NOTICE, LOG_DEBUG = range( 1, 5 )

def _create_base_paths():
    """ creates the base folders """
    ##if ( not os.path.isdir( BASE_DATA_PATH ) ):
    ##    os.makedirs( BASE_DATA_PATH )
    ##if ( not os.path.isdir( BASE_SETTINGS_PATH ) ):
    ##    os.makedirs( BASE_SETTINGS_PATH )
_create_base_paths()



def LOG( status, format, *args ):
    if ( DEBUG_MODE >= status ):
        xbmc.output( "%s: %s\n" % ( ( "INFO", "ERROR", "NOTICE", "DEBUG", )[ status - 1 ], format % args, ) )

def hashFile(name): 
      try: 
                 
                longlongformat = 'q'  # long long 
                bytesize = struct.calcsize(longlongformat) 
                    
                f = open(name, "rb") 
                    
                filesize = os.path.getsize(name) 
                hash = filesize 
                    
                if filesize < 65536 * 2: 
                       return "SizeError" 
                 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
    
                f.seek(max(0,filesize-65536),0) 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
                f.close() 
                returnedhash =  "%016x" % hash 
                return returnedhash 
    
      except(IOError): 
                return "IOError"





def dec2hex(n, l=0):
    # return the hexadecimal string representation of integer n
    s = "%X" % n
    if (l > 0) :
        while len(s) < l:
            s = "0" + s 
    return s

#
# Hexadecimal => integer
#
def hex2dec(s):
    # return the integer value of a hexadecimal string s
    return int(s, 16)

#
# String => Integer
#
def toInteger (string):
    try:
        return int( string )
    except :
        return 0

#
# Detect movie title and year from file name...
#
def getMovieTitleAndYear( filename ):
    name = os.path.splitext( filename )[0]

    cutoffs = ['dvdrip', 'dvdscr', 'cam', 'r5', 'limited',
               'xvid', 'h264', 'x264', 'h.264', 'x.264',
               'dvd', 'screener', 'unrated', 'repack', 'rerip', 
               'proper', '720p', '1080p', '1080i', 'bluray']

    # Clean file name from all kinds of crap...
    for char in ['[', ']', '_', '(', ')']:
        name = name.replace(char, ' ')
    
    # if there are no spaces, start making beginning from dots...
    if name.find(' ') == -1:
        name = name.replace('.', ' ')
    if name.find(' ') == -1:
        name = name.replace('-', ' ')
    
    # remove extra and duplicate spaces!
    name = name.strip()
    while name.find('  ') != -1:
        name = name.replace('  ', ' ')
        
    # split to parts
    parts = name.split(' ')
    year = 0
    cut_pos = 256
    for part in parts:
        # check for year
        if part.isdigit():
            n = int(part)
            if n>1930 and n<2050:
                year = part
                if parts.index(part) < cut_pos:
                    cut_pos = parts.index(part)
                
        # if length > 3 and whole word in uppers, consider as cutword (most likelly a group name)
        if len(part) > 3 and part.isupper() and part.isalpha():
            if parts.index(part) < cut_pos:
                cut_pos = parts.index(part)
                
        # check for cutoff words
        if part.lower() in cutoffs:
            if parts.index(part) < cut_pos:
                cut_pos = parts.index(part)
        
    # make cut
    name = ' '.join(parts[:cut_pos])
    return name, year



def toOpenSubtitles_two( id ):
        languages = { "None"  		: "none",
                      "Albanian"  	: "sq",
                      "Arabic"  	: "ar",
                      "Belarusian"  	: "hy",
                      "Bosnian"  	: "bs",
                      "Bulgarian"  	: "bg",
                      "Catalan"  	: "ca",
                      "Chinese"  	: "zh",
                      "Croatian" 	: "hr",
                      "Czech"  		: "cs",
                      "Danish" 		: "da",
                      "Dutch" 		: "nl",
                      "English" 	: "en",
                      "Esperanto" 	: "eo",
                      "Estonian" 	: "et",
                      "Farsi" 		: "fo",
                      "Finnish" 	: "fi",
                      "French" 		: "fr",
                      "Galician" 	: "gl",
                      "Georgian" 	: "ka",
                      "German" 		: "de",
                      "Greek" 		: "el",
                      "Hebrew" 		: "he",
                      "Hindi" 		: "hi",
                      "Hungarian" 	: "hu",
                      "Icelandic" 	: "is",
                      "Indonesian" 	: "id",
                      "Italian" 	: "it",
                      "Japanese" 	: "ja",
                      "Kazakh" 		: "kk",
                      "Korean" 		: "ko",
                      "Latvian" 	: "lv",
                      "Lithuanian" 	: "lt",
                      "Luxembourgish" 	: "lb",
                      "Macedonian" 	: "mk",
                      "Malay" 		: "ms",
                      "Norwegian" 	: "no",
                      "Occitan" 	: "oc",
                      "Polish" 		: "pl",
                      "Portuguese" 	: "pt",
                      "PortugueseBrazil" 	: "pb",
                      "Romanian" 	: "ro",
                      "Russian" 	: "ru",
                      "SerbianLatin" 	: "sr",
                      "Serbian" 	: "sr",
                      "Slovak" 		: "sk",
                      "Slovenian" 	: "sl",
                      "Spanish" 	: "es",
                      "Swedish" 	: "sv",
                      "Syriac" 		: "syr",
                      "Thai" 		: "th",
                      "Turkish" 	: "tr",
                      "Ukrainian" 	: "uk",
                      "Urdu" 		: "ur",
                      "Vietnamese" 	: "vi",
		      "English (US)" 	: "en",
		      "All" 		: "all"
                    }
        return languages[ id ]

def toOpenSubtitles_fromtwo( id ):
        languages = {   		 "none" :"None",
                      "Albanian"  	: "sq",
                      "Arabic"  	: "ar",
                      "Belarusian"  	: "hy",
                      "Bosnian"  	: "bs",
                      "Bulgarian"  	: "bg",
                      "Catalan"  	: "ca",
                      "Chinese"  	: "zh",
                      "Croatian" 	: "hr",
                      "Czech"  		: "cs",
                      "Danish" 		: "da",
                      "Dutch" 		: "nl",
                       	 "en":"English",
                      "Esperanto" 	: "eo",
                      "Estonian" 	: "et",
                      "Farsi" 		: "fo",
                      "Finnish" 	: "fi",
                      "French" 		: "fr",
                      "Galician" 	: "gl",
                      "Georgian" 	: "ka",
                      "German" 		: "de",
                      "Greek" 		: "el",
                      "Hebrew" 		: "he",
                      "Hindi" 		: "hi",
                      "Hungarian" 	: "hu",
                      "Icelandic" 	: "is",
                      "Indonesian" 	: "id",
                      "Italian" 	: "it",
                      "Japanese" 	: "ja",
                      "Kazakh" 		: "kk",
                      "Korean" 		: "ko",
                      "Latvian" 	: "lv",
                      "Lithuanian" 	: "lt",
                      "Luxembourgish" 	: "lb",
                      "Macedonian" 	: "mk",
                      "Malay" 		: "ms",
                      "Norwegian" 	: "no",
                      "Occitan" 	: "oc",
                      "Polish" 		: "pl",
                      "Portuguese" 	: "pt",
                      "PortugueseBrazil" 	: "pb",
                      "Romanian" 	: "ro",
                      "Russian" 	: "ru",
                       	 "sr":"SerbianLatin",
                       	 "sr":"Serbian",
                      "Slovak" 		: "sk",
                         "sl":"Slovenian",
                      "Spanish" 	: "es",
                      "Swedish" 	: "sv",
                      "Syriac" 		: "syr",
                      "Thai" 		: "th",
                      "Turkish" 	: "tr",
                      "Ukrainian" 	: "uk",
                      "Urdu" 		: "ur",
                      "Vietnamese" 	: "vi",
		      "English (US)" 	: "en",
		      "All" 		: "all"
                    }
        return languages[ id ]

        

def twotoone(id):
  languages = {
    "sq"  :  "29",
    "hy"  :  "0",
    "ar"  :  "12",
    "ay"  :  "0",
    "bs"  :  "10",
    "pb"  :  "48",
    "bg"  :  "33",
    "ca"  :  "53",
    "zh"  :  "17",
    "hr"  :  "38",
    "cs"  :  "7",
    "da"  :  "24",
    "nl"  :  "23",
    "en"  :  "2",
    "et"  :  "20",
    "fi"  :  "31",
    "fr"  :  "8",
    "de"  :  "5",
    "gr"  :  "16",
    "he"  :  "22",
    "hi"  :  "42",
    "hu"  :  "15",
    "is"  :  "6",
    "it"  :  "9",
    "ja"  :  "11",
    "kk"  :  "0",
    "ko"  :  "4",
    "lv"  :  "21",
    "mk"  :  "35",
    "nn"  :  "3",
    "pl"  :  "26",
    "pt"  :  "32",
    "ro"  :  "13",
    "ru"  :  "27",
    "sr"  :  "36",
    "sk"  :  "37",
    "sl"  :  "1",
    "es"  :  "28",
    "sv"  :  "25",
    "th"  :  "44",
    "tr"  :  "30",
    "uk"  :  "46",
    "vi"  :  "51"
  }
  return languages[ id ]
        

def toOpenSubtitlesId( id ):
        languages = { "None"  		: "none",
                      "Albanian"  	: "alb",
                      "Arabic"  	: "ara",
                      "Belarusian"  : "arm",
                      "Bosnian"  	: "bos",
                      "Bulgarian"  	: "bul",
                      "Catalan"  	: "cat",
                      "Chinese"  	: "chi",
                      "Croatian" 	: "hrv",
                      "Czech"  		: "cze",
                      "Danish" 		: "dan",
                      "Dutch" 		: "dut",
                      "English" 	: "eng",
                      "Esperanto" 	: "epo",
                      "Estonian" 	: "est",
                      "Farsi" 		: "per",
                      "Finnish" 	: "fin",
                      "French" 		: "fre",
                      "Galician" 	: "glg",
                      "Georgian" 	: "geo",
                      "German" 		: "ger",
                      "Greek" 		: "ell",
                      "Hebrew" 		: "heb",
                      "Hindi" 		: "hin",
                      "Hungarian" 	: "hun",
                      "Icelandic" 	: "ice",
                      "Indonesian" 	: "ind",
                      "Italian" 	: "ita",
                      "Japanese" 	: "jpn",
                      "Kazakh" 		: "kaz",
                      "Korean" 		: "kor",
                      "Latvian" 	: "lav",
                      "Lithuanian" 	: "lit",
                      "Luxembourgish" 	: "ltz",
                      "Macedonian" 	: "mac",
                      "Malay" 		: "may",
                      "Norwegian" 	: "nor",
                      "Occitan" 	: "oci",
                      "Polish" 		: "pol",
                      "Portuguese" 	: "por",
                      "PortugueseBrazil" 	: "pob",
                      "Romanian" 	: "rum",
                      "Russian" 	: "rus",
                      "SerbianLatin" 	: "scc",
                      "Serbian" 	: "scc",
                      "Slovak" 		: "slo",
                      "Slovenian" 	: "slv",
                      "Spanish" 	: "spa",
                      "Swedish" 	: "swe",
                      "Syriac" 		: "syr",
                      "Thai" 		: "tha",
                      "Turkish" 	: "tur",
                      "Ukrainian" 	: "ukr",
                      "Urdu" 		: "urd",
                      "Vietnamese" 	: "vie",
		      "English (US)" 	: "eng",
		      "All" 		: "all"
                    }
        return languages[ id ]


def toScriptLang(id):
    languages = { 
                  "0" : "Albanian",
                  "1" : "Arabic",
                  "2" : "Belarusian",
                  "3" : "BosnianLatin",
                  "4" : "Bulgarian",
                  "5" : "Catalan",
                  "6" : "Chinese",
                  "7" : "Croatian",
                  "8" : "Czech",
                  "9" : "Danish",
                  "10" : "Dutch",
                  "11" : "English",
                  "12" : "Estonian",
                  "13" : "Finnish",
                  "14" : "French",
                  "15" : "German",
                  "16" : "Greek",
                  "17" : "Hebrew",
                  "18" : "Hindi",
                  "19" : "Hungarian",
                  "20" : "Icelandic",
                  "21" : "Indonesian",
                  "22" : "Italian",
                  "23" : "Japanese",
                  "24" : "Korean",
                  "25" : "Latvian",
                  "26" : "Lithuanian",
                  "27" : "Macedonian",
                  "28" : "Norwegian",
                  "29" : "Polish",
                  "30" : "Portuguese",
                  "31" : "PortugueseBrazil",
                  "32" : "Romanian",
                  "33" : "Russian",
                  "34" : "SerbianLatin",
                  "35" : "Slovak",
                  "36" : "Slovenian",
                  "37" : "Spanish",
                  "38" : "Swedish",
                  "39" : "Thai",
                  "40" : "Turkish",
                  "41" : "Ukrainian",
                  "42" : "Vietnamese",
                }
    return languages[ id ]       
        
        
        
def latin1_to_ascii (unicrap):

	xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
    	0xc6:'Ae', 0xc7:'C',
    	0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
    	0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
    	0xd0:'Th', 0xd1:'N',
    	0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
    	0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
    	0xdd:'Y', 0xde:'th', 0xdf:'ss',
    	0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
    	0xe6:'ae', 0xe7:'c',
    	0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
    	0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
    	0xf0:'th', 0xf1:'n',
    	0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
    	0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
    	0xfd:'y', 0xfe:'th', 0xff:'y',
    	0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
    	0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
    	0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
    	0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
    	0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
    	0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
    	0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
    	0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
    	0xd7:'*', 0xf7:'/'
    	}

	r = ''
	for i in unicrap:
		if xlate.has_key(ord(i)):
			r += xlate[ord(i)]
		elif ord(i) >= 0x80:
			pass
		else:
			r += i
	return r        