"""
    GUI for displaying maps and forecasts from weather.com
    
    Nuka1195
"""

# main imports
import xbmc
import xbmcgui

from threading import Timer

import resources.lib.TWCClient as TWCClient


class GUI( xbmcgui.WindowXMLDialog ):
    # constants
    ACTION_EXIT_SCRIPT = ( 10, )
    ACTION_SET_DEFAULT = ( 117, )
    ACTION_TOGGLE_MAP = ( 18, )
    # required control id's
    CONTROL_MAP_LIST = 500
    CONTROL_HOUR_LIST = 600
    CONTROL_10DAY_LIST = 700
    # buttons
    CONTROL_MAP_BUTTON = 200
    CONTROL_36HOUR_BUTTON = 201
    CONTROL_HOURBYHOUR_BUTTON = 202
    CONTROL_WEEKEND_BUTTON = 203
    CONTROL_10DAY_BUTTON = 204
    CONTROL_WEEKEND_TOGGLE_BUTTON = 300
    CONTROL_MAP_TOGGLE_BUTTON = 301

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        # set our defaults
        self._init_defaults()
        # get default view
        self._get_default_view()
        # set the maps path
        self._set_maps_path()
        # get our local code, needed for localizing radars
        self._get_local_code()
        # setup our radar client
        self.TWCClient = TWCClient.TWCClient( self.local_code )

    def onInit( self ):
        if ( self.defaultview == "36Hour" ):
            # get our 36 hour forecast
            self._fetch_36_forecast()
        elif ( self.defaultview == "HourByHour" ):
            # get our hour by hour forecast
            self._fetch_hour_forecast()
        elif ( self.defaultview == "Weekend" ):
            # get our hour by hour forecast
            self._fetch_weekend_forecast()
        elif ( self.defaultview == "10Day" ):
            # get our hour by hour forecast
            self._fetch_10day_forecast()
        else:
            # set map list and get default map
            self._fetch_map_list()

    def _init_defaults( self ):
        self.timer = None
        self.toggle = True
        self.weekendToggle = False
        self.loading = False
        self.maps_path = False
        self.current_map = None
        self.forecast36Hour = None
        self.forecastHourByHour = None
        self.forecastWeekend = None
        self.forecast10Day = None

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
            # enumerate thru our map list and add map and title and check for default
            for count, map in enumerate( map_list ):
                # create our listitem, label 2 is not visible (in default skin)
                listitem = xbmcgui.ListItem( map[ 1 ], map [ 0 ] )
                # if we have a match, set our class variable
                if ( map[ 1 ] == default ):
                    self.current_map = count
                # add map to our list
                self.getControl( self.CONTROL_MAP_LIST ).addItem( listitem )
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
        if ( xbmc.getCondVisibility( "IsEmpty(Container(50).Property(view-Maps))" ) ):
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

    def _fetch_36_forecast( self ):
        # reset our view
        self._reset_views( 1 )
        # only run this once
        if ( self.forecast36Hour is None ):
            self.forecast36Hour = True
            # fetch 36 hour forecast
            forecasts = self.TWCClient.fetch_36_forecast()
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                self.setProperty( "36Hour%dtitle" % ( day + 1, ), forecast[ 0 ] )
                self.setProperty( "36Hour%dicon" % ( day + 1, ), forecast[ 1 ] )
                self.setProperty( "36Hour%dbrief" % ( day + 1, ), forecast[ 2 ] )
                self.setProperty( "36Hour%dtemptitle" % ( day + 1, ), forecast[ 3 ] )
                self.setProperty( "36Hour%dtemp" % ( day + 1, ), forecast[ 4 ] )
                self.setProperty( "36Hour%dpreciptitle" % ( day + 1, ), forecast[ 5 ] )
                self.setProperty( "36Hour%dprecip" % ( day + 1, ), forecast[ 6 ] )
                self.setProperty( "36Hour%doutlook" % ( day + 1, ), forecast[ 7 ] )
                self.setProperty( "36Hour%ddaylight" % ( day + 1, ), forecast[ 8 ] )

    def _fetch_hour_forecast( self ):
        # reset our view
        self._reset_views( 2 )
        # only run this once
        if ( self.forecastHourByHour is None ):
            self.forecastHourByHour = True
            # fetch hour by hour forecast
            headings, forecasts = self.TWCClient.fetch_hour_forecast()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                self.setProperty( "HBHHead%d" % ( count + 1, ), heading )
            # enumerate thru and set the info
            for forecast in forecasts:
                listitem = xbmcgui.ListItem( forecast[ 0 ] )
                listitem.setProperty( "icon", forecast[ 1 ] )
                listitem.setProperty( "brief", forecast[ 2 ] )
                listitem.setProperty( "temp", forecast[ 3 ] )
                listitem.setProperty( "feels", forecast[ 4 ] )
                listitem.setProperty( "precip", forecast[ 5 ] )
                listitem.setProperty( "dew", forecast[ 6 ] )
                listitem.setProperty( "humidity", forecast[ 7 ] )
                listitem.setProperty( "wind", forecast[ 8 ] )
                self.getControl( self.CONTROL_HOUR_LIST ).addItem( listitem )

    def _fetch_weekend_forecast( self ):
        # reset our view
        self._reset_views( 3 )
        # only run this once
        if ( self.forecastWeekend is None ):
            self.forecastWeekend = True
            # fetch 36 hour forecast
            forecasts = self.TWCClient.fetch_weekend_forecast()
            # enumerate thru and set the info
            for day, forecast in enumerate( forecasts ):
                self.setProperty( "Weekend%dday" % ( day + 1, ), forecast[ 0 ] )
                self.setProperty( "Weekend%ddate" % ( day + 1, ), forecast[ 1 ] )
                self.setProperty( "Weekend%dicon" % ( day + 1, ), forecast[ 2 ] )
                self.setProperty( "Weekend%dbrief" % ( day + 1, ), forecast[ 3 ] )
                self.setProperty( "Weekend%dhightitle" % ( day + 1, ), forecast[ 4 ] )
                self.setProperty( "Weekend%dhightemp" % ( day + 1, ), forecast[ 5 ] )
                self.setProperty( "Weekend%dlowtitle" % ( day + 1, ), forecast[ 6 ] )
                self.setProperty( "Weekend%dlowtemp" % ( day + 1, ), forecast[ 7 ] )
                self.setProperty( "Weekend%dpreciptitle" % ( day + 1, ), forecast[ 8 ] )
                self.setProperty( "Weekend%dprecip" % ( day + 1, ), forecast[ 9 ] )
                self.setProperty( "Weekend%dwindtitle" % ( day + 1, ), forecast[ 10 ] )
                self.setProperty( "Weekend%dwind" % ( day + 1, ), forecast[ 11 ] )
                self.setProperty( "Weekend%duvtitle" % ( day + 1, ), forecast[ 12 ] )
                self.setProperty( "Weekend%duv" % ( day + 1, ), forecast[ 13 ] )
                self.setProperty( "Weekend%dhumiditytitle" % ( day + 1, ), forecast[ 14 ] )
                self.setProperty( "Weekend%dhumidity" % ( day + 1, ), forecast[ 15 ] )
                self.setProperty( "Weekend%dsunrisetitle" % ( day + 1, ), forecast[ 16 ] )
                self.setProperty( "Weekend%dsunrise" % ( day + 1, ), forecast[ 17 ] )
                self.setProperty( "Weekend%dsunsettitle" % ( day + 1, ), forecast[ 18 ] )
                self.setProperty( "Weekend%dsunset" % ( day + 1, ), forecast[ 19 ] )
                self.setProperty( "Weekend%doutlook" % ( day + 1, ), forecast[ 20 ] )
                self.setProperty( "Weekend%dobserved" % ( day + 1, ), forecast[ 21 ] )

    def _fetch_10day_forecast( self ):
        # reset our view
        self._reset_views( 4 )
        # only run this once
        if ( self.forecast10Day is None ):
            self.forecast10Day = True
            # fetch hour by hour forecast
            headings, forecasts = self.TWCClient.fetch_10day_forecast()
            # enumerate thru and set our heading properties
            for count, heading in enumerate( headings ):
                self.setProperty( "10DayHead%d" % ( count + 1, ), heading.strip() )
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

    def _toggle_map( self ):
        # toggle map
        self.toggle = not self.toggle
        # set the proper property
        self.setProperty( "Toggle", ( "zoomed", "", )[ self.toggle ] )

    def _toggle_weekend( self ):
        # toggle map
        self.weekendToggle = not self.weekendToggle
        # set the proper property
        self.setProperty( "WeekendToggle", ( "", "details", )[ self.weekendToggle ] )

    def _reset_views( self, view=0 ):
        self.setProperty( "view-Maps", ( "", "viewing", )[ view == 0 ] )
        self.setProperty( "view-36Hour", ( "", "viewing", )[ view == 1 ] )
        self.setProperty( "view-HourByHour", ( "", "viewing", )[ view == 2 ] )
        self.setProperty( "view-Weekend", ( "", "viewing", )[ view == 3 ] )
        self.setProperty( "view-10Day", ( "", "viewing", )[ view == 4 ] )

    def _get_default_view( self ):
        # get our default view
        self.defaultview = xbmc.getInfoLabel( "Skin.String(twc-defaultview)" )
        view = { "": 0, "Maps": 0, "36Hour": 1, "HourByHour": 2, "Weekend": 3, "10Day": 4 }[ self.defaultview ]
        # reset the view
        self._reset_views( view )

    def _set_default_view( self ):
        if ( xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-Maps))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultmap,%s)" % ( self.getControl( self.CONTROL_MAP_LIST ).getSelectedItem().getLabel(), ) )
            xbmc.executebuiltin( "Skin.Reset(twc-defaultview)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-36Hour))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,36Hour)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-HourByHour))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,HourByHour)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-Weekend))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,Weekend)" )
        elif ( xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-10Day))" ) ):
            xbmc.executebuiltin( "Skin.SetString(twc-defaultview,10Day)" )

    def exit_script( self ):
        if ( self.timer is not None ):
            self.timer.cancel()
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

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        # convert action to an id number
        actionId = action.getId()
        # perform action
        if ( actionId in self.ACTION_EXIT_SCRIPT and not self.loading ):
            self.exit_script()
        elif ( actionId in self.ACTION_TOGGLE_MAP and xbmc.getCondVisibility( "!IsEmpty(Container(50).Property(view-Maps))" ) ):
            self._toggle_map()
        elif ( actionId in self.ACTION_SET_DEFAULT and self.toggle ):
            self._set_default_view()
