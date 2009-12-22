#############################################################################
#
# Navi-X Playlist browser
# v3.0 by rodejo (rodejo16@gmail.com)
#
# -v1.01  (2007/04/01) first release
# -v1.2   (2007/05/10)
# -v1.21  (2007/05/20)
# -v1.22  (2007/05/26)
# -v1.3   (2007/06/15)
# -v1.31  (2007/06/30)
# -v1.4   (2007/07/04)
# -v1.4.1 (2007/07/21)
# -v1.5   (2007/09/14)
# -v1.5.1 (2007/09/17)
# -v1.5.2 (2007/09/22)
# -v1.6   (2007/09/29)
# -v1.6.1 (2007/10/19)
# -v1.7 beta (2007/11/14)
# -v1.7   (2007/11/xx)
# -v1.7.1 (2007/12/15)
# -v1.7.2 (2007/12/20)
# -v1.8 (2007/12/31)
# -v1.9 (2008/02/10)
# -v1.9.1 (2008/02/10)
# -v1.9.2 (2008/02/23)
# -v1.9.3 (2008/06/20)
# -v2.0   (2008/07/21)
# -v2.1   (2008/08/08)
# -v2.2   (2008/08/31)
# -v2.3   (2008/10/18)
# -v2.4   (2008/12/04)
# -v2.5   (2009/01/24)
# -v2.6   (2009/03/21)
# -v2.7   (2009/04/11)
# -v2.7   (2009/05/01) 
# -v3.0.2 (2009/12/21)
#
#############################################################################

from string import *
import sys, os.path
import urllib
import re, random, string
import xbmc, xbmcgui,xbmcplugin
import re, os, time, datetime, traceback
import shutil
import zipfile
import copy
import htmlentitydefs

#import threading

sys.path.append(os.path.join(os.getcwd().replace(";",""),'src'))
from libs2 import *
from settings import *
from CPlayList import *
from CFileLoader import *
#from CDownLoader import *
from CPlayer import *
#from CDialogBrowse import *
from CTextView import *
from CInstaller import *
#from skin import *
#from CBackgroundLoader import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

#####################################################################
# Description: 
######################################################################
def Init():
    #Create default DIRs if not existing.
    if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
    if not os.path.exists(imageCacheDir): 
        os.makedirs(imageCacheDir)
    
    if not os.path.exists(myDownloadsDir): 
        os.makedirs(myDownloadsDir)
 
######################################################################
# Description: Parse playlist file. Playlist file can be a:
#              -PLX file;
#              -RSS v2.0 file (e.g. podcasts);
#              -RSS daily Flick file (XML1.0);
#              -html Youtube file;
# Parameters : URL (optional) =URL of the playlist file.
#              mediaitem (optional)=Playlist mediaitem containing 
#              playlist info. Replaces URL parameter.
#              start_index (optional) = cursor position after loading 
#              playlist.
#              reload (optional)= indicates if the playlist shall be 
#              reloaded or only displayed.
# Return     : 0 on success, -1 if failed.
######################################################################
def ParsePlaylist(mediaitem=CMediaItem() , proxy="CACHING"):
    playlist = CPlayList()  
   
    type = mediaitem.GetType()
    URL=''
   
    #load the playlist
    if type == 'rss_flickr_daily':
        result = playlist.load_rss_flickr_daily(URL, mediaitem, proxy)
    elif type[0:3] == 'rss':
        result = playlist.load_rss_20(URL, mediaitem, proxy)
    elif type == 'html_youtube':
        result = playlist.load_html_youtube(URL, mediaitem, proxy)
    elif type == 'xml_shoutcast':
        result = playlist.load_xml_shoutcast(URL, mediaitem, proxy)
    elif type == 'xml_applemovie':
        result = playlist.load_xml_applemovie(URL, mediaitem, proxy)
    elif type == 'directory':
        result = playlist.load_dir(URL, mediaitem, proxy)
    else: #assume playlist file
        result = playlist.load_plx(URL, mediaitem, proxy)
            
    if result == -1: #error
        dialog = xbmcgui.Dialog()
        dialog.ok("Error", "This playlist requires a newer Navi-X version")
    elif result == -2: #error
        dialog = xbmcgui.Dialog()
        dialog.ok("Error", "Cannot open file.")
                
    if result != 0: #failure
        return -1
            
    #succesful
    playlist.save(RootDir + 'source.plx')
                   
    today=datetime.date.today()
    #fill the main list
    
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    
    for m in playlist.list:
        if m.thumb != 'default':
            thumb = m.thumb            
        else:
            thumb = getPlEntryThumb(m)

        label2 = ''
        if m.date != '':
            l=m.date.split('-')
            entry_date = datetime.date(int(l[0]), int(l[1]), int(l[2]))
            days_past = (today-entry_date).days
            if days_past <= 10:
                if days_past <= 0:
                    label2 = ' [NEW today]'
                elif days_past == 1:
                    label2 = ' [NEW yesterday]'
                else:
                    label2 = ' [NEW '+ str(days_past) + ' days ago]'
                        
        folder=False
        type = m.GetType()
        if (type == 'playlist') or (type == 'rss') or\
           (type == 'rss_flickr_daily') or (type == 'html_youtube') or \
           (type == 'xml_applemovie') or (type == 'directory') or \
           (type == 'xml_shoutcast') or (type == 'search_shoutcast') or \
           (type == 'search_youtube') or (type == 'search'):
            folder = True
            
        desc=''
        if m.description:
                #desc=m.description
                desc=HTMLunescape(m.description)
        
        item = xbmcgui.ListItem(m.name+label2, iconImage=thumb, thumbnailImage=thumb)
        item.setInfo( type=m.type, infoLabels={ "Title": m.name , "Plot": desc } )
        #hack to play youtube swf
        if m.URL.find('youtube.com/v/')>-1:
                m.URL=m.URL.replace('http://youtube.com','http://www.youtube.com')
                m.URL=m.URL.replace('youtube.com/v/','youtube.com/watch?v=')
                m.URL=m.URL.replace('.swf','')
                m.processor='http://navix.turner3d.net/proc/youtube_movies'

        URL = sys.argv[0] + "?mode=0&name=" + urllib.quote_plus(m.name) + \
                             "&type=" + urllib.quote_plus(m.type) + \
                             "&url=" + urllib.quote_plus(m.URL) + \
                             "&processor=" + urllib.quote_plus(m.processor) + \
                             "&date=" + urllib.quote_plus(m.date)                           
                       
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), URL, item, folder, playlist.size())                            
           
        #addSortMethod
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_PLAYLIST_ORDER)
    #xbmcplugin.endOfDirectory(int(sys.argv[1]))
       
    return 0 #success

######################################################################
# Description: Gets the playlist entry thumb image for different types
# Parameters : type = playlist entry type
# Return     : thumb image (local) file name
######################################################################
def getPlEntryThumb(mediaitem):            
    type = mediaitem.GetType()       
        
    #some types are overruled.
    if type[0:3] == 'rss':
        type = 'rss' 
    elif type[0:3] == 'xml':
        type = 'playlist'
    elif type == 'html_youtube':
        type = 'playlist'
    elif type[0:6] == 'search':
        type = 'search'               
    elif type == 'directory':
        type = 'playlist'               
    elif mediaitem.type == 'skin':
        type = 'script'                
    
    #if the icon attribute has been set then use this for the icon.
    URL=''
    if mediaitem.icon != 'default':
        URL = mediaitem.icon

    if URL != '':
        ext = getFileExtension(URL)
        loader = CFileLoader2() #file loader
        loader.load(URL, imageCacheDir + "icon." + ext, timeout=2, proxy="ENABLED", content_type='image')
        if loader.state == 0:
            return loader.localfile
            
    return imageDir+'icon_'+str(type)+'.png'
    
######################################################################
# Description: Handles the selection of an item in the list.
######################################################################  
def getPlaylistPosition(self):
    pos = self.list.getSelectedPosition()
        
    if (self.page > 0):
        pos = pos + (self.page*page_size) - 1
            
    return pos
    
######################################################################
# Description: Handles the selection of an item in the list.
# Parameters : playlist(optional)=the source playlist;
#              pos(optional)=media item position in the playlist;
#              append(optional)=true is playlist must be added to 
#              history list;
#              URL(optional)=link to media file;
# Return     : -
######################################################################
def SelectItem(mediaitem=CMediaItem()):
    type = mediaitem.GetType()
    if type == 'playlist' or type == 'favorite' or type[0:3] == 'rss' or \
       type == 'rss_flickr_daily' or type == 'directory' or \
       type == 'html_youtube' or type == 'xml_shoutcast' or \
       type == 'xml_applemovie':
           
            result = ParsePlaylist(mediaitem)           

    elif type == 'video' or type == 'audio' or type == 'html':
        MyPlayer = CPlayer(xbmc.PLAYER_CORE_AUTO, function=myPlayerChanged)
        result = MyPlayer.play_URL(mediaitem.URL, mediaitem)       
            
        if result != 0:
            dialog = xbmcgui.Dialog()
            dialog.ok("Error", "Could not open file.")
                      
    elif type == 'image':
        viewImage(mediaitem.URL) #single file show
    elif type == 'text':
        OpenTextFile(mediaitem=mediaitem)
    elif type[0:6] == 'script' or type[0:6] == 'plugin':
        InstallApp(mediaitem=mediaitem)
    elif type == 'download':
        Download(mediaitem.URL)
    elif (type[0:6] == 'search'):
        PlaylistSearch(mediaitem, True)
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("Playlist format error", '"' + type + '"' + " is not a valid type.")
    
#    
def Download(url):
        dialog = xbmcgui.Dialog()
        fn = dialog.browse(3,'Select destination','files')
        name=url[url.rfind('/'):]
        name=urllib.unquote_plus(name)
        fn=fn+name
        urllib.urlretrieve(url,fn)
        
######################################################################
# Description: Player changed info can be catched here
# Parameters : action=user key action
# Return     : -
######################################################################
def myPlayerChanged(state):
    #At this moment nothing to handle.
    pass


######################################################################
# Description: Handles display of a text file.
# Parameters : URL=URL to the text file.
# Return     : -
######################################################################
def OpenTextFile(URL='', mediaitem=CMediaItem()):
    textwnd = CTextView()
    result = textwnd.OpenDocument(URL, mediaitem)

    if result == 0:
        textwnd.doModal()
        #textwnd.show()
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("Error", "Could not open file.")
    
######################################################################
# Description: Handles image slideshow.
# Parameters : playlist=the source playlist
#              pos=media item position in the playlist
#              mode=view mode (0=slideshow, 1=recursive slideshow)
#              URL(optional) = URL to image
# Return     : -
######################################################################
def viewImage(iURL=''):
    mode = 0
#    self.setInfoText("Loading...")
    #clear the imageview cache
#    self.delFiles(imageCacheDir)

    if not os.path.exists(imageCacheDir): 
        os.mkdir(imageCacheDir) 

    if mode == 0: #single file show
        localfile= imageCacheDir + '0.'
        if iURL != '':
            URL = iURL
#        else:    
#            URL = playlist.list[pos].URL
        ext = getFileExtension(URL)

        if URL[:4] == 'http':
            loader = CFileLoader()
            loader.load(URL, localfile + ext, proxy="DISABLED")
            if loader.state == 0:
                xbmc.executebuiltin('xbmc.slideshow(' + imageCacheDir + ')')
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Error", "Unable to open image.")
        else:
            #local file
            shutil.copyfile(URL, localfile + ext)
            xbmc.executebuiltin('xbmc.slideshow(' + imageCacheDir + ')')
            
#    elif mode == 1: #recursive slideshow
#        #in case of slideshow store default image
#        count=0
#        for i in range(self.list.size()):
#            if playlist.list[i].type == 'image':
#                localfile=imageCacheDir+'%d.'%(count)
#                URL = playlist.list[i].URL
#                ext = getFileExtension(URL)
#                shutil.copyfile(imageDir+'imageview.png', localfile + ext)
#                count = count + 1
#        if count > 0:
#            count = 0
#            index = pos
#            for i in range(self.list.size()):
#                if count == 2:
#                    xbmc.executebuiltin('xbmc.recursiveslideshow(' + imageCacheDir + ')')
#                    self.state_action = 0
#                elif (count > 2) and (self.state_action == 1):
#                    break
#                            
#                if playlist.list[index].type == 'image':
#                    localfile=imageCacheDir+'%d.'%(count)
#                    URL = playlist.list[index].URL
#                    ext = getFileExtension(URL)
#                    self.loader.load(URL, localfile + ext, proxy="DISABLED")
#                    if self.loader.state == 0:
#                        count = count + 1
#                index = (index + 1) % self.list.size()
#
#            if self.list.size() < 3:
#                #start the slideshow after the first two files. load the remaining files
#                #in the background
#                xbmc.executebuiltin('xbmc.recursiveslideshow(' + imageCacheDir + ')')
#        if count == 0:
#            dialog = xbmcgui.Dialog()
#            dialog.ok("Error", "No images in playlist.")
            
#    self.setInfoText(visible=0)
                
######################################################################
# Description: Handles Installation of Applications
# Parameters : URL=URL to the script ZIP file.
# Return     : -
######################################################################
def InstallApp(URL='', mediaitem=CMediaItem()):
    dialog = xbmcgui.Dialog()
            
    type = mediaitem.GetType(0)
    attributes = mediaitem.GetType(1)
            
    if type == 'script':
        if dialog.yesno("Message", "Install Script?") == False:
            return

        installer = CInstaller()
        result = installer.InstallScript(URL, mediaitem)

    elif type == 'plugin':
        if dialog.yesno("Message", "Install " + attributes + " Plugin?") == False:
            return
        
        installer = CInstaller()
        result = installer.InstallPlugin(URL, mediaitem)
    elif type == 'skin':
        if dialog.yesno("Message", "Install Skin?") == False:
            return

        installer = CInstaller()
        result = installer.InstallSkin(URL, mediaitem)
    else:
        result = -1 #failure
            
    if result == 0:
        dialog.ok(" Installer", "Installation successful.")
        if attributes == 'navi-x':
            dialog.ok(" Installer", "Please restart Navi-X.")
    elif result == -1:
        dialog.ok(" Installer", "Installation aborted.")
    elif result == -3:
        dialog.ok(" Installer", "Invalid ZIP file.")
    else:
        dialog.ok(" Installer", "Installation failed.")                
             
######################################################################
# Description: Handle selection of playlist search item (e.g. Youtube)
# Parameters : item=CMediaItem
#              append(optional)=true is playlist must be added to 
#              history list;
# Return     : -
######################################################################
def PlaylistSearch(item, append):
#    possibleChoices = []
#    possibleChoices.append("New Search")
    #for m in self.SearchHistory:
    #    possibleChoices.append(m)
#    possibleChoices.append("Cancel")                
#    dialog = xbmcgui.Dialog()
#    choice = dialog.select("Search", possibleChoices)

#    if (choice == -1) or (choice == (len(possibleChoices)-1)):
#        return #canceled

    #if choice > 0:
    #    string = self.SearchHistory[choice-1]
    #else:  #New search
    string = ''
            
    keyboard = xbmc.Keyboard(string, 'Search')
    keyboard.doModal()
    if (keyboard.isConfirmed() == False):
        return #canceled
    searchstring = keyboard.getText()
    if len(searchstring) == 0:
        return  #empty string search, cancel
            
    #if search string is different then we add it to the history list.
    #if searchstring != string:
    #    self.SearchHistory.insert(0,searchstring)
    #    if len(self.SearchHistory) > 8: #maximum 8 items
    #        self.SearchHistory.pop()
    #    self.onSaveSearchHistory()
    
    #get the search type:
    index=item.type.find(":")
    if index != -1:
        search_type = item.type[index+1:]
    else:
        search_type = ''
            
    #youtube search
    if (item.type == 'search_youtube') or (search_type == 'html_youtube'):
        fn = searchstring.replace(' ','+')
        if item.URL != '':
            URL = item.URL
        else:
            URL = 'http://www.youtube.com/results?search_query='
        URL = URL + fn
                  
        #ask the end user how to sort
        possibleChoices = ["Relevance", "Date Added", "View Count", "Rating"]
        dialog = xbmcgui.Dialog()
        choice = dialog.select("Sort by", possibleChoices)

        #validate the selected item
        if choice == 1: #Date Added
            URL = URL + '&search_sort=video_date_uploaded'
        elif choice == 2: #View Count
            URL = URL + '&search_sort=video_view_count'
        elif choice == 3: #Rating
            URL = URL + '&search_sort=video_avg_rating'
               
        mediaitem=CMediaItem()
        mediaitem.URL = URL
        mediaitem.type = 'html_youtube'
        mediaitem.name = 'search results: ' + searchstring
        mediaitem.player = item.player

        #create history item
#        tmp = CHistorytem()
#        tmp.index = self.list.getSelectedPosition()
#        tmp.mediaitem = self.mediaitem

#        self.pl_focus = self.playlist
        result = ParsePlaylist(mediaitem=mediaitem)
                
#        if result == 0 and append == True: #successful
#            self.History.append(tmp)
#            self.history_count = self.history_count + 1
    elif item.type == 'search_shoutcast' or (search_type == 'xml_shoutcast'):
        fn=urllib.quote(searchstring)
        URL = 'http://www.shoutcast.com/sbin/newxml.phtml?search='
        URL = URL + fn
        
        mediaitem=CMediaItem()
        mediaitem.URL = URL
        mediaitem.type = 'xml_shoutcast'
        mediaitem.name = 'search results: ' + searchstring
        mediaitem.player = item.player

        #create history item
#        tmp = CHistorytem()
#        tmp.index = self.list.getSelectedPosition()
#        tmp.mediaitem = self.mediaitem

#        self.pl_focus = self.playlist
        result = ParsePlaylist(mediaitem=mediaitem)      
#        if result == 0 and append == True: #successful
#            self.History.append(tmp)
#            self.history_count = self.history_count + 1
    elif item.type == 'search_flickr' or (search_type == 'html_flickr'):
        fn = searchstring.replace(' ','+')
        URL = 'http://www.flickr.com/search/?q='
        URL = URL + fn
        
        mediaitem=CMediaItem()
        mediaitem.URL = URL
        mediaitem.type = 'html_flickr'
        mediaitem.name = 'search results: ' + searchstring
        mediaitem.player = item.player

        #create history item
#        tmp = CHistorytem()
#        tmp.index = self.list.getSelectedPosition()
#        tmp.mediaitem = self.mediaitem

#        self.pl_focus = self.playlist
        result = ParsePlaylist(mediaitem=mediaitem)
                
#        if result == 0 and append == True: #successful
#            self.History.append(tmp)
#            self.history_count = self.history_count + 1

    else: #generic search
        fn = urllib.quote(searchstring)
        URL = item.URL
        URL = URL + fn
                       
        mediaitem=CMediaItem()
        mediaitem.URL = URL
        if search_type != '':
            mediaitem.type = search_type
        else: #default
            mediaitem.type = 'playlist'
                    
        mediaitem.name = 'search results: ' + searchstring
        mediaitem.player = item.player

        #create history item
        #tmp = CHistorytem()

        #tmp.index = self.getPlaylistPosition()
        #tmp.mediaitem = self.mediaitem

        #self.pl_focus = self.playlist
        result = ParsePlaylist(mediaitem=mediaitem)
                
        #if result == 0 and append == True: #successful
            #self.History.append(tmp)
            #self.history_count = self.history_count + 1             

######################################################################
# Description: Deletes all files in a given folder and sub-folders.
#              Note that the sub-folders itself are not deleted.
# Parameters : folder=path to local folder
# Return     : -
######################################################################
def delFiles(folder):
    try:        
        for root, dirs, files in os.walk(folder , topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
    except IOError:
        return
        
def HTMLunescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
    
############End of file
