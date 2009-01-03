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
    CONTROL_MAP_LIST = 500
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
    # settings buttons
    CONTROL_ANIMATED_SETTING_BUTTON = 400
    CONTROL_METRIC_SETTING_BUTTON = 401
    CONTROL_FANART_SETTING_BUTTON = 402
    CONTROL_FANART_DIFFUSE_SETTING_BUTTON = 403
    CONTROL_FANART_TYPE_SETTING_BUTTON = 404

    def __init__( self, *args, **kwargs ):
        module.__init__( self, *args, **kwargs )
        # reset views
        self._reset_views( 0 )
        # set our defaults
        self._init_defaults()
        self._init_view_status()
        # get default view
        self._get_default_view()
        # set the maps path
        self._set_maps_path()
        # get our local code, needed for localizing radars
        self._get_local_code()
        # get our new TWCClient
        self._get_client()

    def onInit( self ):
        dialog.close()
        # set script info
        self._set_script_info()
        # set default fanart diffuse level
        self._set_diffuse_level()
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
        elif ( self.defaultview == self.CONTROL_ALERTS_BUTTON ):
            # get our alerts
            self._show_alerts()
        else:
            # set map list and get default map
            self._fetch_map_list()
        # we check 36 hour as it holds any alerts
        if ( self.defaultview != self.CONTROL_36HOUR_BUTTON and self.defaultview != self.CONTROL_ALERTS_BUTTON ):
            self._fetch_36_forecast( False )

    def _init_defaults( self ):
        self.timer = None
        self.toggle = True
        self.weekendToggle = False
        self.loading = False
        self.maps_path = False
        self.current_map = None

    def _set_script_info( self ):
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "version", "%s - %s" % ( sys.modules[ "__main__" ].__version__, str( sys.modules[ "__main__" ].__svn_revision__ ) ) )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "author", sys.modules[ "__main__" ].__author__ )
        if ( self.defaultview == self.CONTROL_MAP_BUTTON ):
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "defaultview", "%s - %s" % ( _( self.defaultview ), xbmc.getInfoLabel( "Skin.String(twc-defaultmap)" ), ) )
        else:
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "defaultview", _( self.defaultview ) )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "svnurl", sys.modules[ "__main__" ].__url__ )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "scripturl", sys.modules[ "__main__" ].__svn_url__ )

    def _init_view_status( self ):
        self.forecast36Hour = None
        self.forecastHourByHour = None
        self.forecastWeekend = None
        self.forecast10Day = None

    def _get_client( self ):
        # setup our radar client
        self.TWCClient = TWCClient.TWCClient( self.local_code )

    def _get_local_code( self ):
        try:
            t = 0
            while t < 5:
                # grab the current location
                location = xbmc.getInfoLabel( "Weather.Location" )
                # if successful break out of loop
                if ( location.lower() != "busy" ):
                    break
                t += 1
                xbmc.sleep( 500 )
            # loop thru and compare location with the three saved locations
            for count in range( 1, 4 ):
                # grab a saved location
                preset = xbmc.executehttpapi( "getguisetting(3,weather.areacode%d)" % ( count, ) ).replace( "<li>", "" )
                # if location is same as saved location, we have our local code
                if ( preset.split( " - " )[ 1 ] == location ):
                    self.local_code = preset.split( " - " )[ 0 ]
                    break
        except Exception, e:
            print str( e )

    def _set_maps_path( self, path=0 ):
        if ( path == 0 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,weather.com/loading)" )
        elif ( path == 1 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,%s)" % ( self.maps_path, ) )
        elif ( path == 2 ):
            xbmc.executebuiltin( "Skin.SetString(twc-mapspath,weather.com/default)" )

    def _fetch_map_list( self ):
        # reset our view
        self._reset_views()
        # only run this once
        if ( self.current_map is None ):
            # initialize current map
            self.current_map = 0
            # get the users default map
            default = xbmc.getInfoLabel( "Skin.String(twc-defaultmap)" )
            # fetch map list
            map_list = self.TWCClient.fetch_map_list()
            # lock the gui for faster updating
            xbmcgui.lock()
            try:
                # enumerate thru our map list and add map and title and check for default
                for count, map in enumerate( map_list ):
                    # create our listitem, label 2 is not visible (in default skin)
                    listitem = xbmcgui.ListItem( map[ 1 ], map [ 0 ] )
                    # if we have a match, set our class variable
                    if ( map[ 1 ] == default ):
                        self.current_map = count
                    # add map to our list
                    self.getControl( self.CONTROL_MAP_LIST ).addItem( listitem )
            except:
                pass
            # unlock the gui
            xbmcgui.unlock()
        # fetch our map
        self._fetch_map( self.current_map )

    def _fetch_map( self, map ):
        # set the current map
        self.current_map = map
        # cancel any timer
        if ( self.timer is not None ):
            self.timer.cancel()
            self.timer = None
        # do not refresh map if not current view
        if ( xbmc.getCondVisibility( "IsEmpty(Window.Property(view-Maps))" ) ):
            return
        # get maps url name
        map = self.getControl( self.CONTROL_MAP_LIST ).getListItem( map ).getLabel2()
        # make sure user can't keep selecting maps
        self.loading = True
        # we set our skin setting to defaultimages while downloading
        self._set_maps_path()
        # fetch the available map urls
        maps = self.TWCClient.fetch_map_urls( map )
        # fetch the images
        self.maps_path, expires = self.TWCClient.fetch_images( maps )
        # now set our skin string so multi image will display images 1==success, 2==failure
        self._set_maps_path( ( self.maps_path == "" ) + 1 )
        # successful so set timer thread
        if ( self.maps_path != "" and expires > 0 ):
            self.timer = Timer( expires, self._fetch_map,( self.current_map, ) )
            self.timer.start()
        # reset loading status
        self.loading = False

    def _fetch_36_forecast( self, showView=True ):
        # reset our view
        if ( showView ):
            self._reset_views( self.CONTROL_36HOUR_BUTTON )
        # fetch 36 hour forecast
        alerts, alertscolor, forecasts = self.TWCClient.fetch_36_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        # set any alerts
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Alerts", alerts )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "AlertsColor", alertscolor )
        try:
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dicon" % ( day + 1, ), forecast[ 1 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dbrief" % ( day + 1, ), forecast[ 2 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dtemptitle" % ( day + 1, ), forecast[ 3 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dtemp" % ( day + 1, ), forecast[ 4 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dpreciptitle" % ( day + 1, ), forecast[ 5 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dprecip" % ( day + 1, ), forecast[ 6 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%doutlook" % ( day + 1, ), forecast[ 7 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%ddaylight" % ( day + 1, ), forecast[ 8 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour%dtitle" % ( day + 1, ), forecast[ 0 ] )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _fetch_hour_forecast( self ):
        # reset our view
        self._reset_views( self.CONTROL_HOURBYHOUR_BUTTON )
        # fetch hour by hour forecast
        headings, forecasts = self.TWCClient.fetch_hour_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # reset list
            self.getControl( self.CONTROL_HOUR_LIST ).reset()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "HBHHead%d" % ( count + 1, ), heading )
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
        # reset our view
        self._reset_views( self.CONTROL_WEEKEND_BUTTON )
        # fetch 36 hour forecast
        forecasts = self.TWCClient.fetch_weekend_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%ddate" % ( day + 1, ), forecast[ 1 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dicon" % ( day + 1, ), forecast[ 2 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dbrief" % ( day + 1, ), forecast[ 3 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dhightitle" % ( day + 1, ), forecast[ 4 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dhightemp" % ( day + 1, ), forecast[ 5 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dlowtitle" % ( day + 1, ), forecast[ 6 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dlowtemp" % ( day + 1, ), forecast[ 7 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dpreciptitle" % ( day + 1, ), forecast[ 8 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dprecip" % ( day + 1, ), forecast[ 9 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dwindtitle" % ( day + 1, ), forecast[ 10 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dwind" % ( day + 1, ), forecast[ 11 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%duvtitle" % ( day + 1, ), forecast[ 12 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%duv" % ( day + 1, ), forecast[ 13 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dhumiditytitle" % ( day + 1, ), forecast[ 14 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dhumidity" % ( day + 1, ), forecast[ 15 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dsunrisetitle" % ( day + 1, ), forecast[ 16 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dsunrise" % ( day + 1, ), forecast[ 17 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dsunsettitle" % ( day + 1, ), forecast[ 18 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dsunset" % ( day + 1, ), forecast[ 19 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%doutlook" % ( day + 1, ), forecast[ 20 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobserved" % ( day + 1, ), forecast[ 21 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedpreciptitle" % ( day + 1, ), forecast[ 22 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedprecip" % ( day + 1, ), forecast[ 23 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedavghightitle" % ( day + 1, ), forecast[ 24 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedavghigh" % ( day + 1, ), forecast[ 25 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedavglowtitle" % ( day + 1, ), forecast[ 26 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedavglow" % ( day + 1, ), forecast[ 27 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedrecordhightitle" % ( day + 1, ), forecast[ 28 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedrecordhigh" % ( day + 1, ), forecast[ 29 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedrecordlowtitle" % ( day + 1, ), forecast[ 30 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dobservedrecordlow" % ( day + 1, ), forecast[ 31 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dalert" % ( day + 1, ), forecast[ 32 ] )
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend%dday" % ( day + 1, ), forecast[ 0 ] )
        except:
            pass
        # unlock the gui
        xbmcgui.unlock()

    def _fetch_10day_forecast( self ):
        # reset our view
        self._reset_views( self.CONTROL_10DAY_BUTTON )
        # fetch hour by hour forecast
        headings, forecasts = self.TWCClient.fetch_10day_forecast()
        # lock the gui for faster updating
        xbmcgui.lock()
        try:
            # reset list
            self.getControl( self.CONTROL_10DAY_LIST ).reset()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "10DayHead%d" % ( count + 1, ), heading.strip() )
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
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Toggle", ( "zoomed", "", )[ self.toggle ] )

    def _toggle_weekend( self ):
        # toggle map
        self.weekendToggle = not self.weekendToggle
        # set the proper property
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "WeekendToggle", ( "", "details", )[ self.weekendToggle ] )

    def _reset_views( self, view=200 ):
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-Maps", ( "", "viewing", )[ view == self.CONTROL_MAP_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-36Hour", ( "", "viewing", )[ view == self.CONTROL_36HOUR_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-HourByHour", ( "", "viewing", )[ view == self.CONTROL_HOURBYHOUR_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-Weekend", ( "", "viewing", )[ view == self.CONTROL_WEEKEND_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-10Day", ( "", "viewing", )[ view == self.CONTROL_10DAY_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-Alerts", ( "", "viewing", )[ view == self.CONTROL_ALERTS_BUTTON ] )
        xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "view-Settings", ( "", "viewing", )[ view == self.CONTROL_SETTINGS_BUTTON ] )

    def _get_default_view( self ):
        # get our default view
        defaultview = xbmc.getInfoLabel( "Skin.String(twc-defaultview)" )
        self.defaultview = { "": self.CONTROL_MAP_BUTTON,
                                    "Maps": self.CONTROL_MAP_BUTTON,
                                    "36Hour": self.CONTROL_36HOUR_BUTTON,
                                    "HourByHour": self.CONTROL_HOURBYHOUR_BUTTON,
                                    "Weekend": self.CONTROL_WEEKEND_BUTTON,
                                    "10Day": self.CONTROL_10DAY_BUTTON,
                                    "Alerts": self.CONTROL_ALERTS_BUTTON
                                    }[ defaultview ]

    def _set_default_view( self ):
        if ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-Maps))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultmap,%s)" % ( self.getControl( self.CONTROL_MAP_LIST ).getListItem( self.current_map ).getLabel(), ) )
            xbmc.executebuiltin( "Skin.Reset(twc-defaultview)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-36Hour))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,36Hour)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-HourByHour))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,HourByHour)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-Weekend))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,Weekend)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-10Day))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,10Day)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-Alerts))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,Alerts)" )
        # necessary sleep to give Skin.String() time to update
        xbmc.sleep(30)
        # called so no duplicate code for setting proper self.defaultview value
        self._get_default_view()
        # set our new info
        self._set_script_info()

    def _show_settings( self ):
        # reset our view
        self._reset_views( self.CONTROL_SETTINGS_BUTTON )

    def _show_alerts( self ):
        # we also check 36 hour as it holds any alerts
        self._fetch_36_forecast( False )
        # we set the deaful view to maps if no alert was found
        if ( xbmc.getCondVisibility( "IsEmpty(Window.Property(Alerts))" ) ):
            self._fetch_map_list()
        else:
            # reset our view
            self._reset_views( self.CONTROL_ALERTS_BUTTON )

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
        # TODO: when a newer xbmc is released, eliminate the except block
        # we reset these so old info does not show when user changes metric/english setting
        try:
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).clearProperty( "36Hour1title" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).clearProperty( "HBHHead1" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).clearProperty( "Weekend1day" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).clearProperty( "10DayHead1" )
        except:
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "36Hour1title", "" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "HBHHead1", "" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "Weekend1day", "" )
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty( "10DayHead1", "" )

    def _set_fanart_path( self ):
        # create the dialog object
        dialog = xbmcgui.Dialog()
        # get the users input
        value = dialog.browse( 0, _( 402 ), "files", "", False, False, xbmc.getInfoLabel( "Skin.String(twc-fanart-path)" ) )
        # set our skin string
        xbmc.executebuiltin( "Skin.SetString(twc-fanart-path,%s)" % ( value, ) )

    def _set_diffuse_level( self, change=0 ):
        # oue fade levels 00FFFFFF is off
        levels = [ "00FFFFFF", "30FFFFFF", "60FFFFFF", "90FFFFFF", "BBFFFFFF", "DDFFFFFF", "FFFFFFFF" ]
        # get previous setting
        diffusecolor = xbmc.getInfoLabel( "Skin.String(twc-fanart-diffusecolor)" )
        # if no previous setting set 60FFFFFF as default (my preference)
        if ( diffusecolor == "" ):
            level = 2
        else:
            level = levels.index( diffusecolor )
        # add the change value
        level += change
        # make sure level is valid
        if ( level == len( levels ) ):
            level = 0
        elif ( level < 0 ):
            level = len( levels ) - 1
        # set our skin setting
        xbmc.executebuiltin( "Skin.SetString(twc-fanart-diffusecolor,%s)" % ( levels[ level ], ) )
        # enumerate thru and set the proper diffuselevel
        for i in range( 7 ):
            # if this is the level we are at, set true
            if ( level == i ):
                xbmc.executebuiltin( "Skin.SetBool(twc-fanart-diffuselevel%d)" % ( i, ) )
            else:
                xbmc.executebuiltin( "Skin.Reset(twc-fanart-diffuselevel%d)" % ( i, ) )

    def _set_fanart_type( self ):
        xbmc.executebuiltin( "Skin.ToggleSetting(twc-fanart-type)" )

    def exit_script( self ):
        # cancel any timer
        if ( self.timer is not None ):
            self.timer.cancel()
        # TODO: remove this when dialogs work properly
        # we call this as dialogs do not properly clear properties.
        try:
            xbmcgui.Window(xbmcgui.getCurrentWindowId()).clearProperties()
        except:
            pass
        # close dialog
        self.close()

    def onClick( self, controlId ):
        if ( controlId == self.CONTROL_MAP_TOGGLE_BUTTON ):
            self._toggle_map()
        elif ( self.toggle ):
            if ( controlId == self.CONTROL_MAP_LIST and not self.loading ):
                self._fetch_map( self.getControl( self.CONTROL_MAP_LIST ).getSelectedPosition() )
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
            elif ( controlId == self.CONTROL_SETTINGS_BUTTON ):
                self._show_settings()
            elif ( controlId == self.CONTROL_ALERTS_BUTTON ):
                self._show_alerts()
            elif ( controlId == self.CONTROL_ANIMATED_SETTING_BUTTON ):
                self._toggle_animated_setting()
            elif ( controlId == self.CONTROL_METRIC_SETTING_BUTTON ):
                self._toggle_metric_setting()
            elif ( controlId == self.CONTROL_FANART_SETTING_BUTTON ):
                self._set_fanart_path()
            elif ( controlId == self.CONTROL_FANART_DIFFUSE_SETTING_BUTTON ):
                self._set_diffuse_level( 1 )
            elif ( controlId == self.CONTROL_FANART_TYPE_SETTING_BUTTON ):
                self._set_fanart_type()

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
            elif ( actionId in self.ACTION_TOGGLE_MAP and xbmc.getCondVisibility( "!IsEmpty(Window.Property(view-Maps))" ) ):
                self._toggle_map()
            elif ( actionId in self.ACTION_SET_DEFAULT and self.toggle ):
                self._set_default_view()
            elif ( actionId in self.ACTION_SET_DEFAULT and self.toggle ):
                self._set_default_view()
            elif ( self.getFocusId() == self.CONTROL_FANART_DIFFUSE_SETTING_BUTTON ):
                if ( actionId in self.ACTION_MOVEMENT_LEFT ):
                    self._set_diffuse_level( -1 )
                elif ( actionId in self.ACTION_MOVEMENT_RIGHT ):
                    self._set_diffuse_level( 1 )
        except:
            pass
