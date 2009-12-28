"""
    GUI for displaying maps and forecasts from weather.com
    
    Nuka1195
"""

# main imports
import sys
import os

import xbmc
import xbmcgui

"""
from threading import Thread
"""

import resources.lib.WeatherClient as WeatherClient


class Main:
    _ = xbmc.Language( os.getcwd() ).getLocalizedString
    Settings = xbmc.Settings( os.getcwd() )

    def __init__( self, *args, **kwargs ):
        # get current window
        self._get_weather_window()
        # get our new WeatherClient
        self._get_client()
        # if user selected a new map, only need to fetch it
        if ( sys.argv[ 1 ].startswith( "map=" ) ):
            # parse sys.argv for params
            params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
            # fetch map (map=%s&title=%s&location=
            self._fetch_map( params[ "map" ], params[ "title" ], params[ "location" ] )
        else:
            # set plugin name property
            self._set_plugin_name()
            # clear key properties if new location
            if ( self.new_location ):
                self._clear_properties()
            # initialize our thread list
            """
            thread_list = []
            # get our 36 hour forecast
            current = FetchInfo( self._fetch_36_forecast )
            thread_list += [ current ]
            current.start()
            # get our hour by hour forecast
            current = FetchInfo( self._fetch_hourly_forecast )
            thread_list += [ current ]
            current.start()
            # get our weekend forecast
            current = FetchInfo( self._fetch_weekend_forecast )
            thread_list += [ current ]
            current.start()
            # get our 10 day forecast
            current = FetchInfo( self._fetch_10day_forecast )
            thread_list += [ current ]
            current.start()
            # get our map list and default map
            current = FetchInfo( self._fetch_map_list )
            thread_list += [ current ]
            current.start()
            # join our threads with the main thread
            for thread in thread_list:
               thread.join()
            """
            self._fetch_map_list()
            self._fetch_36_forecast()
            self._fetch_10day_forecast()
            self._fetch_hourly_forecast()
            self._fetch_weekend_forecast()
        # we're finished, exit
        self._exit_script()

    def _get_weather_window( self ):
        # grab the weather window
        self.WEATHER_WINDOW = xbmcgui.Window( 12600 )

    def _set_plugin_name( self ):
        # set plugin name
        self.WEATHER_WINDOW.setProperty( "PluginName", sys.modules[ "__main__" ].__pluginname__ )

    def _get_client( self ):
        self.settings = { "translate": None }
        if ( self.Settings.getSetting( "translate" ) == "true" ):
            self.settings[ "translate" ] = {
                                        "Chinese (Simple)": "en_zh",
                                        "Chinese (Traditional)": "en_zt",
                                        "Dutch": "en_nl",
                                        "French": "en_fr",
                                        "German": "en_de",
                                        "German (Austria)": "en_de",
                                        "Greek": "en_el",
                                        "Italian": "en_it",
                                        "Japanese": "en_ja",
                                        "Korean": "en_ko",
                                        "Portuguese": "en_pt",
                                        "Portuguese (Brazil)": "en_pt",
                                        "Russian": "en_ru",
                                        "Spanish": "en_es",
                                        "Spanish (Mexico)": "en_es",
                                    }.get( xbmc.getLanguage(), None )
        if ( sys.argv[ 1 ].startswith( "map=" ) ):
            self.areacode = xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" )
        else:
            self.areacode = sys.argv[ 1 ]
        # set if new location
        self.new_location = ( xbmc.getInfoLabel( "Window(Weather).Property(Weather.AreaCode)" ) != self.areacode )
        # if new set it
        if ( self.new_location ):
            self.WEATHER_WINDOW.setProperty( "Weather.AreaCode", self.areacode )
        # setup our radar client
        self.WeatherClient = WeatherClient.WeatherClient( self.areacode, self.settings[ "translate" ] )

    def _set_maps_path( self, path=0, maps_path="", legend_path="" ):
        # we have three possibilities. loading, default (error) or the actual map path
        if ( path == 0 ):
            self.WEATHER_WINDOW.setProperty( "MapStatus", "loading" )
            self.WEATHER_WINDOW.setProperty( "MapPath", "weather.com plus/loading" )
            self.WEATHER_WINDOW.setProperty( "LegendPath", "" )
        elif ( path == 1 ):
            self.WEATHER_WINDOW.setProperty( "MapStatus", "loaded" )
            self.WEATHER_WINDOW.setProperty( "MapPath", maps_path )
            self.WEATHER_WINDOW.setProperty( "LegendPath", legend_path )
        elif ( path == 2 ):
            self.WEATHER_WINDOW.setProperty( "MapStatus", "error" )
            self.WEATHER_WINDOW.setProperty( "MapPath", "weather.com plus/error" )
            self.WEATHER_WINDOW.setProperty( "LegendPath", "" )

    def _clear_properties( self ):
        # alerts
        self.WEATHER_WINDOW.clearProperty( "Alerts" )
        self.WEATHER_WINDOW.setProperty( "Alerts.Color", "default" )
        # video
        self.WEATHER_WINDOW.clearProperty( "Video" )
        # 36 Hour
        self.WEATHER_WINDOW.clearProperty( "36Hour.1.Heading" )
        self.WEATHER_WINDOW.clearProperty( "36Hour.2.Heading" )
        self.WEATHER_WINDOW.clearProperty( "36Hour.3.Heading" )
        # Weekend
        self.WEATHER_WINDOW.clearProperty( "Weekend.1.Date" )
        self.WEATHER_WINDOW.clearProperty( "Weekend.2.Date" )
        self.WEATHER_WINDOW.clearProperty( "Weekend.3.Date" )
        # 10-Day
        self.WEATHER_WINDOW.clearProperty( "Daily.Heading1" )
        # Hourly
        self.WEATHER_WINDOW.clearProperty( "Hourly.Heading1" )

    def _clear_map_list( self, list_id ):
        # enumerate thru and clear all map list labels, icons and onclicks
        for count in range( 1, 31 ):
            # these are what the user sees and the action the button performs
            self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapLabel.%d" % ( list_id, count, ) )
            self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapLabel2.%d" % ( list_id, count, ) )
            self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapIcon.%d" % ( list_id, count, ) )
            self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapOnclick.%d" % ( list_id, count, ) )
        # set the default titles
        self._set_map_list_titles( list_id )

    def _set_map_list_titles( self, list_id, title=None, long_title=None ):
        # set map list titles for skinners buttons
        if ( title is None ):
            # non user defined list
            title = ( "", self._( 32800 + int( self.Settings.getSetting( "maplist%d" % ( list_id, ) ) ) ), )[ int( self.Settings.getSetting( "maplist%d" % ( list_id, ) ) ) > 0 ]
            long_title = self._( 32600 + int( self.Settings.getSetting( "maplist%d" % ( list_id, ) ) ) )
        # now set the titles
        self.WEATHER_WINDOW.setProperty( "MapList.%d.ShortTitle" % ( list_id, ), title )
        self.WEATHER_WINDOW.setProperty( "MapList.%d.LongTitle" % ( list_id, ), long_title )

    def _fetch_map_list( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # intialize our download variable, we use this so we don't re-download same info
        map_download = []
        # enumerate thru and clear our properties if map is different (if user changed setiings), local and user defined list should be downloaded if location changed
        for count in range( 1, 4 ):
            # do we need to download this list?
            map_download += [ ( self.new_location and int( self.Settings.getSetting( "maplist%d" % ( count, ) ) ) == 1 ) or 
                                            ( self.new_location and int( self.Settings.getSetting( "maplist%d" % ( count, ) ) ) == len( self.WeatherClient.BASE_MAPS ) - 1 ) or 
                                            ( self.WEATHER_WINDOW.getProperty( "MapList.%d.LongTitle" % ( count, ) ) != self._( 32600 + int( self.Settings.getSetting( "maplist%d" % ( count, ) ) ) ) ) ]
            # do we need to clear the info?
            if ( map_download[ count - 1 ] ):
                self._clear_map_list( count )
        # we set this here in case we do not need to download new lists
        current_map = self.WEATHER_WINDOW.getProperty( "Weather.CurrentMapUrl" )
        current_map_title = self.WEATHER_WINDOW.getProperty( "Weather.CurrentMap" )
        # only run if any new map lists
        if ( True in map_download ):
            # we set our maps path property to loading images while downloading
            self._set_maps_path()
            # set default map, we allow skinners to have users set this with a skin string
            # TODO: look at this, seems wrong, when changing locations maps can fail to load.
            default = ( self.WEATHER_WINDOW.getProperty( "Weather.CurrentMap" ), xbmc.getInfoLabel( "Skin.String(TWC.DefaultMap)" ), )[ xbmc.getInfoLabel( "Skin.String(TWC.DefaultMap)" ) != "" and self.WEATHER_WINDOW.getProperty( "Weather.CurrentMap" ) == "" ]
            # enumurate thru map lists and fetch map list
            for maplist_count in range( 1, 4 ):
                # only fetch new list if required
                if ( not map_download[ maplist_count - 1 ] ):
                    continue
                # get the correct category
                map_category = int( self.Settings.getSetting( "maplist%d" % ( maplist_count, ) ) )
                # fetch map list
                category_title, maps = self.WeatherClient.fetch_map_list( map_category, self.Settings.getSetting( "maplist_user_file" ), xbmc.getInfoLabel( "Window(Weather).Property(LocationIndex)" ) )
                # only run if maps were found
                if ( maps is None ):
                    continue
                # set a current_map in case one isn't set
                if ( current_map == "" ):
                    current_map = maps[ 0 ][ 0 ]
                    current_map_title = maps[ 0 ][ 1 ]
                # if user defined map list set the new titles
                if ( category_title is not None ):
                    self._set_map_list_titles( maplist_count, category_title, category_title )
                # enumerate thru our map list and add map and title and check for default
                for count, map in enumerate( maps ):
                    # create our label, icon and onclick event
                    self.WEATHER_WINDOW.setProperty( "MapList.%d.MapLabel.%d" % ( maplist_count, count + 1, ), map[ 1 ] )
                    self.WEATHER_WINDOW.setProperty( "MapList.%d.MapLabel2.%d" % ( maplist_count, count + 1, ), map[ 0 ] )
                    self.WEATHER_WINDOW.setProperty( "MapList.%d.MapIcon.%d" % ( maplist_count, count + 1, ), map[ 1 ].replace( ":", " -" ).replace( "/", " - " ) + ".jpg" )
                    self.WEATHER_WINDOW.setProperty( "MapList.%d.MapOnclick.%d" % ( maplist_count, count + 1, ), "XBMC.RunScript(%s,map=%s&title=%s&location=%s)" % ( sys.argv[ 0 ], map[ 0 ], map[ 1 ], str( map[ 2 ] ) ) )
                    # if we have a match, set our class variable
                    if ( map[ 1 ] == default ):
                        current_map = map[ 0 ]
                        current_map_title = map[ 1 ]
        # fetch the current map
        self._fetch_map( current_map, current_map_title, xbmc.getInfoLabel( "Window(Weather).Property(LocationIndex)" ) )

    def _fetch_map( self, map, title, locationindex=None ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # we set our maps path property to loading images while downloading
        self._set_maps_path()
        # we set Weather.CurrentMap and Weather.CurrentMapUrl, the skin can handle it when the user selects a new map for immediate update
        self.WEATHER_WINDOW.setProperty( "Weather.CurrentMap", title )
        self.WEATHER_WINDOW.setProperty( "Weather.CurrentMapUrl", map )
        # fetch the available map urls
        maps = self.WeatherClient.fetch_map_urls( map, self.Settings.getSetting( "maplist_user_file" ), locationindex )
        # fetch the images
        maps_path, legend_path = self.WeatherClient.fetch_images( maps )
        # hack incase the weather in motion link was bogus
        if ( maps_path == "" and len( maps[ 1 ] ) ):
            maps_path, legend_path = self.WeatherClient.fetch_images( ( maps[ 0 ], [], maps[ 2 ], ) )
        # now set our window properties so multi image will display images 1==success, 2==failure
        self._set_maps_path( ( maps_path == "" ) + 1, maps_path, legend_path )

    def _set_alerts( self, alerts, alertsrss, alertsnotify, alertscolor, alertscount ):
        # send notification if user preference and there are alerts
        if ( int( self.Settings.getSetting( "alert_notify" ) ) > 0 and alerts != "" and ( self.Settings.getSetting( "alert_notify_once" ) == "false"
            or self.WEATHER_WINDOW.getProperty( "Alerts.RSS" ) != alertsrss )
            ):
            xbmc.executebuiltin( "XBMC.Notification(%s,\"%s\",%d,weather.com plus/alert-%s.png)" % ( self._( 32100 ), alertsnotify, ( 0, 10, 20, 30, 45, 60, 120, 300, 600, )[ int( self.Settings.getSetting( "alert_notify" ) ) ] * 1000, alertscolor, ) )
        # set any alerts
        self.WEATHER_WINDOW.setProperty( "Alerts", alerts )
        self.WEATHER_WINDOW.setProperty( "Alerts.RSS", alertsrss )
        self.WEATHER_WINDOW.setProperty( "Alerts.Color", ( "default", alertscolor, )[ alerts != "" ] )
        self.WEATHER_WINDOW.setProperty( "Alerts.Count", ( "", str( alertscount ), )[ alertscount > 1 ] )
        self.WEATHER_WINDOW.setProperty( "Alerts.Label", xbmc.getLocalizedString( 33049 + ( alertscount > 1 ) ) )

    def _set_video( self, video_url ):
        self.WEATHER_WINDOW.setProperty( "Video", video_url )

    def _fetch_36_forecast( self, showView=True ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # fetch 36 hour forecast
        alerts, alertsrss, alertsnotify, alertscolor, alertscount, forecasts, video = self.WeatherClient.fetch_36_forecast( self.WEATHER_WINDOW.getProperty( "Video" ) )
        # set any alerts
        self._set_alerts( alerts, alertsrss, alertsnotify, alertscolor, alertscount )
        # set video
        self._set_video( video )
        # enumerate thru and set the info
        for day, forecast in enumerate( forecasts ):
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.OutlookIcon" % ( day + 1, ), forecast[ 1 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.FanartCode" % ( day + 1, ), os.path.splitext( os.path.basename( forecast[ 1 ] ) )[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Outlook" % ( day + 1, ), forecast[ 2 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.TemperatureColor" % ( day + 1, ), forecast[ 3 ].lower() )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.TemperatureHeading" % ( day + 1, ), ( xbmc.getLocalizedString( 393 ), xbmc.getLocalizedString( 391 ), )[ forecast[ 3 ] == "Low" ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Temperature" % ( day + 1, ), forecast[ 4 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Precipitation" % ( day + 1, ), forecast[ 6 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Forecast" % ( day + 1, ), forecast[ 7 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.DaylightTitle" % ( day + 1, ), forecast[ 8 ].replace( "Sunrise", xbmc.getLocalizedString( 33027 ) ).replace( "Sunset", xbmc.getLocalizedString( 33028 ) ) )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.DaylightTime" % ( day + 1, ), forecast[ 9 ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.DaylightType" % ( day + 1, ), ( "sunrise", "sunset", )[ forecast[ 8 ] == "Sunset" ] )
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Heading" % ( day + 1, ), { "Today": xbmc.getLocalizedString( 33006 ), "Tonight": xbmc.getLocalizedString( 33018 ), "Tomorrow": xbmc.getLocalizedString( 33007 ), "Tomorrow Night": xbmc.getLocalizedString( 33019 ) }[ forecast[ 0 ] ] )

    def _fetch_hourly_forecast( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # enumerate thru and clear all hourly times
        for count in range( 1, 28 ):
            # clear all hourly times as some locals do not have all of them
            self.WEATHER_WINDOW.clearProperty( "Hourly.%d.Time" % ( count, ) )
        # fetch hourly forecast
        forecasts = self.WeatherClient.fetch_hourly_forecast()
        # date dictionary
        date_dict = { "January": xbmc.getLocalizedString( 51 ), "February": xbmc.getLocalizedString( 52 ), "March": xbmc.getLocalizedString( 53 ), "April": xbmc.getLocalizedString( 54 ), "May": xbmc.getLocalizedString( 55 ), "June": xbmc.getLocalizedString( 56 ), "July": xbmc.getLocalizedString( 57 ), "August": xbmc.getLocalizedString( 58 ), "September": xbmc.getLocalizedString( 59 ), "October": xbmc.getLocalizedString( 60 ), "November": xbmc.getLocalizedString( 61 ), "December": xbmc.getLocalizedString( 62 ) }
        # initialize count variable
        count = 0
        # enumerate thru and set the info
        for forecast in forecasts:
            # do we need to skip this time
            if ( ( ":15" in forecast[ 0 ] or ":45" in forecast[ 0 ] ) and int( self.Settings.getSetting( "hourly_steps") ) > 0 ):
                continue
            if ( ":30" in forecast[ 0 ] and int( self.Settings.getSetting( "hourly_steps") ) > 1 ):
                continue
            # we want this one, increment counter
            count += 1
            # set properties
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Time" % ( count, ), forecast[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Date" % ( count, ), "%s %s" % ( date_dict[ forecast[ 1 ].split( " " )[ 0 ] ], forecast[ 1 ].split( " " )[ 1 ], ) )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.OutlookIcon" % ( count, ), forecast[ 2 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.FanartCode" % ( count, ), os.path.splitext( os.path.basename( forecast[ 2 ] ) )[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Temperature" % ( count, ), forecast[ 3 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Outlook" % ( count, ), forecast[ 4 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.FeelsLike" % ( count, ), forecast[ 5 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Precipitation" % ( count, ), forecast[ 6 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Humidity" % ( count, ), forecast[ 7 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.WindDirection" % ( count, ), forecast[ 8 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.WindSpeed" % ( count, ), forecast[ 9 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.ShortWindDirection" % ( count, ), forecast[ 10 ] )
        # set our headings
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading1", xbmc.getLocalizedString( 555 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading2", xbmc.getLocalizedString( 33020 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading3", xbmc.getLocalizedString( 401 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading4", xbmc.getLocalizedString( 33024 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading5", xbmc.getLocalizedString( 33022 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading6", xbmc.getLocalizedString( 406 ) )
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading7", xbmc.getLocalizedString( 404 ) )

    def _fetch_weekend_forecast( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # fetch weekend forecast
        forecasts = self.WeatherClient.fetch_weekend_forecast()
        # enumerate thru and set the info
        for day, forecast in enumerate( forecasts ):
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.OutlookIcon" % ( day + 1, ), forecast[ 2 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.FanartCode" % ( day + 1, ), os.path.splitext( os.path.basename( forecast[ 2 ] ) )[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Outlook" % ( day + 1, ), forecast[ 3 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.HighTemperature" % ( day + 1, ), forecast[ 5 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.LowTemperature" % ( day + 1, ), forecast[ 7 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Precipitation" % ( day + 1, ), forecast[ 9 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Wind" % ( day + 1, ), forecast[ 11 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.UV" % ( day + 1, ), forecast[ 13 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Humidity" % ( day + 1, ), forecast[ 15 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Sunrise" % ( day + 1, ), forecast[ 17 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Sunset" % ( day + 1, ), forecast[ 19 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Forecast" % ( day + 1, ), forecast[ 20 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Observed" % ( day + 1, ), forecast[ 21 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.ObservedPrecipitation" % ( day + 1, ), forecast[ 23 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.ObservedAvgHighTemperature" % ( day + 1, ), forecast[ 25 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.ObservedAvgLowTemperature" % ( day + 1, ), forecast[ 27 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.ObservedRecordHighTemperature" % ( day + 1, ), forecast[ 29 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.ObservedRecordLowTemperature" % ( day + 1, ), forecast[ 31 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.DepartureHigh" % ( day + 1, ), forecast[ 33 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.DepartureHighColor" % ( day + 1, ), ( "low", "high", "default", )[ ( len( forecast[ 33 ] ) and forecast[ 33 ][ 0 ] == "+" ) + ( forecast[ 33 ] == "+0" ) ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.DepartureLow" % ( day + 1, ), forecast[ 34 ] )
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.DepartureLowColor" % ( day + 1, ), ( "low", "high", "default", )[ ( len( forecast[ 34 ] ) and forecast[ 34 ][ 0 ] == "+" ) + ( forecast[ 34 ] == "+0" ) ] )
            # do this last so skin's visibilty works better
            self.WEATHER_WINDOW.setProperty( "Weekend.%d.Date" % ( day + 1, ), forecast[ 1 ] )

    def _fetch_10day_forecast( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # fetch daily forecast
        forecasts = self.WeatherClient.fetch_10day_forecast()
        # clear the 10th day as sometimes there is not one
        self.WEATHER_WINDOW.clearProperty( "Daily.10.ShortDay" )
        self.WEATHER_WINDOW.clearProperty( "Daily.10.LongDay" )
        # localized long and short day dictionary
        shortdayDict = { "Mon": xbmc.getLocalizedString( 41 ), "Tue": xbmc.getLocalizedString( 42 ), "Wed": xbmc.getLocalizedString( 43 ), "Thu": xbmc.getLocalizedString( 44 ), "Fri": xbmc.getLocalizedString( 45 ), "Sat": xbmc.getLocalizedString( 46 ), "Sun": xbmc.getLocalizedString( 47 ), "Today": xbmc.getLocalizedString( 33006 ), "Tonight": xbmc.getLocalizedString( 33018 ) }
        longdayDict = { "Mon": xbmc.getLocalizedString( 11 ), "Tue": xbmc.getLocalizedString( 12 ), "Wed": xbmc.getLocalizedString( 13 ), "Thu": xbmc.getLocalizedString( 14 ), "Fri": xbmc.getLocalizedString( 15 ), "Sat": xbmc.getLocalizedString( 16 ), "Sun": xbmc.getLocalizedString( 17 ), "Today": xbmc.getLocalizedString( 33006 ), "Tonight": xbmc.getLocalizedString( 33018 ) }
        # enumerate thru and set the info
        for count, forecast in enumerate( forecasts ):
            self.WEATHER_WINDOW.setProperty( "Daily.%d.LongDay" % ( count + 1, ), longdayDict[ forecast[ 0 ] ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.ShortDay" % ( count + 1, ), shortdayDict[ forecast[ 0 ] ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.Date" % ( count + 1, ), forecast[ 1 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.OutlookIcon" % ( count + 1, ), forecast[ 2 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.FanartCode" % ( count + 1, ), os.path.splitext( os.path.basename( forecast[ 2 ] ) )[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.Outlook" % ( count + 1, ), forecast[ 3 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.HighTemperature" % ( count + 1, ), forecast[ 4 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.LowTemperature" % ( count + 1, ), forecast[ 5 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.Precipitation" % ( count + 1, ), forecast[ 6 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.WindDirection" % ( count + 1, ), forecast[ 7 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.WindSpeed" % ( count + 1, ), forecast[ 8 ] )
            self.WEATHER_WINDOW.setProperty( "Daily.%d.ShortWindDirection" % ( count + 1, ), forecast[ 9 ] )
        # set our heading properties
        self.WEATHER_WINDOW.setProperty( "Daily.Heading1", xbmc.getLocalizedString( 552 ) )
        self.WEATHER_WINDOW.setProperty( "Daily.Heading2", xbmc.getLocalizedString( 33020 ) )
        self.WEATHER_WINDOW.setProperty( "Daily.Heading3", xbmc.getLocalizedString( 393 ) )
        self.WEATHER_WINDOW.setProperty( "Daily.Heading4", xbmc.getLocalizedString( 391 ) )
        self.WEATHER_WINDOW.setProperty( "Daily.Heading5", xbmc.getLocalizedString( 33022 ) )
        self.WEATHER_WINDOW.setProperty( "Daily.Heading6", xbmc.getLocalizedString( 404 ) )

    def _exit_script( self ):
        # end script
        pass

"""
class FetchInfo( Thread ):
    def __init__( self, method ):
        Thread.__init__( self )
        self.method = method

    def run( self ):
        self.method()
"""