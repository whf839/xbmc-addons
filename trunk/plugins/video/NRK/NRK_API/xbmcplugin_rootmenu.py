#
#
#   NRK plugin for XBMC Media center
#
# Copyright (C) 2009 Victor Vikene  contact: z0py3r@hotmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#

import sys, os
import api_nrk as nrk
import xbmc
from utils import Key, Plugin
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, getSetting

xbmc.log( "PLUGIN::LOADED -> '%s'" % __name__, xbmc.LOGNOTICE )
lang = xbmc.getLocalizedString
FAV_PATH = os.path.join(
                xbmc.translatePath("special://profile/"), 
                "plugin_data", 
                "video", 
                os.path.basename(Plugin.cwd), 
                "shows.xml"
            )

class Main:
    
    rpath = os.path.join(os.getcwd(), 'resources', 'images')
    
    
    
    def add(self, label, prefix, type, id=None, img='', icon='', isdir=True, commands=None):
    
        if img != '':
            img = os.path.join(self.rpath, img)
            
        url = Key.build_url(prefix, type=type, id=id)
        li  = ListItem(label, iconImage=icon, thumbnailImage=img)
        if commands:
            li.addContextMenuItems( commands, True )
        ok  = addDirectoryItem(self.hndl, url=url, listitem=li, isFolder=isdir)
        
        return ok
        
        
        
    def __init__(self):
    
        self.hndl = int(sys.argv[1])
     
     
        self.add('Program',  nrk.PROGRAM,  nrk.PROGRAM,  img='program-icon.png')
        self.add('Direkte',  nrk.PROGRAM,  nrk.LIVE,     img='live-icon.png')
        self.add('Kanalene', nrk.CHANNELS, nrk.CHANNELS, img='channels-icon.png')
            
        self.add('Sport',    nrk.PROGRAM, nrk.PLAYLIST, 'sport',    'sports-icon.png')
        self.add('Nyheter',  nrk.PROGRAM, nrk.PLAYLIST, 'nyheter',  'news-icon.png')
        self.add('Distrikt', nrk.PROGRAM, nrk.PLAYLIST, 'distrikt', 'regions-icon.png')
        #self.add('Barn',     nrk.PROGRAM, nrk.PLAYLIST, 'super',    'children-icon.png')
        self.add('Natur',    nrk.PROGRAM, nrk.PLAYLIST, 'natur',    'nature-icon.png')
      
        self.add('NRKBeta',           'nrkbeta',  'feed',     img='nrkbeta.png')
        self.add('NRK Nettradio',     'webradio', 'webradio', img='speaker-icon.png')
        self.add('NRK Video Podcast', 'podcast',  'video',    img='video-podcast.png')
        self.add('NRK Lyd Podcast',   'podcast',  'sound',    img='audio-podcast.png')
        
        commands = []
        commands.append(( lang(30800), 
                        'XBMC.RunPlugin(%s)' % ( Key.build_url('teletext', page=101)), 
                        ))
        commands.append(( lang(30801), 
                        'XBMC.RunPlugin(%s)' % ( Key.build_url('teletext', page=131)), 
                        ))
        commands.append(( lang(30802), 
                        'XBMC.RunPlugin(%s)' % ( Key.build_url('teletext', page=200)), 
                        ))
        commands.append(( lang(30803), 
                        'XBMC.RunPlugin(%s)' % ( Key.build_url('teletext', page=300)), 
                        ))
        commands.append(( lang(30804), 
                        'XBMC.RunPlugin(%s)' % ( Key.build_url('teletext', page=590)), 
                        ))
        self.add('NRK Tekst TV',      'teletext', 'teletext', img='ttv-icon.png', isdir=False, commands=commands)
        
        if os.path.isfile(FAV_PATH):
          self.add('Favoritt Program', 'favorites', 'favorites', img='favorites.png')
          
        endOfDirectory(self.hndl)
