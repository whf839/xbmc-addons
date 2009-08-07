"""
    GUI for displaying maps and forecasts from weather.com
    
    Nuka1195
"""

# main imports
import sys
import os

import xbmc
import xbmcgui

from threading import Thread

import resources.lib.WeatherClient as WeatherClient


class Main:
    _ = xbmc.Language( os.getcwd() ).getLocalizedString
    Settings = xbmc.Settings( os.getcwd() )

    def __init__( self, *args, **kwargs ):
        # get current window
        self._get_weather_window()
        # get our new WeatherClient
        self._get_client()
        # get user preferences
        self._get_settings()
        # if user selected a new map, only need to fetch it
        if ( sys.argv[ 1 ].startswith( "map=" ) ):
            self._fetch_map( sys.argv[ 1 ][ 4 : ] )
        else:
            # set plugin name property
            self._set_plugin_name()
            # clear key properties if new location
            if ( self.new_location ):
                self._clear_properties()
            # initialize our thread list
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
        # we're finished, exit
        self._exit_script()

    def _get_settings( self ):
        self.settings[ "maplist1_category" ] = self.WeatherClient.BASE_MAPS[ int( self.Settings.getSetting( "maplist1" ) ) ][ 0 ]
        self.WEATHER_WINDOW.setProperty( "MapList.1.LongTitle", self._( ( 32600, 32601, 32602, 32603, 32604, 32605, 32606, 32607, 32608, 32609, 32610, 32611, 32612, 32613, 32614, 32615, 32616, 32617, 32618, 32619, 32620, 32621, 32622, 32623, 32624, 32625, 32626, 32627, 32628, 32629, 32630, 32631, 32632, 32633, 32634, 32635, 32636, 32637, 32638, 32639, 32640, 32641, 32642, 32643, 32644, 32645, 32646, 32647, 32648, 32649, 32650, 32651, 32652, 32653, 32654, 32655, 32656, 32657, 32658, 32659, 32660, 32661, 32662, 32663, )[ int( self.Settings.getSetting( "maplist1" ) ) ] ) )
        self.WEATHER_WINDOW.setProperty( "MapList.1.ShortTitle", self._( ( 32800, 32801, 32802, 32803, 32804, 32805, 32806, 32807, 32808, 32809, 32810, 32811, 32812, 32813, 32814, 32815, 32816, 32817, 32818, 32819, 32820, 32821, 32822, 32823, 32824, 32825, 32826, 32827, 32828, 32829, 32830, 32831, 32832, 32833, 32834, 32835, 32836, 32837, 32838, 32839, 32840, 32841, 32842, 32843, 32844, 32845, 32846, 32847, 32848, 32849, 32850, 32851, 32852, 32853, 32854, 32855, 32856, 32857, 32858, 32859, 32860, 32861, 32862, 32863, )[ int( self.Settings.getSetting( "maplist1" ) ) ] ) )
        self.settings[ "maplist2_category" ] = self.WeatherClient.BASE_MAPS[ int( self.Settings.getSetting( "maplist2" ) ) ][ 0 ]
        self.WEATHER_WINDOW.setProperty( "MapList.2.LongTitle", self._( ( 32600, 32601, 32602, 32603, 32604, 32605, 32606, 32607, 32608, 32609, 32610, 32611, 32612, 32613, 32614, 32615, 32616, 32617, 32618, 32619, 32620, 32621, 32622, 32623, 32624, 32625, 32626, 32627, 32628, 32629, 32630, 32631, 32632, 32633, 32634, 32635, 32636, 32637, 32638, 32639, 32640, 32641, 32642, 32643, 32644, 32645, 32646, 32647, 32648, 32649, 32650, 32651, 32652, 32653, 32654, 32655, 32656, 32657, 32658, 32659, 32660, 32661, 32662, 32663, )[ int( self.Settings.getSetting( "maplist2" ) ) ] ) )
        self.WEATHER_WINDOW.setProperty( "MapList.2.ShortTitle", self._( ( 32800, 32801, 32802, 32803, 32804, 32805, 32806, 32807, 32808, 32809, 32810, 32811, 32812, 32813, 32814, 32815, 32816, 32817, 32818, 32819, 32820, 32821, 32822, 32823, 32824, 32825, 32826, 32827, 32828, 32829, 32830, 32831, 32832, 32833, 32834, 32835, 32836, 32837, 32838, 32839, 32840, 32841, 32842, 32843, 32844, 32845, 32846, 32847, 32848, 32849, 32850, 32851, 32852, 32853, 32854, 32855, 32856, 32857, 32858, 32859, 32860, 32861, 32862, 32863, )[ int( self.Settings.getSetting( "maplist2" ) ) ] ) )
        self.settings[ "maplist3_category" ] = self.WeatherClient.BASE_MAPS[ int( self.Settings.getSetting( "maplist3" ) ) ][ 0 ]
        self.WEATHER_WINDOW.setProperty( "MapList.3.LongTitle", self._( ( 32600, 32601, 32602, 32603, 32604, 32605, 32606, 32607, 32608, 32609, 32610, 32611, 32612, 32613, 32614, 32615, 32616, 32617, 32618, 32619, 32620, 32621, 32622, 32623, 32624, 32625, 32626, 32627, 32628, 32629, 32630, 32631, 32632, 32633, 32634, 32635, 32636, 32637, 32638, 32639, 32640, 32641, 32642, 32643, 32644, 32645, 32646, 32647, 32648, 32649, 32650, 32651, 32652, 32653, 32654, 32655, 32656, 32657, 32658, 32659, 32660, 32661, 32662, 32663, )[ int( self.Settings.getSetting( "maplist3" ) ) ] ) )
        self.WEATHER_WINDOW.setProperty( "MapList.3.ShortTitle", self._( ( 32800, 32801, 32802, 32803, 32804, 32805, 32806, 32807, 32808, 32809, 32810, 32811, 32812, 32813, 32814, 32815, 32816, 32817, 32818, 32819, 32820, 32821, 32822, 32823, 32824, 32825, 32826, 32827, 32828, 32829, 32830, 32831, 32832, 32833, 32834, 32835, 32836, 32837, 32838, 32839, 32840, 32841, 32842, 32843, 32844, 32845, 32846, 32847, 32848, 32849, 32850, 32851, 32852, 32853, 32854, 32855, 32856, 32857, 32858, 32859, 32860, 32861, 32862, 32863, )[ int( self.Settings.getSetting( "maplist3" ) ) ] ) )

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
        self.new_location = ( xbmc.getInfoLabel( "Skin.String(Weather.AreaCode)" ) != self.areacode )
        # if new set it
        if ( self.new_location ):
            xbmc.executebuiltin( "Skin.SetString(Weather.AreaCode,%s" % self.areacode )
        # setup our radar client
        self.WeatherClient = WeatherClient.WeatherClient( self.areacode, self.settings[ "translate" ] )

    def _set_maps_path( self, path=0, maps_path="" ):
        # we have three possibilities. loading, default (error) or the actual map path
        if ( path == 0 ):
            #xbmc.executebuiltin( "Skin.SetString(twc-mapspath,TWC Plus/loading)" )
            self.WEATHER_WINDOW.setProperty( "MapStatus", "loading" )
            self.WEATHER_WINDOW.setProperty( "MapPath", "weather/loading" )
        elif ( path == 1 ):
            self.WEATHER_WINDOW.setProperty( "MapStatus", "loaded" )
            self.WEATHER_WINDOW.setProperty( "MapPath", maps_path )
            #xbmc.executebuiltin( "Skin.SetString(twc-mapspath,%s)" % ( maps_path, ) )
        elif ( path == 2 ):
            self.WEATHER_WINDOW.setProperty( "MapStatus", "error" )
            self.WEATHER_WINDOW.setProperty( "MapPath", "weather/default" )
            #xbmc.executebuiltin( "Skin.SetString(twc-mapspath,TWC Plus/default)" )

    def _clear_properties( self ):
        # alerts
        self.WEATHER_WINDOW.clearProperty( "Alerts" )
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
        # set map path to loading
        self._set_maps_path()
        # clear our maplist properties
        for count in range( 3 ):
            # enumerate thru and clear all map list labels and onclicks
            for count2 in range( 30 ):
                # these are what the user sees and the action the button performs
                self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapLabel%d" % ( count + 1, count2 + 1, ) )
                self.WEATHER_WINDOW.clearProperty( "MapList.%d.MapOnclick%d" % ( count + 1, count2 + 1, ) )
        
    def _fetch_map_list( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # get the users default map
        default = current_map = xbmc.getInfoLabel( "Skin.String(weather.defaultmap)" )
        # enumurate thru map lists and fetch map list
        for maplist_count in range( 1, 4 ):
            # get the correct category
            map_category = self.settings[ "maplist%d_category" % ( maplist_count, ) ]
            # check for users preferemce
            for count, mapc in enumerate( self.WeatherClient.BASE_MAPS ):
                # found it, no need to continue
                if ( mapc[ 0 ] == map_category ):
                    break
            # fetch map list
            maps = self.WeatherClient.fetch_map_list( count )
            # set a current_map in case one isn't set
            if ( not current_map ):
                current_map = maps[ 0 ][ 0 ]
            # enumerate thru our map list and add map and title and check for default
            for count, map in enumerate( maps ):
                # create our label and onclick event
                self.WEATHER_WINDOW.setProperty( "MapList.%d.MapLabel%d" % ( maplist_count, count + 1, ), map[ 1 ] )
                self.WEATHER_WINDOW.setProperty( "MapList.%d.MapOnclick%d" % ( maplist_count, count + 1, ), "XBMC.RunScript(%s,map=%s)" % ( sys.argv[ 0 ], map[ 0 ], ) )
                # if we have a match, set our class variable
                if ( map[ 1 ] == default ):
                    current_map = map[ 0 ]
        # fetch the current map
        self._fetch_map( current_map )

    def _fetch_map( self, map ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # we set our skin setting to defaultimages while downloading
        self._set_maps_path()
        # fetch the available map urls
        maps = self.WeatherClient.fetch_map_urls( map )
        # fetch the images
        maps_path, expires = self.WeatherClient.fetch_images( maps )
        # hack incase the weather in motion link was bogus
        if ( expires < 0 and len( maps[ 1 ] ) ):
            maps_path, expires = self.WeatherClient.fetch_images( ( maps[ 0 ], [], ) )
        # now set our skin string so multi image will display images 1==success, 2==failure
        self._set_maps_path( ( maps_path == "" ) + 1, maps_path )

    def _set_alerts( self, alerts, alertscolor, alertscount ):
        # set any alerts
        self.WEATHER_WINDOW.setProperty( "Alerts", alerts )
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
        alerts, alertscolor, alertscount, forecasts, video = self.WeatherClient.fetch_36_forecast( self.WEATHER_WINDOW.getProperty( "Video" ) )
        # set any alerts
        self._set_alerts( alerts, alertscolor, alertscount )
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
            self.WEATHER_WINDOW.setProperty( "36Hour.%d.Heading" % ( day + 1, ), { "Today": xbmc.getLocalizedString( 33006 ), "Tonight": xbmc.getLocalizedString( 33018 ), "Tomorrow": xbmc.getLocalizedString( 33007 ), "Tomorrow Night": xbmc.getLocalizedString( 33019 ) }[ forecast[ 0 ] ] )

    def _fetch_hourly_forecast( self ):
        # exit script if user changed locations
        if ( self.areacode != xbmc.getInfoLabel( "Window(Weather).Property(AreaCode)" ) ):
            return
        # enumerate thru and clear all hourly times
        for count in range( 28 ):
            # clear all hourly times as some locals do not have all 27
            self.WEATHER_WINDOW.clearProperty( "Hourly.%d.Time" % ( count + 1, ) )
        # fetch hourly forecast
        headings, forecasts = self.WeatherClient.fetch_hourly_forecast()
        # enumerate thru and set the info
        for count, forecast in enumerate( forecasts ):
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Time" % ( count + 1, ), forecast[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.OutlookIcon" % ( count + 1, ), forecast[ 1 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.FanartCode" % ( count + 1, ), os.path.splitext( os.path.basename( forecast[ 1 ] ) )[ 0 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Temperature" % ( count + 1, ), forecast[ 2 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Outlook" % ( count + 1, ), forecast[ 3 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.FeelsLike" % ( count + 1, ), forecast[ 4 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Precipitation" % ( count + 1, ), forecast[ 5 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.Humidity" % ( count + 1, ), forecast[ 6 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.WindDirection" % ( count + 1, ), forecast[ 7 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.WindSpeed" % ( count + 1, ), forecast[ 8 ] )
            self.WEATHER_WINDOW.setProperty( "Hourly.%d.ShortWindDirection" % ( count + 1, ), forecast[ 9 ] )
        # set our headings
        self.WEATHER_WINDOW.setProperty( "Hourly.Heading1",xbmc.getLocalizedString( 555 ) )
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
        headings, forecasts = self.WeatherClient.fetch_10day_forecast()
        # clear the 10th day as sometimes there is not one
        self.WEATHER_WINDOW.clearProperty( "Daily.10.ShortDay" )
        self.WEATHER_WINDOW.clearProperty( "Daily.10.LongDay" )
        # localized long and short day dictionary
        shortdayDict = { "Mon": xbmc.getLocalizedString( 41 ), "Tue": xbmc.getLocalizedString( 42 ), "Wed": xbmc.getLocalizedString( 43 ), "Thu": xbmc.getLocalizedString( 44 ), "Fri": xbmc.getLocalizedString( 45 ), "Sat": xbmc.getLocalizedString( 46 ), "Sun": xbmc.getLocalizedString( 47 ), "Today": xbmc.getLocalizedString( 33006 ),"Tonight": xbmc.getLocalizedString( 33018 ) }
        longdayDict = { "Mon": xbmc.getLocalizedString( 11 ), "Tue": xbmc.getLocalizedString( 12 ), "Wed": xbmc.getLocalizedString( 13 ), "Thu": xbmc.getLocalizedString( 14 ), "Fri": xbmc.getLocalizedString( 15 ), "Sat": xbmc.getLocalizedString( 16 ), "Sun": xbmc.getLocalizedString( 17 ), "Today": xbmc.getLocalizedString( 33006 ),"Tonight": xbmc.getLocalizedString( 33018 ) }
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


class FetchInfo( Thread ):
    def __init__( self, method ):
        Thread.__init__( self )
        self.method = method

    def run( self ):
        self.method()
