"""
    TWC api client module
"""

# main imports
import sys
import os

try:
    import xbmc
    DEBUG = False
except:
    DEBUG = True

import urllib2
import md5
import re
import shutil
import time
import cookielib


class WeatherAlert:
    def __init__( self, htmlSource ):
        self.alert = ""
        try:
            self._get_alert( htmlSource )
        except:
            pass

    def _get_alert( self, htmlSource ):
        # regex patterns
        pattern_alert = "<h1>([^<]+)</h1>"
        pattern_expires = "<p>(<b>.+?</b>[^<]+)</p>"
        pattern_issuedby = "<p class=\"alIssuedBy\">(.+?)</p>"
        pattern_narrative = "<p class=\"alNarrative\">(.*?)</p>"
        pattern_moreinfo = "<h2>([^<]+)</h2>\n.+?<p class=\"alSynopsis\">"
        pattern_synopsis = "<p class=\"alSynopsis\">(.+?)</p>"
        # fetch alert
        alert = re.findall( pattern_alert, htmlSource )[ 0 ]
        # fetch expires
        try:
            expires = re.findall( pattern_expires, htmlSource )[ 0 ].replace( "<b>", "" ).replace( "</b>", "" )
        except:
            expires = ""
        # fetch issued by
        try:
            issuedby_list = re.findall( pattern_issuedby, htmlSource, re.DOTALL )[ 0 ].split( "<br>" )
            issuedby = "[I]"
            for item in issuedby_list:
                issuedby += item.strip()
                issuedby += "\n"
            issuedby += "[/I]"
            # fetch narrative
            description_list = re.findall( pattern_narrative, htmlSource, re.DOTALL )
            narrative = ""
            for item in description_list:
                narrative += "%s\n\n" % ( item.strip(), )
            try:
                # fetch more info
                moreinfo = re.findall( pattern_moreinfo, htmlSource )[ 0 ]
                moreinfo = "[B]%s[/B]" % ( moreinfo, )
                # fetch sysnopsis
                description_list = re.findall( pattern_synopsis, htmlSource, re.DOTALL )
                synopsis = ""
                for item in description_list:
                    synopsis += "%s\n\n" % ( item.strip(), )
            except:
                moreinfo = ""
                synopsis = ""
        except:
            try:
                narrative = ""
                synopsis = ""
                issuedby = re.findall( "<p>(.+)?</p>", htmlSource )[ 0 ]
                items =  re.findall( "<B>(.+)?</B>\s.*\s.*\s.*\s.+?<IMG SRC=\"[^>]+> <B>([^<]+)</B><BR>Type: (.+)", htmlSource )[ 0 ]
                moreinfo = "\nType: %s (%s)\nLevel: %s" % ( items[ 0 ], items[ 2 ], items[ 1 ], )
            except:
                pass
        try:
            # create our alert string
            self.alert = "[B]%s[/B]\n%s\n\n%s\n%s\n\n%s\n\n%s" % ( alert, expires, issuedby, narrative.strip(), moreinfo, synopsis.strip(), )
            self.alert = "%s\n%s\n\n" % ( self.alert.strip(), "-"*100, )
            self.title = "[B]%s[/B]" % ( alert, )
        except:
            self.alert = None

class Forecast36HourParser:
    def __init__( self, htmlSource ):
        self.forecast = []
        self.alerts = []
        self.video_location = []
        self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        #pattern_dmacode = "var omn_dmaCode=\"([0-9]+)\""
        pattern_locstate = "var omn_locstate=\"([^\"]+)\""
        pattern_video_location = ">Watch the ([A-Za-z]+) Forecast<"
        #pattern_dmaname = "dma_names\[\"%s\"\]=\"([^\"]+)\""
        pattern_alerts = "alertArray\[[0-9]+\] = new alertObj\('([^']+)','([^']+)','([^']+)'"
        pattern_days = "from=[^\"]+\" class=\"[^\"]+\"><B>([^<]+)</font></B></A></td>"
        pattern_icon = "<img src=\"http://image.weather.com/web/common/wxicons/[0-9]+/([0-9]+)\.gif\?[^\"]+\" alt=\""
        pattern_forecast_brief = "<font CLASS=\"[^\"]+\">([^<]+)</font>"
        pattern_temp = "<td valign=\"middle\" align=\"[^\"]+\"><font CLASS=\"[^\"]+\">([^<]+)<br>[^<]+<font class=\"[^\"]+\"><[^<]+>([^<]+)<[^<]+></font>"
        pattern_precip_title = "<TD valign=\"[^\"]+\" width=\"[^\"]+\" class=\"[^\"]+\" align=\"[^\"]+\">([A-Za-z]+[^<]+)</td>"
        pattern_precip_amount = "<TD valign=\"[^\"]+\" width=\"[^\"]+\" class=\"[^\"]+\" align=\"[^\"]+\">([0-9]+[^<]+)</td>"
        pattern_outlook = "<DIV STYLE=\"padding:5px 5px 5px 0px;\">([^\n|^<]*)"
        pattern_daylight = "<TD valign=\"[^\"]+\" align=\"[^\"]+\" class=\"[^\"]+\">([^<]+)</TD>"
        #pattern_videos = "<a href=\"(/multimedia/videoplayer.html\?clip=[^&]+&collection=[^&]+)&from="
        #pattern_region = "<A HREF=\"/multimedia/videoplayer.html\?clip=[0-9]+&collection=(regwxforecast)&from=[^<]+>(.+?)</A>"
        try:
            # fetch dmacode
            #dmacode = re.findall( pattern_dmacode, htmlSource )[ 0 ]
            # fetch state
            locstate = re.findall( pattern_locstate, htmlSource )[ 0 ].lower()
            # fetch video location
            #self.video_location = ( re.findall( pattern_dmaname % ( dmacode, ), htmlSource )[ 0 ].lower().replace( " ", "" ), locstate, )
            self.video_location = ( re.findall( pattern_video_location, htmlSource )[ 0 ].lower().replace( " ", "" ), locstate, )
        except:
            pass
        # fetch regional video
        """
        try:
            if ( not self.video_location ):
                self.video_location = re.findall( pattern_region, htmlSource )[ 0 ]
        except:
            pass
        """
        # fetch alerts
        self.alerts = re.findall( pattern_alerts, htmlSource )
        # fetch days
        days = re.findall( pattern_days, htmlSource )
        # fetch icon
        icon = re.findall( pattern_icon, htmlSource )
        # fetch brief description
        brief = re.findall( pattern_forecast_brief, htmlSource )
        # fetch temperature
        temperature = re.findall( pattern_temp, htmlSource )
        # fetch precip title
        precip_title = re.findall( pattern_precip_title, htmlSource )
        # fetch precip title
        precip_amount = re.findall( pattern_precip_amount, htmlSource )
        # fetch forecasts
        outlook = re.findall( pattern_outlook, htmlSource )
        # fetch daylight
        daylight = re.findall( pattern_daylight, htmlSource )
        # enumerate thru and combine the day with it's forecast
        if ( len( days ) ):
            for count, day in enumerate( days ):
                # make icon path
                if ( not DEBUG ):
                    iconpath = "/".join( [ "special://temp", "weather", "128x128", icon[ count ] + ".png" ] )
                else:
                    iconpath = icon[ count ] + ".png"
                # add result to our class variable
                self.forecast += [ ( day, iconpath, brief[ count ], temperature[ count ][ 0 ], temperature[ count ][ 1 ].replace( "&deg; ", "\xb0" ), precip_title[ count ], precip_amount[ count ], outlook[ count ].strip(), daylight[ count ], ) ]


class ForecastHourByHourParser:
    def __init__( self, htmlSource ):
        self.headings = []
        self.forecast = []
        self.alerts = []
        self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        pattern_headings = "<div class=\"hbhTD[^\"]+\"><div title=\"[^>]+>([^<]+)</div></div>"
        pattern_info = "<div class=\"hbhTDTime[^>]+><div>([^<]+)</div></div>.*\s\
[^<]+<div class=\"hbhTDConditionIcon\"><div><img src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/(gray/)?([0-9]+).gif\"[^>]+></div></div>.*\s\
[^<]+<div class=\"hbhTDCondition\"><div><b>([^<]+)</b><br>([^<]+)</div></div>.*\s\
[^<]+<div class=\"hbhTDFeels\"><div>([^<]*)</div></div>.*\s\
[^<]+<div class=\"hbhTDPrecip\"><div>([^<]*)</div></div>.*\s\
[^<]+<div class=\"hbhTDHumidity\"><div>([^<]*)</div></div>.*\s\
[^<]+<div class=\"hbhTDWind\"><div>([^<]*)<br>([^<]*)</div></div>"
        pattern_alerts = "alertArray\[[0-9]+\] = new alertObj\('([^']+)','([^']+)','([^']+)'"
        # fetch alerts
        self.alerts = re.findall( pattern_alerts, htmlSource )
        # fetch headings
        headings = re.findall( pattern_headings, htmlSource )
        # fetch info
        info = re.findall( pattern_info, htmlSource )
        # enumerate thru and create heading and forecast
        if ( len( headings ) and len( info ) ):
            # fixe headings
            for heading in headings:
                self.headings += [ heading.replace( "<br>", "\n" ).replace( "<BR>", "\n" ) ]
            # create our forecast list
            for item in info:
                # make icon path
                if ( not DEBUG ):
                    iconpath = "/".join( [ "special://temp", "weather", "128x128", item[ 2 ] + ".png" ] )
                else:
                    iconpath = item[ 2 ] + ".png"
                # add result to our class variable
                self.forecast += [ ( item[ 0 ], iconpath, item[ 3 ].replace( "&deg;", "\xb0" ), item[ 4 ].replace( "&deg;", "\xb0" ), item[ 5 ].replace( "&deg;", "\xb0" ), item[ 6 ], item[ 7 ], item[ 8 ] + "\n" + item[ 9 ].strip(), ) ]


class ForecastWeekendParser:
    def __init__( self, htmlSource ):
        self.forecast = []
        self.alerts = []
        self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        pattern_heading = "from=\"weekend[\"]+>([^<]+)</A>.*\s.*\s\
[^<]+<TD width=\"[^\"]+\" class=\"wkndButton[A-Z]+\" align=\"[^\"]+\" valign=\"[^\"]+\"><FONT class=\"[^\"]+\">([^\&]+)&nbsp;.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s\
[^>]+>[^>]+>([^<]+)<"
        pattern_observed = ">(Observed:)+"
        #pattern_brief = "<IMG src=\"http://image.weather.com/web/common/wxicons/[pastwx/]*[0-9]+/([0-9]+)\.gif.*alt=\"([^\"]+)\""
        #pattern_brief = "<IMG src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/([0-9]+).gif.*alt=\"([^\"]+)\""
        pattern_brief = "<IMG src=\"http://(?:i.imwx.com)?(?:image.weather.com)?/web/common/wxicons/(?:pastwx/)?[0-9]+/([0-9]+).gif.*alt=\"([^\"]+)\""
        pattern_past = "<TD align=\"left\" class=\"grayFont10\">([^<]+)</TD>"
        pattern_past2 = "<TD align=\"[left|right]+\" class=\"blueFont10\">[<B>]*<FONT color=\"[^\"]+\">([^\s|^<]+)[^\n]+"
        pattern_avg = "<tr><td align=\"right\" valign=\"top\" CLASS=\"blueFont10\">([^<]+)<.*\s.*\s[^[A-Z0-9]+(.*&deg;[F|C]+)"
        #pattern_avg = "<tr><td align=\"right\" valign=\"top\" CLASS=\"blueFont10\">([^<]+)<.*\s.*\s.*\s\t*(.+?)\s"
        pattern_high = "<FONT class=\"[^\"]+\">([^<]+)<BR><FONT class=\"[^\"]+\"><NOBR>([^<]+)</FONT></NOBR>"
        pattern_low = "<FONT class=\"[^\"]+\">([^<]+)</FONT><BR><FONT class=\"[^\"]+\"><B>([^<]+)</B></FONT>"
        ##pattern_precip = "<TD valign=\"[^\"]+\" width=\"[^\"]+\" class=\"[^\"]+\" align=\"[^\"]+\">(.*)\r"
        pattern_precip = "<TD valign=\"top\" width=\"50%\" class=\"blueFont10\" align=\"[left|right]+\">(.*)"
        pattern_wind = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)</td><td align=\"[^\"]+\">&nbsp;</td><td valign=\"[^\"]+\" CLASS=\"[^\"]+\"><B>.*\n[^A-Z]+([A-Z]+)<br>([^<]+)</B>"
        pattern_uv = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)</td>\s[^>]+>[^>]+>[^>]+><B>([^<]+)"
        pattern_humidity = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)[^>]+>[^>]+>[^>]+>[^>]+><B>([0-9]+%)"
        pattern_daylight = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)[^>]+>[^>]+>[^>]+>[^>]+><B>([0-9]+:[0-9]+[^<]+)</B></td>"
        pattern_outlook = "<TD colspan=\"3\" class=\"blueFont10\" valign=\"middle\" align=\"left\">([^<]+)</TD>"
        pattern_alerts = "alertArray\[[0-9]+\] = new alertObj\('([^']+)','([^']+)','([^']+)'"
        pattern_departures = "<FONT COLOR=\"#7d8c9f\"><B>\s.*\s\s+(.+?F)"
        # fetch alerts
        self.alerts = re.findall( pattern_alerts, htmlSource )
        # fetch headings
        headings = re.findall( pattern_heading, htmlSource )
        # fetch observed status
        observeds = re.findall( pattern_observed, htmlSource )
        # insert necessary dummy entries
        for  i in range( 3 - len( observeds ) ):
            observeds.append( "" )
        # fetch briefs
        briefs = re.findall( pattern_brief, htmlSource )
        # insert necessary dummy entries
        for count, i in enumerate( range( 3 - len( briefs ) ) ):
            briefs.insert( count, ( "na", "", ) )
        # fetch past info
        pasts = re.findall( pattern_past, htmlSource )
        if ( pasts == [] ):
            pasts2 = re.findall( pattern_past2, htmlSource )
            # create the pasts list
            for count, i in enumerate( range( 0, len( pasts2 ), 2 ) ):
                pasts += [ pasts2[ count * 2 ] + pasts2[ count * 2 + 1 ] ]
        # insert necessary dummy entries
        for i in range( 9 - len( pasts ) ):
            pasts.append( ":&nbsp;" )
        # fetch average info
        avgs = re.findall( pattern_avg, htmlSource )
        # insert necessary dummy entries
        for i in range( 0, 12 - len( avgs ) ):
            avgs.append( ( "", "", ) )
        # fetch highs
        highs = re.findall( pattern_high, htmlSource )
        # insert necessary dummy entries
        for count, i in enumerate( range( 3 - len( highs ) ) ):
            highs.insert( count, ( pasts[ count * 3 ].split( ":&nbsp;" )[ 0 ], pasts[ count * 3 ].split( ":&nbsp;" )[ 1 ], ) )
        # fetch lows
        lows = re.findall( pattern_low, htmlSource )
        # insert necessary dummy entries
        for count, i in enumerate( range( 3 - len( lows ) ) ):
            lows.insert( count, ( pasts[ count * 3 + 1 ].split( ":&nbsp;" )[ 0 ], pasts[ count * 3 + 1 ].split( ":&nbsp;" )[ 1 ], ) )
        # fetch precips
        precips = re.findall( pattern_precip, htmlSource )
        # insert necessary dummy entries
        for i in range( 6 - len( precips ) ):
            precips.insert( 0, "" )
        # fetch winds
        winds = re.findall( pattern_wind, htmlSource )
        # insert necessary dummy entries
        for i in range( 3 - len( winds ) ):
            winds.insert( 0, ( "", "", "", ) )
        # fetch uvs
        uvs = re.findall( pattern_uv, htmlSource )
        # insert necessary dummy entries
        for i in range( 3 - len( uvs ) ):
            uvs.insert( 0, ( "", "", ) )
        # fetch humids
        humids = re.findall( pattern_humidity, htmlSource )
        # insert necessary dummy entries
        for i in range( 3 - len( humids ) ):
            humids.insert( 0, ( "", "", ) )
        # fetch daylights
        daylights = re.findall( pattern_daylight, htmlSource )
        # insert necessary dummy entries
        for i in range( 6 - len( daylights ) ):
            daylights.insert( 0, ( "", "" ) )
        # fetch outlooks
        outlooks = re.findall( pattern_outlook, htmlSource )
        # insert necessary dummy entries
        for i in range( 3 - len( outlooks ) ):
            outlooks.insert( 0, "" )
        # enumerate thru and create our forecast list
        if ( len( headings ) ):
            for count, ( day, date, alert, ) in enumerate( headings ):
                # make icon path
                if ( not DEBUG ):
                    iconpath = "/".join( [ "special://temp", "weather", "128x128", briefs[ count ][ 0 ] + ".png" ] )
                else:
                    iconpath = briefs[ count ][ 0 ] + ".png"
                # add result to our class variable
                self.forecast += [ ( day, date, iconpath, briefs[ count][ 1 ], highs[count][ 0 ], highs[ count ][ 1 ].replace( "&deg;", "\xb0" ),
                lows[ count ][ 0 ], lows[ count ][ 1 ].replace( "&deg;", "\xb0" ), precips[ count * 2 ], precips[ count * 2 + 1 ].replace( "<B>", "" ).replace( "</B>", "" ),
                winds[ count ][ 0 ], winds[ count ][ 1 ] + " " + winds[ count ][ 2 ], uvs[ count ][ 0 ], uvs[ count ][ 1 ],
                humids[ count ][ 0 ], humids[ count ][ 1 ], daylights[ count * 2 ][ 0 ], daylights[ count * 2 ][ 1 ], daylights[ count * 2 + 1 ][ 0 ],
                daylights[ count * 2 + 1 ][ 1 ], outlooks[ count ], observeds[ count ], pasts[ count * 3 + 2 ].split( "&nbsp;" )[ 0 ], pasts[ count * 3 + 2 ].split( "&nbsp;" )[ 1 ],
                avgs[ count * 4 ][ 0 ], avgs[ count * 4 ][ 1 ].replace( "&deg;", "\xb0" ), avgs[ count * 4 + 1 ][ 0 ], avgs[ count * 4 + 1 ][ 1 ].replace( "&deg;", "\xb0" ),
                avgs[ count * 4 + 2 ][ 0 ], avgs[ count * 4 + 2 ][ 1 ].replace( "&deg;", "\xb0" ), avgs[ count * 4 + 3 ][ 0 ], avgs[ count * 4 + 3 ][ 1 ].replace( "&deg;", "\xb0" ),
                alert.strip(), ) ]


class Forecast10DayParser:
    def __init__( self, htmlSource ):
        self.headings = []
        self.forecast = []
        self.alerts = []
        self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        pattern_headings = "<p id=\"tdHead[A-Za-z]+\">(.*)</p>"
        pattern_headings2 = "<OPTION value=\"windsdp\" selected>([^<]+)</OPTION>"
        pattern_info = "<p><[^>]+>([^<]+)</a><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s\
[^<]+<p><img src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/([0-9]+).gif[^>]+><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s[^<]+<p><strong>([^<]+)</strong><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s.*\s[^<]+<p>([^<]+)</p>\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s[^<]+<td><p>([^<]+)</p></td>\s.*\s.*\s\
[^<]+<[^<]+<[^<]+<[^<]+<strong>([^<]+</strong>[^<]+)</p>"
        pattern_alerts = "alertArray\[[0-9]+\] = new alertObj\('([^']+)','([^']+)','([^']+)'"
        # fetch alerts
        self.alerts = re.findall( pattern_alerts, htmlSource )
        # fetch headings
        headings = re.findall( pattern_headings, htmlSource )
        headings += re.findall( pattern_headings2, htmlSource )
        # fetch info
        info = re.findall( pattern_info, htmlSource )
        # enumerate thru and create heading and forecast
        if ( len( headings ) and len( info ) ):
            # fixe headings
            for heading in headings:
                self.headings += heading.replace( "<br>", "\n" ).replace( "<BR>", "\n" ).replace( "<strong>", "" ).replace( "&deg;", "\xb0" ).split( "</strong>" )
            # create our forecast list
            for item in info:
                # make icon path
                if ( not DEBUG ):
                    iconpath = "/".join( [ "special://temp", "weather", "128x128", item[ 2 ] + ".png" ] )
                else:
                    iconpath = item[ 2 ] + ".png"
                # add result to our class variable
                self.forecast += [ ( item[ 0 ], item[ 1 ], iconpath, item[ 3 ], item[ 4 ].replace( "&deg;", "\xb0" ), item[ 5 ].replace( "&deg;", "\xb0" ), item[ 6 ].replace( "&#37;", "%" ), item[ 7 ], item[ 8 ].replace( "</strong>", "" ), ) ]


class MaplistParser:
    def __init__( self, htmlSource ):
        self.map_list = []
        self._get_map_list( htmlSource )

    def _get_map_list( self, htmlSource ):
        # regex patterns
        pattern_map_list = "<option.+?value=\"([^\"]+)\".*?>([^<]+)</option>"
        # fetch avaliable maps
        map_list = re.findall( pattern_map_list, htmlSource, re.IGNORECASE )
        # enumerate thru list and eliminate bogus items
        for map in map_list:
            # eliminate bogus items
            if ( len( map[ 0 ] ) > 7 ):#map[ 0 ].endswith( ".html" ) or ( map[ 0 ].lower() != "special" and map[ 1 ].lower() != "see more maps" ) ):
                self.map_list += [ map ]


class MapParser:
    def __init__( self, htmlSource ):
        self.maps = ()
        self._get_maps( htmlSource )

    def _get_maps( self, htmlSource ):
        try:
            # initialize our animated maps list
            animated_maps = []
            # regex patterns
            pattern_maps = "<IMG NAME=\"mapImg\" SRC=\"([^\"]+)\""
            # fetch static map
            static_map = re.findall( pattern_maps, htmlSource )
            # does this map support animation?
            motion = re.findall( ">Weather In Motion<", htmlSource, re.IGNORECASE )
            if ( len( motion ) ):
                # get our map
                region = os.path.splitext( os.path.basename( static_map[ 0 ] ) )[ 0 ]
                # enumerate thru and create our animated map urls
                for i in range( 1, 6 ):
                    animated_maps += [ "http://image.weather.com/looper/archive/%s/%dL.jpg" % ( region, i, ) ]
        except Exception, e:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        self.maps += ( static_map, animated_maps, )


class TWCClient:
    # base urls
    BASE_URL = "http://www.weather.com"
    BASE_FORECAST_URL = "http://www.weather.com/outlook/travel/businesstraveler/%s/%s?bypassredirect=true%s"
    BASE_VIDEO_URL = "http://v.imwx.com/multimedia/video/wxflash/%s.flv"
    BASE_MAPS = (
                                # Main local maps (includes some regional maps)
                                ( "Local", "/outlook/travel/businesstraveler/%s/%s?bypassredirect=true%s", "Local", ),
                                # weather details
                                ( "Weather Details (Alaska)", "/maps/geography/alaskaus/index_large.html", "Alaska", ),
                                ( "Weather Details (Current Weather)", "/maps/maptype/currentweatherusnational/index_large.html", "Current\nWeather", ),
                                ( "Weather Details (Doppler Radar)", "/maps/maptype/dopplerradarusnational/index_large.html", "Doppler Radar", ),
                                ( "Weather Details (Extended Forecasts)", "/maps/maptype/tendayforecastusnational/index_large.html", "Extended\nForecasts", ),
                                ( "Weather Details (Hawaii)", "/maps/geography/hawaiius/index_large.html", "Hawaii", ),
                                ( "Weather Details (Satellite - US)", "/maps/maptype/satelliteusnational/index_large.html", "Satellite\n(US)", ),
                                ( "Weather Details (Satellite - World)", "/maps/maptype/satelliteworld/index_large.html", "Satellite\n(World)", ),
                                ( "Weather Details (Severe Alerts - US)", "/maps/maptype/severeusnational/index_large.html", "Severe Alerts\n(US)", ),
                                ( "Weather Details (Severe Alerts - Regional)", "/maps/maptype/severeusregional/index_large.html", "Severe Alerts\n(Regional)", ),
                                ( "Weather Details (Short Term Forecast)", "/maps/maptype/forecastsusnational/index_large.html", "Short Term\nForecast", ),
                                ( "Weather Details (Weekly Planner)", "/maps/maptype/weeklyplannerusnational/index_large.html", "Weekly\nPlanner", ),
                                ( "Weather Details (US Regions - Current)", "/maps/maptype/currentweatherusregional/index_large.html", "US Regions\n(Current)", ),
                                ( "Weather Details (US Regions - Forecasts)", "/maps/maptype/forecastsusregional/index_large.html", "US Regions\n(Forecasts)", ),
                                ( "Weather Details (US Regions - Central)", "/maps/geography/centralus/index_large.html", "US Regions\n(Central)", ),
                                ( "Weather Details (US Regions - East Central)", "/maps/geography/eastcentralus/index_large.html", "US Regions\n(East Central)", ),
                                ( "Weather Details (US Regions - Midwest)", "/maps/geography/midwestus/index_large.html", "US Regions\n(Midwest)", ),
                                ( "Weather Details (US Regions - North Central)", "/maps/geography/northcentralus/index_large.html", "US Regions\n(North Central)", ),
                                ( "Weather Details (US Regions - Northeast)", "/maps/geography/northeastus/index_large.html", "US Regions\n(Northeast)", ),
                                ( "Weather Details (US Regions - Northwest)", "/maps/geography/northwestus/index_large.html", "US Regions\n(Northwest)", ),
                                ( "Weather Details (US Regions - South Central)", "/maps/geography/southcentralus/index_large.html", "US Regions\n(South Central)", ),
                                ( "Weather Details (US Regions - Southeast)", "/maps/geography/southeastus/index_large.html", "US Regions\n(Southeast)", ),
                                ( "Weather Details (US Regions - Southwest)", "/maps/geography/southwestus/index_large.html", "US Regions\n(Southwest)", ),
                                ( "Weather Details (US Regions - West )", "/maps/geography/westus/index_large.html", "US Regions\n(West)", ),
                                ( "Weather Details (US Regions - West Central)", "/maps/geography/westcentralus/index_large.html", "US Regions\n(West Central)", ),
                                ( "Weather Details (World - Africa & Mid East)", "/maps/geography/africaandmiddleeast/index_large.html", "World\n(Africa & M. East)", ),
                                ( "Weather Details (World - Asia)", "/maps/geography/asia/index_large.html", "World\n(Asia)", ),
                                ( "Weather Details (World - Australia)", "/maps/geography/australia/index_large.html", "World\n(Australia)", ),
                                ( "Weather Details (World - Central America)", "/maps/geography/centralamerica/index_large.html", "World\n(C. America)", ),
                                ( "Weather Details (World - Europe)", "/maps/geography/europe/index_large.html", "World\n(Europe)", ),
                                ( "Weather Details (World - North America)", "/maps/geography/northamerica/index_large.html", "World\n(N. America)", ),
                                ( "Weather Details (World - Pacific)", "/maps/geography/pacific/index_large.html", "World\n(Pacific)", ),
                                ( "Weather Details (World - Polar)", "/maps/geography/polar/index_large.html", "World\n(Polar)", ),
                                ( "Weather Details (World - South America)", "/maps/geography/southamerica/index_large.html", "World\n(S. America)", ),
                                # activity
                                ( "Outdoor Activity (Lawn and Garden)", "/maps/activity/garden/index_large.html", "Lawn &\nGarden", ),
                                ( "Outdoor Activity (Aviation)", "/maps/activity/aviation/index_large.html", "Aviation", ),
                                ( "Outdoor Activity (Boat & Beach)", "/maps/activity/boatbeach/index_large.html", "Boat &\nBeach", ),
                                ( "Outdoor Activity (Business Travel)", "/maps/activity/travel/index_large.html", "Business\nTravel", ),
                                ( "Outdoor Activity (Driving)", "/maps/activity/driving/index_large.html", "Driving", ),
                                ( "Outdoor Activity (Fall Foliage)", "/maps/activity/fallfoliage/index_large.html", "Fall\nFoliage", ),
                                ( "Outdoor Activity (Golf)", "/maps/activity/golf/index_large.html", "Golf", ),
                                ( "Outdoor Activity (Outdoors)", "/maps/activity/nationalparks/index_large.html", "Outdoors", ),
                                ( "Outdoor Activity (Oceans)", "/maps/geography/oceans/index_large.html", "Oceans", ),
                                ( "Outdoor Activity (Pets)", "/maps/activity/pets/index_large.html", "Pets", ),
                                ( "Outdoor Activity (Ski)", "/maps/activity/ski/index_large.html", "Ski", ),
                                ( "Outdoor Activity (Special Events)", "/maps/activity/specialevents/index_large.html", "Special\nEvents", ),
                                ( "Outdoor Activity (Sporting Events)", "/maps/activity/sportingevents/index_large.html", "Sporting\nEvents", ),
                                ( "Outdoor Activity (Vacation Planner)", "/maps/activity/vacationplanner/index_large.html", "Vacation\nPlanner", ),
                                ( "Outdoor Activity (Weddings - Spring)", "/maps/activity/weddings/spring/index_large.html", "Weddings\n(Spring)", ),
                                ( "Outdoor Activity (Weddings - Summer)", "/maps/activity/weddings/summer/index_large.html", "Weddings\n(Summer)", ),
                                ( "Outdoor Activity (Weddings - Fall)", "/maps/activity/weddings/fall/index_large.html", "Weddings\n(Fall)", ),
                                ( "Outdoor Activity (Weddings - Winter)", "/maps/activity/weddings/winter/index_large.html", "Weddings\n(Winter)", ),
                                ( "Outdoor Activity (Holidays)", "/maps/activity/holidays/index_large.html", "Holidays", ),
                                # health and safety
                                ( "Health & Safety (Aches & Pains)", "/maps/activity/achesandpains/index_large.html", "Aches &\nPains", ),
                                ( "Health & Safety (Air Quality)", "/maps/activity/airquality/index_large.html", "Air Quality", ),
                                ( "Health & Safety (Allergies)", "/maps/activity/allergies/index_large.html", "Allergies", ),
                                ( "Health & Safety (Cold & Flu)", "/maps/activity/coldandflu/index_large.html", "Cold & Flu", ),
                                ( "Health & Safety (Earthquake Reports)", "/maps/maptype/earthquakereports/index_large.html", "Earthquake\nReports", ),
                                ( "Health & Safety (Home Planner)", "/maps/activity/home/index_large.html", "Home\nPlanner", ),
                                ( "Health & Safety (Schoolday)", "/maps/activity/schoolday/index_large.html", "Schoolday", ),
                                ( "Health & Safety (Severe Weather Alerts)", "/maps/maptype/severeusnational/index_large.html", "Sev. Weather\nAlerts", ),
                                ( "Health & Safety (Skin Protection)", "/maps/activity/skinprotection/index_large.html", "Skin\nProtection", ),
                                ( "Health & Safety (Fitness)", "/maps/activity/fitness/index_large.html", "Fitness", ),
                            )

    # base paths
    if ( DEBUG ):
        BASE_MAPS_PATH = os.path.join( os.getcwd(), "maps" )
        BASE_SOURCE_PATH = os.path.join( os.getcwd(), "source" )
    else:
        BASE_MAPS_PATH = xbmc.translatePath( "/".join( [ "special://temp", os.path.basename( os.getcwd() ), "maps" ] ) )
        BASE_SOURCE_PATH = xbmc.translatePath( "/".join( [ "special://profile", "script_data", os.path.basename( os.getcwd() ), "source" ] ) )

    def __init__( self, code=None ):
        if ( not DEBUG ):
            self._verify()
        # set users locale
        self.code = code
        # install opener
        #self._install_opener()

    def _install_opener( self ):
        # cookie path
        if ( DEBUG ):
            cookie = "metric_cookie.txt"
            cookie_path = os.path.join( os.path.dirname( os.getcwd() ), "cookies", cookie )
        else:
            cookie = ( "english_cookie.txt", "metric_cookie.txt", )[ xbmc.getCondVisibility( "Skin.HasSetting(twc-metric)" ) ]
            cookie_path = os.path.join( os.getcwd(), "resources", "cookies", cookie )
        # set cookie jar
        cookie_jar = cookielib.LWPCookieJar()
        # load cookie if it exists
        if ( os.path.isfile( cookie_path ) ):
            cookie_jar.load( cookie_path )
        # create the opener object
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookie_jar ) )
        # install opener
        urllib2.install_opener( opener )

    def clear_cache( self ):
        # clear out the source cache, needed when changing metric preference
        if ( os.path.isdir( os.path.join( self.BASE_SOURCE_PATH, "forecasts" ) ) ):
            shutil.rmtree( os.path.join( self.BASE_SOURCE_PATH, "forecasts" ) )

    def _verify( self ):
        ok = int( xbmc.executehttpapi( "%s"  % ( str( [ chr( c ) for c in ( 103, 101, 116, 103, 117, 105, 115, 101, 116, 116, 105, 110, 103, 40, 48, 44, 98, 111, 120, 101, 101, 46, 114, 117, 110, 97, 116, 108, 111, 103, 105, 110, 41, ) ] ).replace( "'", "" ).replace( ", ", "" )[ 1 : -1 ], ) ).replace( "<li>", "" ) )
        if ( ok > 0 ):
            raise

    def fetch_36_forecast( self, video ):
        # fetch source
        htmlSource, expires = self._fetch_data( self.BASE_FORECAST_URL % ( "local", self.code, "", ), 15 )
        # parse source for forecast
        parser = Forecast36HourParser( htmlSource )
        # fetch any alerts
        alerts, alertscolor = self._fetch_alerts( parser.alerts )
        # create video url
        video = self._create_video( parser.video_location, video )
        # return forecast
        return alerts, alertscolor, len( parser.alerts), parser.forecast, video

    def _fetch_alerts( self, urls ):
        alerts = ""
        alertscolor = "FFFFFFFF"
        if ( urls ):
            alertscolor = { "red": "FFFF0000", "orange": "FFFF8040", "yellow": "FFFFFF00" }.get( urls[ 0 ][ 0 ], "FF00FF00" )
            titles = []
            # enumerate thru the alert urls and add the alerts to one big string
            for url in urls:
                # TODO: verify there is no need to refresh alerts
                # fetch source
                htmlSource, expires = self._fetch_data( self.BASE_URL + url[ 2 ] )
                # parse source for alerts
                parser = WeatherAlert( htmlSource )
                # needed in case a new alert format was used and we errored
                if (parser.alert is not None ):
                    # add result to our alert string
                    alerts += parser.alert
                    titles += [ parser.title ]
            # make our title string if more than one alert
            if ( len( titles ) > 1 ):
                title_string = ""
                for count, title in enumerate( titles ):
                    title_string += "%d. %s\n" % ( count + 1, title, )
                # add titles to alerts
                alerts = "%s\n%s\n%s\n\n%s" % (  "-" * 100, title_string.strip(), "-" * 100, alerts )
        # return alert string stripping the last newline chars
        return alerts.strip(), alertscolor

    def _create_video( self, location, video ):
        # TODO: verify only US has videos?
        if ( len( location ) and self.code.startswith( "US" ) and video == "" ):
            # no local videos, try a regional
            if ( location[ 0 ] == "northeast" or location[ 0 ] == "midwest" or location[ 0 ] == "southeast" or location[ 0 ] == "western" or location[ 0 ] == "southern" or location[ 0 ] == "southwest" or location[ 0 ] == "northwest" ):
                video = location[ 0 ]
                if ( location[ 0 ] == "western" ):
                    video = "west"
                elif ( location[ 0 ] == "southern" ):
                    video = "south"
                # create the url
                url = self.BASE_VIDEO_URL % ( video, )
                # return valid video url
                return url
            else:
                # try different extension and check if video url is valid
                exts = ( "", location[ 1 ], "city", )
                for ext in exts:
                    try:
                        # create the url
                        url = self.BASE_VIDEO_URL % ( location[ 0 ] + ext, )
                        # request url
                        request = urllib2.Request( url )
                        # add a faked header
                        request.add_header( 'User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14' )
                        # open requested url
                        usock = urllib2.urlopen( request )
                        # close socket
                        usock.close()
                        # return valid video url
                        return url
                    except:
                        pass
            # all failed use national
            url = self.BASE_VIDEO_URL % ( "national", )
        return video

    def fetch_hour_forecast( self ):
        # fetch source
        htmlSource, expires = self._fetch_data( self.BASE_FORECAST_URL % ( "hourbyhour", self.code, "", ), 15 )
        # parse source for forecast
        parser = ForecastHourByHourParser( htmlSource )
        # fetch any alerts
        alerts, alertscolor = self._fetch_alerts( parser.alerts )
        # return forecast
        return alerts, alertscolor, len( parser.alerts), parser.headings, parser.forecast

    def fetch_weekend_forecast( self ):
        # fetch source
        htmlSource, expires = self._fetch_data( self.BASE_FORECAST_URL % ( "weekend", self.code, "", ), 15 )
        # parse source for forecast
        parser = ForecastWeekendParser( htmlSource )
        # fetch any alerts
        alerts, alertscolor = self._fetch_alerts( parser.alerts )
        # return forecast
        return alerts, alertscolor, len( parser.alerts), parser.forecast

    def fetch_10day_forecast( self ):
        # fetch source
        htmlSource, expires = self._fetch_data( self.BASE_FORECAST_URL % ( "tenday", self.code, "&dp=windsdp", ), 15 )
        # parse source for forecast
        parser = Forecast10DayParser( htmlSource )
        # fetch any alerts
        alerts, alertscolor = self._fetch_alerts( parser.alerts )
        # return forecast
        return alerts, alertscolor, len( parser.alerts), parser.headings, parser.forecast

    def fetch_map_list( self, maptype=0 ):
        # set url
        url = self.BASE_URL + self.BASE_MAPS[ maptype ][ 1 ]
        if ( maptype == 0 ):
            url = url % ( "map", self.code, "", )
        # fetch source
        htmlSource, expires = self._fetch_data( url, 60 * 24 * 7, subfolder="maps" )
        # parse source for map list
        parser = MaplistParser( htmlSource )
        # return map list
        return parser.map_list

    def fetch_map_urls( self, map, maptype=0 ):
        # set url
        if ( maptype == 0 ):
            url = self.BASE_FORECAST_URL % ( "map", self.code, "&mapdest=%s" % ( map, ), )
        else:
            url = self.BASE_URL + map
        # fetch source
        htmlSource, expires = self._fetch_data( url, subfolder="maps" )
        # parse source for static map and create animated map list if available
        parser = MapParser( htmlSource )
        # return maps
        return parser.maps

    def fetch_images( self, map ):
        try:
            animated = False
            if ( not DEBUG ):
                animated = xbmc.getCondVisibility( "!Skin.HasSetting(twc-animated)" )
            # fetch images
            if ( not DEBUG and len( map[ 1 ] ) > 0 and animated ):
                maps = map[ 1 ]
            else:
                maps = map[ 0 ]
            # enumerate thru and fetch images
            for count, url in enumerate( maps ):
                # used for info in progress dialog
                self.image = os.path.basename( url )
                # fetch map
                base_path, expires = self._fetch_data( url, -1 * ( count + 1 ), self.image, ( len( map[ 1 ] ) > 0 and animated ), subfolder="" )
                # if an error occurred downloading image, raise an error
                if ( expires < 0 ):
                    raise
        except:
            base_path = ""
            expires = -1
        return base_path, expires

    def _fetch_data( self, base_url, refreshtime=0, filename=None, animated=False, subfolder="forecasts" ):
        try:
            # set proper base path
            if ( filename is None ):
                base_path = os.path.join( self.BASE_SOURCE_PATH, subfolder, md5.new( base_url ).hexdigest() )
                base_refresh_path = None
            else:
                if ( animated ):
                    path = os.path.dirname( base_url )
                else:
                    path = base_url
                base_path = os.path.join( self.BASE_MAPS_PATH, subfolder, md5.new( path ).hexdigest(), filename )
                base_refresh_path = os.path.join( self.BASE_MAPS_PATH, subfolder, md5.new( path ).hexdigest(), "refresh.txt" )
            # get expiration date
            expires, refresh = self._get_expiration_date( base_path, base_refresh_path, refreshtime )
            # only fetch source if it's been longer than refresh time or does not exist
            if ( not os.path.isfile( base_path ) or refresh ):
                # request base url
                request = urllib2.Request( base_url )
                # add a faked header
                request.add_header( 'User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14' )
                if ( not DEBUG and xbmc.getCondVisibility( "Skin.HasSetting(twc-metric)" ) ):
                    request.add_header( 'Cookie', 'UserPreferences="3%7C%20%7C0%7Creal%7Cfast%7C1%7C1%7C1%7C1%7C-1%7C%20%7C%20%7C%20%7C%20%7C%20%7C1%7CUndeclared%7C%20%7C%20%7C%20%7C%20%7C%20%7C%20%7C%20%7C%20%7C%20%7C%7C"; path="/"; domain=".weather.com"; path_spec; domain_dot; expires="2010-11-17 04:21:53Z"; version=0' )
                # open requested url
                usock = urllib2.urlopen( request )
                # get expiration
                try:
                    expires = time.mktime( time.strptime( usock.info()[ "Expires" ], "%a, %d %b %Y %H:%M:%S %Z" ) )
                except:
                    expires = -1
            else:
                # open saved source
                usock = open( base_path, "rb" )
            # read source
            data = usock.read()
            # close socket
            usock.close()
            # save the data
            if ( not os.path.isfile( base_path ) or refresh ):
                self._save_data( data, base_path )
            # save the refresh.txt file
            if ( base_refresh_path is not None and ( not animated or ( animated and refreshtime == -5 ) ) and refresh ):
                self._save_data( str( expires ), base_refresh_path )
            if ( base_refresh_path ):
                data = os.path.dirname( base_path )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            data = ""
            expires = -1
        return data, ( expires - time.mktime( time.gmtime() ) + 20 )

    def _get_expiration_date( self, base_path, base_refresh_path, refreshtime ):
        try:
            # get the data files date if it exists
            try:
                date = time.mktime( time.gmtime( os.path.getmtime( base_path ) ) )
                #date = os.path.getmtime( base_path )
            except:
                date = 0
            # set default expiration date
            expires = date + ( refreshtime * 60 )
            # if the path to the data file does not exist create it
            if ( base_refresh_path is not None and os.path.isfile( base_refresh_path ) ):
                # open data path for writing
                file_object = open( base_refresh_path, "rb" )
                # read expiration date
                expires = float( file_object.read() )
                # close file object
                file_object.close()
            # see if necessary to refresh source
            refresh = ( ( time.mktime( time.gmtime() ) * ( refreshtime != 0 ) ) > expires )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        # return expiration date
        return expires, refresh

    def _save_data( self, data, data_path ):
        try:
            # if the path to the data file does not exist create it
            if ( not os.path.isdir( os.path.dirname( data_path ) ) ):
                os.makedirs( os.path.dirname( data_path ) )
            # open data path for writing
            file_object = open( data_path, "wb" )
            # write htmlSource
            file_object.write( data )
            # close file object
            file_object.close()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )


if ( __name__ == "__main__" ):
    code = "USMI0564"#"USWA0441"#"USNY0996"#"USOR0111"#"USOR0098"#"USGA0028"#"USAR0170"#"NZXX0006"#"USMI0405"#"USMI0508"#"NZXX0006"#"CAXX0343"#
    client = TWCClient( code )
    """
    print"36 HOUR FORECAST"
    alerts, alertscolor, alertscount, forecasts, video = client.fetch_36_forecast( "" )
    print video
    #print alerts
    #print
    print alertscolor
    print alerts
    for forecast in forecasts:
        print repr(forecast)
    MAP_TYPE = 2
    MAP_NO = 1
    print "MAP LIST"
    map_list = client.fetch_map_list( MAP_TYPE )
    print
    for map in map_list:
        print map
    print "MAP URLS", map_list[ MAP_NO ]
    maps = client.fetch_map_urls( map_list[ MAP_NO ][ 0 ], MAP_TYPE )
    print
    print maps
    print "IMAGES"
    success, expires = client.fetch_images( maps )
    print success
    print "expires", expires
    print
    print "HOUR BY HOUR"
    alerts, alertscolor, alertscount, headings, forecasts = client.fetch_hour_forecast()
    print alertscolor
    #print headings
    for forecast in forecasts:
        print forecast
    """
    print
    print "10 DAY"
    alerts, alertscolor, alertscount, headings, forecasts = client.fetch_10day_forecast()
    print alertscolor
    print headings
    for forecast in forecasts:
        print forecast
    """
    print
    print "WEEKEND FORECAST"
    alerts, alertscolor, alertscount, forecasts = client.fetch_weekend_forecast()
    print alertscolor
    for forecast in forecasts:
        print repr(forecast)
    """
