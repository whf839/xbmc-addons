"""
    GUI for displaying maps and forecasts from weather.com
    
    Nuka1195
"""

# main imports
import sys
import os

import xbmc
import xbmcgui

_ = xbmc.Language( os.getcwd() ).getLocalizedString

dialog = xbmcgui.DialogProgress()
dialog.create( _( 0 ), _( 10 ) )

from threading import Timer

import resources.lib.TWCClient as TWCClient

# determine users preference window or dialog
if ( sys.modules[ "__main__" ].window ):
    module = xbmcgui.WindowXML
else:
    module = xbmcgui.WindowXMLDialog


class GUI( module ):
    # constants
    ACTION_EXIT_SCRIPT = ( 10, )
    ACTION_SET_DEFAULT = ( 117, )
    ACTION_TOGGLE_MAP = ( 18, )
    ACTION_MOVEMENT_LEFT = ( 1, )
    ACTION_MOVEMENT_RIGHT = ( 2, )
    # required control id's
    CONTROL_MAP_LISTS = ( 500, 501, 502, )
    CONTROL_HOUR_LIST = 600
    CONTROL_10DAY_LIST = 700
    # view buttons
    CONTROL_MAP_BUTTON = 200
    CONTROL_36HOUR_BUTTON = 201
    CONTROL_HOURBYHOUR_BUTTON = 202
    CONTROL_WEEKEND_BUTTON = 203
    CONTROL_10DAY_BUTTON = 204
    CONTROL_SETTINGS_BUTTON = 205
    CONTROL_ALERTS_BUTTON = 206
    # toggle buttons
    CONTROL_WEEKEND_TOGGLE_BUTTON = 300
    CONTROL_MAP_TOGGLE_BUTTON = 301
    CONTROL_PLAY_VIDEO_BUTTON = 302
    # settings buttons
    CONTROL_ANIMATED_SETTING_BUTTON = 400
    CONTROL_METRIC_SETTING_BUTTON = 401
    CONTROL_SHOW_ALERTS_SETTING_BUTTON = 402
    CONTROL_MAPS_LIST_SETTING_BUTTONS = ( 403, 404, 405, )
    CONTROL_FANART_SETTING_BUTTON = 406
    CONTROL_FANART_TYPE_SETTING_BUTTON = 407
    CONTROL_FANART_DIFFUSE_SETTING_BUTTON = 408

    def __init__( self, *args, **kwargs ):
        module.__init__( self, *args, **kwargs )
        # set our defaults
        self._init_defaults()
        self._init_view_status()
        # set the maps path
        self._set_maps_path()
        # get our local code, needed for localizing radars
        self._get_local_code()
        # get our new TWCClient
        self._get_client()
        # set default map list settings
        self._set_default_maplists()

    def onInit( self ):
        dialog.close()
        # get default view
        self._get_default_view()
        # get current window
        self._get_current_window()
        # set script info
        self._set_script_info()
        # set default view
        if ( self.defaultview == self.CONTROL_36HOUR_BUTTON ):
            # get our 36 hour forecast
            self._fetch_36_forecast()
        elif ( self.defaultview == self.CONTROL_HOURBYHOUR_BUTTON ):
            # get our hour by hour forecast
            self._fetch_hour_forecast()
        elif ( self.defaultview == self.CONTROL_WEEKEND_BUTTON ):
            # get our hour by hour forecast
            self._fetch_weekend_forecast()
        elif ( self.defaultview == self.CONTROL_10DAY_BUTTON ):
            # get our hour by hour forecast
            self._fetch_10day_forecast()
        else:
            # set map list and get default map
            self._fetch_map_list()

    def _get_current_window( self ):
        # TODO: enable this code block if dialogs get properties
        """
        # current window for setting properties
        self.CURRENT_WINDOW = xbmcgui.getCurrentWindowDialogId()
        # not a valid dialog window, so grab the current window
        if ( not( 13000 <= self.CURRENT_WINDOW <= 13100 ) ):
        """
        self.CURRENT_WINDOW = xbmcgui.Window( xbmcgui.getCurrentWindowId() )

    def _init_defaults( self ):
        self.timer = None
        self.toggle = True
        self.weekendToggle = False
        self.loading = False
        self.maps_path = False
        self.current_map = None

    def _set_default_maplists( self ):
        if ( xbmc.getInfoLabel( "Skin.String(twc-maplist1-category)" ) == "" ):
            xbmc.executebuiltin( "Skin.SetString(twc-maplist1-category,%s)" % ( self.TWCClient.BASE_MAPS[ 0 ][ 0 ], ) )
            xbmc.executebuiltin( "Skin.SetString(twc-maplist1-title,%s)" % ( self.TWCClient.BASE_MAPS[ 0 ][ 2 ], ) )
        if ( xbmc.getInfoLabel( "Skin.String(twc-maplist2-category)" ) == "" ):
            xbmc.executebuiltin( "Skin.SetString(twc-maplist2-category,%s)" %  ( self.TWCClient.BASE_MAPS[ 2 ][ 0 ], ) )
            xbmc.executebuiltin( "Skin.SetString(twc-maplist2-title,%s)" % ( self.TWCClient.BASE_MAPS[ 2 ][ 2 ], ) )
        if ( xbmc.getInfoLabel( "Skin.String(twc-maplist3-category)" ) == "" ):
            xbmc.executebuiltin( "Skin.SetString(twc-maplist3-category,%s)" % ( self.TWCClient.BASE_MAPS[ 37 ][ 0 ], ) )
            xbmc.executebuiltin( "Skin.SetString(twc-maplist3-title,%s)" % ( self.TWCClient.BASE_MAPS[ 37 ][ 2 ], ) )

    def _set_script_info( self ):
        self.CURRENT_WINDOW.setProperty( "version", "%s - r%s" % ( sys.modules[ "__main__" ].__version__, str( sys.modules[ "__main__" ].__svn_revision__ ) ) )
        self.CURRENT_WINDOW.setProperty( "author", sys.modules[ "__main__" ].__author__ )
        if ( self.defaultview == self.CONTROL_MAP_BUTTON ):
            self.CURRENT_WINDOW.setProperty( "defaultview", "%s - %s" % ( _( self.defaultview ), xbmc.getInfoLabel( "Skin.String(twc-defaultmap)" ), ) )
        else:
            self.CURRENT_WINDOW.setProperty( "defaultview", _( self.defaultview ) )
        self.CURRENT_WINDOW.setProperty( "svnurl", sys.modules[ "__main__" ].__url__ )
        self.CURRENT_WINDOW.setProperty( "scripturl", sys.modules[ "__main__" ].__svn_url__ )

    def _init_view_status( self ):
        self.forecast36Hour = None
        self.forecastHourByHour = None
        self.forecastWeekend = None
        self.forecast10Day = None

    def _get_client( self ):
        # setup our radar client
        self.TWCClient = TWCClient.TWCClient( self.local_code )

    def _get_local_code( self ):
        # use the Weather window property (should never return None)
        self.local_code = xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" )

    def _set_maps_path( self, path=0 ):
        # we have three possibilities. loading, default (error) or the actual map path
        if ( path == 0 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,weather.com/loading)" )
        elif ( path == 1 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,%s)" % ( self.maps_path, ) )
        elif ( path == 2 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,weather.com/default)" )

    def _fetch_map_list( self ):
        # only run this once
        if ( self.current_map is None ):
            ### clear our maplist exists properties
            ##for count in range( len( self.CONTROL_MAP_LISTS ) ):
            ##    self.CURRENT_WINDOW.clearProperty( "maplist%d" % ( count + 1, ) )
            # initialize current map
            self.current_map = 0
            self.current_maplist = self.CONTROL_MAP_LISTS[ 0 ]
            # get the users default map
            default = xbmc.getInfoLabel( "Skin.String(twc-defaultmap)" )
            map_lists = 1
           # set number of map lists, only the US has multiple
            map_lists = len( self.CONTROL_MAP_LISTS )
            # enumurate thru map lists and fetch map list
            for maplist_count in range( map_lists ):
                # what is users preference
                map = xbmc.getInfoLabel( "Skin.String(twc-maplist%d-category)" % ( maplist_count + 1, ) )
                # check for users preferemce
                for count, mapc in enumerate( self.TWCClient.BASE_MAPS ):
                    # found it, no need to continue
                    if ( mapc[ 0 ] == map ):
                        break
                # set map list tab exists
                self.CURRENT_WINDOW.setProperty( "maplist%d" % ( maplist_count + 1, ), "1" )
                # fetch map list
                map_list = self.TWCClient.fetch_map_list( count )
                # lock the gui for faster updating
                xbmcgui.lock()
                # reset our map list
                self.getControl( self.CONTROL_MAP_LISTS[ maplist_count ] ).reset()
                # enumerate thru our map list and add map and title and check for default
                for count, map in enumerate( map_list ):
                    # create our listitem, label 2 is not visible (in default skin)
                    listitem = xbmcgui.ListItem( map[ 1 ], map [ 0 ] )
                    # if we have a match, set our class variable
                    if ( map[ 1 ] == default ):
                        self.current_map = count
                        self.current_maplist = self.CONTROL_MAP_LISTS[ maplist_count ]
                    # add map to our list
                    self.getControl( self.CONTROL_MAP_LISTS[ maplist_count ] ).addItem( listitem )
                # unlock the gui
                xbmcgui.unlock()
            # fetch our map
            self._fetch_map( self.current_map, self.current_maplist )

    def _fetch_map( self, map, controlId ):
        # set the current map
        self.current_map = map
        self.current_maplist = controlId
        # cancel any timer
        if ( self.timer is not None ):
            self.timer.cancel()
            self.timer = None
        # do not refresh map if not current view
        if ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),200) | [StringCompare(Window.Property(CurrentView),206) + IsEmpty(Window.Property(Alerts))]" ) ):
            #return
            # get maps url name
            map = self.getControl( controlId ).getListItem( map ).getLabel2()
            # make sure user can't keep selecting maps
            self.loading = True
            # we set our skin setting to defaultimages while downloading
            self._set_maps_path()
            # fetch the available map urls
            maps = self.TWCClient.fetch_map_urls( map, controlId - self.CONTROL_MAP_LISTS[ 0 ] )
            # fetch the images
            self.maps_path, expires = self.TWCClient.fetch_images( maps )
            # hack incase the weather in motion link was bogus
            if ( expires < 0 and len( maps[ 1 ] ) ):
                self.maps_path, expires = self.TWCClient.fetch_images( ( maps[ 0 ], [], ) )
            # we check 36 hour as it holds any alerts
            self._fetch_36_forecast( False )
            # now set our skin string so multi image will display images 1==success, 2==failure
            self._set_maps_path( ( self.maps_path == "" ) + 1 )
            # successful so set timer thread
            if ( self.maps_path != "" and expires > 0 ):
                self.timer = Timer( expires, self._fetch_map, ( self.current_map, controlId, ) )
                self.timer.start()
            # reset loading status
            self.loading = False

    def _set_alerts( self, alerts, alertscolor, alertscount ):
        # set any alerts
        self.CURRENT_WINDOW.setProperty( "Alerts", alerts )
        self.CURRENT_WINDOW.setProperty( "AlertsColor", alertscolor )
        self.CURRENT_WINDOW.setProperty( "AlertsCount", ( "", str( alertscount ), )[ alertscount > 1 ] )
        self.CURRENT_WINDOW.setProperty( "AlertsLabel", _( self.CONTROL_ALERTS_BUTTON * ( 10, 1, )[ alertscount > 1 ] ) )

    def _set_video( self, video_url ):
        self.CURRENT_WINDOW.setProperty( "Video", video_url )

    def _fetch_36_forecast( self, showView=True ):
        # fetch 36 hour forecast
        alerts, alertscolor, alertscount, forecasts, video = self.TWCClient.fetch_36_forecast( self.CURRENT_WINDOW.getProperty( "Video" ) )
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # set any alerts
            self._set_alerts( alerts, alertscolor, alertscount )
            # set video
            self._set_video( video )
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                self.CURRENT_WINDOW.setProperty( "36Hour%dicon" % ( day + 1, ), forecast[ 1 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dbrief" % ( day + 1, ), forecast[ 2 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dtemptitle" % ( day + 1, ), forecast[ 3 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dtemp" % ( day + 1, ), forecast[ 4 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dpreciptitle" % ( day + 1, ), forecast[ 5 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dprecip" % ( day + 1, ), forecast[ 6 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%doutlook" % ( day + 1, ), forecast[ 7 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%ddaylight" % ( day + 1, ), forecast[ 8 ] )
                self.CURRENT_WINDOW.setProperty( "36Hour%dtitle" % ( day + 1, ), forecast[ 0 ] )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _fetch_hour_forecast( self ):
        # fetch hour by hour forecast
        alerts, alertscolor, alertscount, headings, forecasts = self.TWCClient.fetch_hour_forecast()
        try:
            # set any alerts
            self._set_alerts( alerts, alertscolor, alertscount )
            # lock the gui for faster updating
            xbmcgui.lock()
            # reset list
            self.getControl( self.CONTROL_HOUR_LIST ).reset()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                self.CURRENT_WINDOW.setProperty( "HBHHead%d" % ( count + 1, ), heading )
            # enumerate thru and set the info
            for forecast in forecasts:
                listitem = xbmcgui.ListItem( forecast[ 0 ] )
                listitem.setProperty( "icon", forecast[ 1 ] )
                listitem.setProperty( "brief", forecast[ 2 ] )
                listitem.setProperty( "temp", forecast[ 3 ] )
                listitem.setProperty( "feels", forecast[ 4 ] )
                listitem.setProperty( "precip", forecast[ 5 ] )
                #listitem.setProperty( "dew", forecast[ 6 ] )
                listitem.setProperty( "humidity", forecast[ 6 ] )
                listitem.setProperty( "wind", forecast[ 7 ] )
                self.getControl( self.CONTROL_HOUR_LIST ).addItem( listitem )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _fetch_weekend_forecast( self ):
        # fetch 36 hour forecast
        alerts, alertscolor, alertscount, forecasts = self.TWCClient.fetch_weekend_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # set any alerts
            self._set_alerts( alerts, alertscolor, alertscount )
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                self.CURRENT_WINDOW.setProperty( "Weekend%ddate" % ( day + 1, ), forecast[ 1 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dicon" % ( day + 1, ), forecast[ 2 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dbrief" % ( day + 1, ), forecast[ 3 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dhightitle" % ( day + 1, ), forecast[ 4 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dhightemp" % ( day + 1, ), forecast[ 5 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dlowtitle" % ( day + 1, ), forecast[ 6 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dlowtemp" % ( day + 1, ), forecast[ 7 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dpreciptitle" % ( day + 1, ), forecast[ 8 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dprecip" % ( day + 1, ), forecast[ 9 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dwindtitle" % ( day + 1, ), forecast[ 10 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dwind" % ( day + 1, ), forecast[ 11 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%duvtitle" % ( day + 1, ), forecast[ 12 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%duv" % ( day + 1, ), forecast[ 13 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dhumiditytitle" % ( day + 1, ), forecast[ 14 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dhumidity" % ( day + 1, ), forecast[ 15 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dsunrisetitle" % ( day + 1, ), forecast[ 16 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dsunrise" % ( day + 1, ), forecast[ 17 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dsunsettitle" % ( day + 1, ), forecast[ 18 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dsunset" % ( day + 1, ), forecast[ 19 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%doutlook" % ( day + 1, ), forecast[ 20 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobserved" % ( day + 1, ), forecast[ 21 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedpreciptitle" % ( day + 1, ), forecast[ 22 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedprecip" % ( day + 1, ), forecast[ 23 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedavghightitle" % ( day + 1, ), forecast[ 24 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedavghigh" % ( day + 1, ), forecast[ 25 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedavglowtitle" % ( day + 1, ), forecast[ 26 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedavglow" % ( day + 1, ), forecast[ 27 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedrecordhightitle" % ( day + 1, ), forecast[ 28 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedrecordhigh" % ( day + 1, ), forecast[ 29 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedrecordlowtitle" % ( day + 1, ), forecast[ 30 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dobservedrecordlow" % ( day + 1, ), forecast[ 31 ] )
                ##self.CURRENT_WINDOW.setProperty( "Weekend%dalert" % ( day + 1, ), forecast[ 32 ] )
                self.CURRENT_WINDOW.setProperty( "Weekend%dday" % ( day + 1, ), forecast[ 0 ] )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _fetch_10day_forecast( self ):
        # fetch hour by hour forecast
        alerts, alertscolor, alertscount, headings, forecasts = self.TWCClient.fetch_10day_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # set any alerts
            self._set_alerts( alerts, alertscolor, alertscount )
            # reset list
            self.getControl( self.CONTROL_10DAY_LIST ).reset()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                self.CURRENT_WINDOW.setProperty( "10DayHead%d" % ( count + 1, ), heading.strip() )
            # enumerate thru and set the info
            for forecast in forecasts:
                listitem = xbmcgui.ListItem( forecast[ 0 ] )
                listitem.setProperty( "date", forecast[ 1 ] )
                listitem.setProperty( "icon", forecast[ 2 ] )
                listitem.setProperty( "brief", forecast[ 3 ].replace( " / ", "/" ).replace( " ", "\n" ).replace( "/", " /\n" ) )
                listitem.setProperty( "high", forecast[ 4 ] )
                listitem.setProperty( "low", forecast[ 5 ] )
                listitem.setProperty( "precip", forecast[ 6 ] )
                listitem.setProperty( "wind", forecast[ 7 ] )
                listitem.setProperty( "speed", forecast[ 8 ] )
                self.getControl( self.CONTROL_10DAY_LIST ).addItem( listitem )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _toggle_map( self ):
        # toggle map
        self.toggle = not self.toggle
        # set the proper property
        self.CURRENT_WINDOW.setProperty( "Toggle", ( "zoomed", "", )[ self.toggle ] )

    def _toggle_weekend( self ):
        # toggle map
        self.weekendToggle = not self.weekendToggle
        # set the proper property
        self.CURRENT_WINDOW.setProperty( "WeekendToggle", ( "", "details", )[ self.weekendToggle ] )

    def _get_default_view( self ):
        # get our default view
        defaultview = xbmc.getInfoLabel( "Skin.String(twc-defaultview)" )
        self.defaultview = { "": self.CONTROL_MAP_BUTTON,
                                    "200": self.CONTROL_MAP_BUTTON,
                                    "201": self.CONTROL_36HOUR_BUTTON,
                                    "202": self.CONTROL_HOURBYHOUR_BUTTON,
                                    "203": self.CONTROL_WEEKEND_BUTTON,
                                    "204": self.CONTROL_10DAY_BUTTON,
                                    }[ defaultview ]

    def _set_default_view( self ):
        if ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),200)" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultmap,%s)" % ( self.getControl( self.current_maplist ).getListItem( self.current_map ).getLabel(), ) )
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,200)" )
        elif ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),201)" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,201)" )
        elif ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),202)" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,202)" )
        elif ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),203)" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,203)" )
        elif ( xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),204)" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,204)" )
        # necessary sleep to give Skin.String() time to update
        xbmc.sleep( 30 )
        # called so no duplicate code for setting proper self.defaultview value
        self._get_default_view()
        # set our new info
        self._set_script_info()

    def _toggle_animated_setting( self ):
        xbmc.executebuiltin( "Skin.ToggleSetting(twc-animated)" )

    def _toggle_metric_setting( self ):
        xbmc.executebuiltin( "Skin.ToggleSetting(twc-metric)" )
        # get our new TWCClient
        self._get_client()
        # clear cache
        self.TWCClient.clear_cache()
        # reset our view status
        self._init_view_status()
        # clear forecast visible properties
        self._clear_forecasts()
        # we check 36 hour as it holds any alerts
        self._fetch_36_forecast( False )

    def _clear_forecasts( self ):
        # we reset these so old info does not show when user changes metric/english setting
        self.CURRENT_WINDOW.clearProperty( "36Hour1title" )
        self.CURRENT_WINDOW.clearProperty( "HBHHead1" )
        self.CURRENT_WINDOW.clearProperty( "Weekend1day" )
        self.CURRENT_WINDOW.clearProperty( "10DayHead1" )

    def _toggle_show_alerts( self ):
        xbmc.executebuiltin( "Skin.ToggleSetting(twc-show-alerts)" )

    def _choose_map_list( self, maplist ):
        dialog = xbmcgui.Dialog()
        choice = dialog.select( _( 450 ), [ title for title, url, tabtitle in self.TWCClient.BASE_MAPS ] )
        if ( choice != -1 ):
            xbmc.executebuiltin( "Skin.SetString(twc-maplist%d-category,%s)" % ( maplist - 402, self.TWCClient.BASE_MAPS[ choice ][ 0 ], ) )
            xbmc.executebuiltin( "Skin.SetString(twc-maplist%d-title,%s)" % ( maplist - 402, self.TWCClient.BASE_MAPS[ choice ][ 2 ], ) )
            self.current_map = None
            self._fetch_map_list()

    def exit_script( self ):
        # cancel any timer
        if ( self.timer is not None ):
            self.timer.cancel()
        # TODO: remove this if dialogs get properties
        # we call this as dialogs do not support properties
        self.CURRENT_WINDOW.clearProperties()
        # close dialog
        self.close()

    def onClick( self, controlId ):
        if ( controlId == self.CONTROL_MAP_TOGGLE_BUTTON ):
            self._toggle_map()
        elif ( self.toggle ):
            if ( controlId in self.CONTROL_MAP_LISTS and not self.loading ):
                self._fetch_map( self.getControl( controlId ).getSelectedPosition(), controlId )
            elif ( controlId == self.CONTROL_MAP_BUTTON ):
                self._fetch_map_list()
            elif ( controlId == self.CONTROL_36HOUR_BUTTON ):
                self._fetch_36_forecast()
            elif ( controlId == self.CONTROL_HOURBYHOUR_BUTTON ):
                self._fetch_hour_forecast()
            elif ( controlId == self.CONTROL_WEEKEND_BUTTON ):
                self._fetch_weekend_forecast()
            elif ( controlId == self.CONTROL_10DAY_BUTTON ):
                self._fetch_10day_forecast()
            elif ( controlId == self.CONTROL_WEEKEND_TOGGLE_BUTTON ):
                self._toggle_weekend()
            elif ( controlId == self.CONTROL_ANIMATED_SETTING_BUTTON ):
                self._toggle_animated_setting()
            elif ( controlId == self.CONTROL_METRIC_SETTING_BUTTON ):
                self._toggle_metric_setting()
            elif ( controlId == self.CONTROL_SHOW_ALERTS_SETTING_BUTTON ):
                self._toggle_show_alerts()
            elif ( controlId in self.CONTROL_MAPS_LIST_SETTING_BUTTONS ):
                self._choose_map_list( controlId )

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        # this try block is needed to not spam the log window with errors about no focusable item, when using a mouse
        try:
            # convert action to an id number
            actionId = action.getId()
            # perform action
            if ( actionId in self.ACTION_EXIT_SCRIPT and not self.loading ):
                self.exit_script()
            elif ( actionId in self.ACTION_TOGGLE_MAP and xbmc.getCondVisibility( "StringCompare(Window.Property(CurrentView),200)" ) ):
                self._toggle_map()
            elif ( actionId in self.ACTION_SET_DEFAULT and self.toggle ):
                self._set_default_view()
        except:
            pass
