"""

    Programs/Plugin to check for SVN Repo updates of your installed scripts and Plugins

    This version as part of "SVN Repo installer" Programs/Plugin

    Written by BigBellyBilly
    Contact me at BigBellyBilly at gmail dot com - Bugs reports and suggestions welcome.

""" 

import sys, os
import os.path
import xbmc, xbmcgui, xbmcplugin
import urllib, urlparse
import re
import traceback
from string import find
#from pprint import pprint

# Script constants
__plugin__ = "xbmcplugin_update"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '01-04-2009'
xbmc.output( "[PLUGIN]: %s Dated: %s started!" % (__plugin__, __date__))

def log(msg):
    try:
        xbmc.output("[%s]: %s" % (__plugin__, msg))
    except: pass

# check if build is special:// aware - set roots paths accordingly
XBMC_HOME = 'special://home'
if not os.path.isdir(xbmc.translatePath(XBMC_HOME)):    # if fails to convert to Q:, old builds
    XBMC_HOME = 'Q:'
log("XBMC_HOME=%s" % XBMC_HOME)


#############################################################################################################
class Main:

    URL_BASE_SVN_SCRIPTING = "http://xbmc-scripting.googlecode.com/svn"
    URL_BASE_SVN_ADDONS = "http://xbmc-addons.googlecode.com/svn"

    def __init__( self ):
        log("__init__()")
        ok = False

        #SVN_BASE_LIST = (self.URL_BASE_SVN_ADDONS, self.URL_BASE_SVN_SCRIPTING)
        self.SVN_URL_LIST = [ "xbmc-addons", "xbmc-scripting" ]
        #for base_url in SVN_BASE_LIST:
        #    self.SVN_URL_LIST.append( "/".join( [base_url, "trunk"] ) )  

        #['plugin://programs/SVN Repo Installer/', '-1', '?download_url="%2Ftrunk%2Fplugins%2Fmusic/iTunes%2F"&repo=\'xbmc-addons\'&install=""&ioffset=2&voffset=0']
        # create all XBMC script/plugin paths
        paths = ("plugins/programs","plugins/video","plugins/music","plugins/pictures","scripts")
        self.XBMC_PATHS = []
        for p in paths:
            self.XBMC_PATHS.append( xbmc.translatePath( "/".join( [XBMC_HOME, p] ) ) )

        self.dialogProgress = xbmcgui.DialogProgress()
        self.dialogProgress.create(__plugin__)
        self.findInstalled()
        if self.INSTALLED:
            self.checkUpdates() 
        self.dialogProgress.close()

# dev only test dict
#        self.INSTALLED = [ { "filepath": "C:\Program Files\XBMC\plugins\Programs\GoogleReader", "ver": "0.1" , "svn_ver": "0.2", "svn_url": "http://xbmc-addons/svn/trunk/plugins/programs/GoogleReader"},
#                           { "filepath": "C:\Program Files\XBMC\plugins\Video\Reeplay.it", "ver": "0.1" , "svn_ver": "0.2", "svn_url": "http://xbmc-addons/svn/trunk/plugins/video/reeplay.it"}]
        if self.INSTALLED:
            ok = self.showUpdates()
        xbmcplugin.endOfDirectory( int( sys.argv[ 1 ] ), ok, True, False)

    #####################################################################################################
    def findInstalled(self):
        log("> findInstalled()")
        
        self.INSTALLED = []
        ignoreList = (".","..",".backups")
        self.dialogProgress.update(0, "Checking installed ...")
        TOTAL_PATHS = len(self.XBMC_PATHS)
        for count, p in enumerate(self.XBMC_PATHS):
            if not os.path.isdir(p): continue

            files = os.listdir(p)
            for f in files:
                # ignore parent dirs
                if f in ignoreList: continue

                percent = int( count * 100.0 / TOTAL_PATHS )
                self.dialogProgress.update(percent)

                # extract version
                try:
                    filepath = os.path.join( p, f )
                    doc = open( os.path.join(filepath, "default.py"), "r" ).read()
                    ver = self.parseVersion(doc)
                    self.INSTALLED.append({"filepath": filepath, "ver": ver})
                except:
                    print str(sys.exc_info()[ 1 ])

#        pprint (self.INSTALLED)
        log("< findInstalled()  installed count=%d" % len(self.INSTALLED))

        
    #####################################################################################################
    def checkUpdates(self):
        log("> checkUpdates()")

        actionMsg = "Checking SVN ..."
        self.dialogProgress.update(0, actionMsg)

        TOTAL_PATHS = len(self.INSTALLED)
        quit = False
        for count, info in enumerate(self.INSTALLED):
            log("%d checking installed=%s" % (count, info))

            if not info['ver']: continue            # ignore installed without version doc tag

            # find installed category from filepath
            installedCategory  = self.parseCategory(info['filepath'])

            for repo in self.SVN_URL_LIST:
                repo_info = self._get_repo_info( repo )
                print repo_info
                base_url = repo_info[ 0 ] + repo_info[ 1 ]
                # xbmc-scripting has no 'scripts' in svn path, so remove it from installedCategory
                if base_url.startswith(self.URL_BASE_SVN_SCRIPTING):
                    installedCategory = installedCategory.replace('scripts/','')

                url = "/".join( [base_url, installedCategory, "default.py"] )
                log("url=" + url)

                percent = int( count * 100.0 / TOTAL_PATHS )
                self.dialogProgress.update(percent, actionMsg, installedCategory, urlparse.urlparse(url)[1])
                if self.dialogProgress.iscanceled():
                    quit = True
                    break

                # download default.py
                try:
                    sock = urllib.urlopen( url.replace(' ','%20') )
                    doc = sock.read()
                    sock.close()
                except:
                    xbmcgui.Dialog().ok(__plugin__ + " - ERROR!", str(sys.exc_info()[ 1 ]) )
                    quit = True
                    break
                else:
                    # check __version__ tag
                    svn_ver = self.parseVersion(doc)
                    if svn_ver:
                        self.INSTALLED[count]['svn_ver'] = svn_ver
                        self.INSTALLED[count]['svn_url'] = url.replace('/default.py','')
                        self.INSTALLED[count]['repo'] = repo
                        self.INSTALLED[count]['install'] = repo_info[ 2 ][ 2 ]
                        self.INSTALLED[count]['ioffset'] = repo_info[ 2 ][ 3 ]
                        self.INSTALLED[count]['voffset'] = repo_info[ 2 ][ 4 ]
                        
#        self.INSTALLED = [ { "filepath": "C:\Program Files\XBMC\plugins\Programs\GoogleReader", "ver": "0.1" , "svn_ver": "0.2", "svn_url": "http://xbmc-addons/svn/trunk/plugins/programs/GoogleReader"},

                        break # found in svn, move to next installed

            if quit: break

#        pprint (self.INSTALLED)
        log("< checkUpdates() updated count=%d" % len(self.INSTALLED))

    def _get_repo_info( self, repo ):
        # path to info file
        repopath = os.path.join( os.getcwd(), "resources", "repositories", repo, "repo.xml" )
        try:
            # grab a file object
            fileobject = open( repopath, "r" )
            # read the info
            info = fileobject.read()
            # close the file object
            fileobject.close()
            # repo's base url
            REPO_URL = re.findall( '<url>([^<]+)</url>', info )[ 0 ]
            # root of repository
            REPO_ROOT = re.findall( '<root>([^<]*)</root>', info )[ 0 ]
            # structure of repo
            REPO_STRUCTURES = re.findall( '<structure name="([^"]+)" noffset="([^"]+)" install="([^"]*)" ioffset="([^"]+)" voffset="([^"]+)"', info )
            return ( REPO_URL, REPO_ROOT, REPO_STRUCTURES[ 0 ], )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return None


    #####################################################################################################
    def parseVersion(self, doc):
        try:
            ver = re.search("__version__.*?[\"'](.*?)[\"']",  doc, re.IGNORECASE).group(1)
        except:
            ver = ""
        log("parseVersion() version=%s" % ver)
        return ver

    #####################################################################################################
    def parseCategory(self, filepath):
        try:
            cat = re.search("(plugins.*|scripts.*)$",  filepath, re.IGNORECASE).group(1)
            cat = cat.replace("\\", "/")
        except:
            ver = ""
        log("parseCategory() cat=%s" % cat)
        return cat

    #####################################################################################################
    def showUpdates(self):
        log("> showUpdates()")
        ok = False

        try:
            # create display list
            sz = len(self.INSTALLED)
            for info in self.INSTALLED:
#                print info
                path = ''
                ver = info.get('ver', '')
                filepath = info.get('filepath', '')
                svn_ver = info.get('svn_ver','')
                svn_url = info.get('svn_url','')
                if svn_url:
                    repo = re.search('(xbmc-\w+)', svn_url, re.IGNORECASE).group(1)
                else:
                    repo = "Unknown"

                # make update state according to found information
                if not ver:
                    verState = "Unknown Version"
                    ver = '?'
                elif not svn_url or not svn_ver:
                    verState = "Not in SVN"
                elif ver >= svn_ver:
                    verState = "OK"
                else:
                    # NEW AVAILABLE - setup callback url for plugin SVN Repo Installer
                    verState = "New! v" + svn_ver
                    trunk_url = re.search('(/trunk.*?)$', svn_url, re.IGNORECASE).group(1)
                    # determine install location according to repo
                    #if svn_url.startswith(self.URL_BASE_SVN_SCRIPTING):
                    #    install = 'scripts'
                    #else:
                    #    install = ''
                    #['plugin://programs/SVN Repo Installer/', '-1', '?download_url="%2Ftrunk%2Fplugins%2Fmusic/iTunes%2F"&repo=\'xbmc-addons\'&install=""&ioffset=2&voffset=0']

                    url_args = "download_url=%s&repo=%s&install=%s&ioffset=%s&voffset=%s" % \
                                (repr(urllib.quote_plus(trunk_url + "/")),
                                repr(urllib.quote_plus(info[ "repo"] )),
                                repr(info[ "install"] ),
                                info[ "ioffset"],
                                info[ "voffset"],)
                    path='%s?%s' % ( sys.argv[ 0 ], url_args, )
                    log("path=" + path)

                # display text
                text = "[%s] %s v%s" % (repo, self.parseCategory(filepath), ver)
                if verState.startswith( "New" ):
                    label2 = "[COLOR=FFFF0000]%s[/COLOR]" % verState
                elif verState == "OK":
                    label2 = "[COLOR=FF00FF00]%s[/COLOR]" % verState
                else:
                    label2 = "[COLOR=FFFFFF00]%s[/COLOR]" % verState
                
                # addons thumbnail from svn_url
                icon = ""
                thumbnail = ""
                if svn_url:
                    thumbnail = "/".join( [svn_url.replace(' ','%20'), "default.tbn"] )

                # determine default icon according to addon type
                if svn_url:
                    if svn_url.startswith(self.URL_BASE_SVN_SCRIPTING) or find(svn_url,'scripts/') != -1:
                        icon = "DefaultScriptBig.png"
                    elif find(svn_url,'programs/') != -1:
                        icon = "DefaultProgramBig.png"
                    elif find(svn_url,'music/') != -1:
                        icon = "defaultAudioBig.png"
                    elif find(svn_url,'pictures/') != -1:
                        icon = "defaultPictureBig.png"
                    elif find(svn_url,'videos/') != -1:
                        icon = "defaultVideoBig.png"
                # check skin for image, else fallback DefaultFile
                if not icon or not xbmc.skinHasImage(icon):
                    log("skinHasImage() not found: " + icon)
                    icon = "DefaultFileBig.png"
                if not thumbnail:
                    thumbnail = "DefaultFileBig.png"
                log("icon=" + icon)
                log("thumbnail=" + thumbnail)

                li=xbmcgui.ListItem( text, label2, icon, thumbnail, path=path )
                li.setInfo( type="Video", infoLabels={ "Title": text, "Genre": label2 } )

                xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=path, listitem=li, isFolder=False, totalItems=sz )

            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
            xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files")
            ok = True
        except:
            traceback.print_exc()

        log("< showUpdates() ok=%s" % ok)
        return ok
    
#################################################################################################################
if ( __name__ == "__main__" ):
    try:
        Main()
    except:
        traceback.print_exc()