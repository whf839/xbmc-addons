"""
    weather.com api client module
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
from urllib import urlencode
import md5
import re
import time


# TODO: maybe use xbmc language strings for brief outlook translation
def _translate_text( text, translate ):
    # base babelfish url
    url = "http://babelfish.yahoo.com/translate_txt"
    try:
        # trick for translating T-Storms, TODO: verify if this is necessary
        text = text.replace( "T-Storms", "Thunderstorms" )
        # data dictionary
        data = { "ei": "UTF-8", "doit": "done", "fr": "bf-home", "intl": "1", "tt": "urltext", "trtext": text, "lp": translate, "btnTrTxt": "Translate" }
        # request url
        request = urllib2.Request( url, urlencode( data ) )
        # add a faked header, we use ie 8.0. it gives correct results for regex
        request.add_header( "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)" )
        # open requested url
        usock = urllib2.urlopen( request )
        # read htmlSource
        htmlSource = usock.read()
        # close socket
        usock.close()
        # find translated text
        text = re.findall( "<div id=\"result\"><div style=\"[^\"]+\">([^<]+)", htmlSource )[ 0 ]
    except Exception, e:
        # TODO: add error checking?
        pass
    # return translated text
    return text

def _normalize_outlook( outlook ):
    # if we're debugging xbmc module is not available
    tid = "F"
    sid = "mph"
    if ( not DEBUG ):
        tid = xbmc.getRegion( id="tempunit" )[ -1 ]
        sid = xbmc.getRegion( id="speedunit" )
    # enumerate thru and localize values
    for count, tmp_outlook in enumerate( outlook ):
        if ( tid == "C" ):
            # calculate the localized temp if C is required
            temps = re.findall( "[0-9]+F", tmp_outlook )
            for temp in temps:
                tmp_outlook = re.sub( temp, _localize_unit( temp ) + tid, tmp_outlook, 1 )
            # calculate the localized temp ranges if C is required
            temps = re.findall( "[low|mid|high]+ [0-9]+s", tmp_outlook )
            add = { "l": 3, "m": 6, "h": 9 }
            for temp in temps:
                new_temp = _localize_unit( str( int( re.findall( "[0-9]+", temp )[ 0 ] ) + add.get( temp[ 0 ], 3 ) ) )
                temp_int = int( float( new_temp ) / 10 ) * 10
                temp_rem = int( float( new_temp ) % 10 )
                temp_text = ( "low %ds", "mid %ds", "high %ds", )[ ( temp_rem >= 4 ) + ( temp_rem >= 6 ) ]
                tmp_outlook = re.sub( temp, temp_text % ( temp_int, ), tmp_outlook, 1 )
        if ( sid != "mph" ):
            # calculate the localized wind if C is required
            winds = re.findall( "[0-9]+ to [0-9]+ mph", tmp_outlook )
            for wind in winds:
                speeds = re.findall( "[0-9]+", wind )
                for speed in speeds:
                    wind = re.sub( speed, _localize_unit( speed, "speed" ).split( " " )[ 0 ], wind, 1 )
                tmp_outlook = re.sub( "[0-9]+ to [0-9]+ mph", wind.replace( "mph", sid ), tmp_outlook, 1 )
        # add our text back to the main variable
        outlook[ count ] = tmp_outlook
    # return normalized text
    return outlook

def _localize_unit( value, unit="temp" ):
    # grab the specifier
    value_specifier = value.split( " " )[ -1 ].upper()
    # replace any invalid characters
    value = value.replace( chr(176), "" ).replace( "&deg;", "" ).replace( "mph", "" ).replace( "miles", "" ).replace( "mile", "" ).replace( "in.", "" ).replace( "F", "" ).replace( "AM", "" ).replace( "PM", "" ).replace( "am", "" ).replace( "pm", "" ).strip()
    # do not convert invalid values
    if ( not value or value.startswith( "N/A" ) ):
        return value
    # time conversion
    if ( unit == "time" or unit == "time24" ):
        # format time properly
        if ( ":" not in value ):
            value += ":00"
        # set default time
        time = value
        # set our default temp unit
        id = ( "%H:%M", "%I:%M:%S %p", )[ unit == "time" ]
        # if we're debugging xbmc module is not available
        if ( not DEBUG and unit == "time" ):
            id = xbmc.getRegion( id="time" )
            # print id
        # 24 hour ?
        if ( id.startswith( "%H" ) ):
            hour = int( value.split( ":" )[ 0 ] )
            if (hour < 0 ):
               hour += 12
            hour += ( 12 * ( value_specifier == "PM" and int( value.split( ":" )[ 0 ] ) != 12 ) )
            hour -= ( 12 * ( value_specifier == "AM" and int( value.split( ":" )[ 0 ] ) == 12 ) )
            time = "%d:%s" % ( hour, value.split( ":" )[ 1 ], )
            # print "[Weather.com+] Converting Time : "+value + " " + value_specifier+ " -> " + time
        else : 
            hour = int( value.split( ":" )[ 0 ] )
            if (hour < 0 ):
               hour += 24

            if ( hour > 12 and value_specifier == value) :
                 value_specifier = "PM"
                 hour -= 12
            elif (value_specifier == value) :
                 value_specifier = "AM"
            # hour -= ( 12 * ( value_specifier == "PM" and int( value.split( ":" )[ 0 ] ) != 12 ) )
            time = "%d:%s" % ( hour, value.split( ":" )[ 1 ], )            
            if (unit == "time") :
                 time = "%s %s" % ( time, value_specifier, ) 
                 # print value + " -> " + time


        # add am/pm if used
        # if ( id.endswith( "xx" ) ):
            # time = "%s %s" % ( time, value_specifier, ) 
        # return localized time
        return time
    else:
        # we need a float
        value = float( value )
        # temp conversion
        if ( unit == "temp" or  unit == "tempdiff" ):
            # set our default temp unit
            id = "F"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = xbmc.getRegion( id="tempunit" )[ -1 ]
            # calculate the localized temp if C is required
            if ( id == "C" ):
                # C/F difference or temperature conversion
                if ( unit == "tempdiff" ):
                    # 9 degrees of F equal 5 degrees of C
                    value = round( float( 5 * value ) / 9 )
                else:
                    # convert to celcius
                    value = round( ( value - 32 ) * ( float( 5 ) / 9 ) )
            # return localized temp
            return "%s%d" % ( ( "", "+", )[ value >= 0 and unit == "tempdiff" ], value )
        # speed conversion
        elif ( unit == "speed" ):
            # set our default temp unit
            id = "mph"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = xbmc.getRegion( id="speedunit" )
            # calculate the localized speed
            if ( id == "km/h" ):
                value = round( value * 1.609344 )
            elif ( id == "m/s" ):
                value = round( value * 0.45 )
            elif ( id == "ft/min" ):
                value = round( value * 88 )
            elif ( id == "ft/s" ):
                value = round( value * 1.47 )
            elif ( id == "yard/s" ):
                value = round( value * 0.4883 )
            # return localized speed
            return "%d %s" % ( value, id, )
        # depth conversion
        elif ( unit == "depth" ):
            # set our default depth unit
            id = "in."
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "in.", "cm.", )[ xbmc.getRegion( id="tempunit" )[ -1 ] == "C" ]
            # calculate the localized depth
            if ( id == "cm." ):
                value = float( value * 2.54 )
            # return localized depth
            return "%.2f %s" % ( value, id, )
        # pressure conversion
        elif ( unit == "pressure" ):
            # set our default pressure unit
            id = "in."
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "in.", "mb.", )[ xbmc.getRegion( id="tempunit" )[ -1 ] == "C" ]
            # calculate the localized pressure
            if ( id == "mb." ):
                value = float( value * 33.8637526 )
            # return localized pressure
            return "%.2f %s" % ( value, id, )
        # distance conversion
        elif ( unit == "distance" ):
            # set our default distance unit
            id = "mile"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "kilometer", "mile", )[ xbmc.getRegion( id="speedunit" ) == "mph" ]
            # calculate the localized distance
            if ( id == "kilometer" ):
                value = float( value * 1.609344 )
            # pluralize for values != 1
            if ( value != 1.0 ):
                id += "s"
            # return localized distance
            return "%.1f %s" % ( value, id, )

def _english_localize_unit( value, unit="temp" ):
    # grab the specifier
    value_specifier = value.split( " " )[ -1 ].upper()
    # replace any invalid characters
    value = value.replace( chr(176), "" ).replace( "&deg;", "" ).replace( "km/h", "" ).replace( "kilometers", "" ).replace( "kilometer", "" ).replace("km", "").replace( "mb", "" ).replace( "C", "" ).replace( "AM", "" ).replace( "PM", "" ).replace( "am", "" ).replace( "pm", "" ).strip()
    # do not convert invalid values
    if ( not value or value.startswith( "N/A" ) ):
        return value
    # time conversion
    if ( unit == "time" or unit == "time24" ):
        # format time properly
        if ( ":" not in value ):
            value += ":00"
        # set default time
        time = value
        # set our default temp unit
        id = ( "%H:%M", "%I:%M:%S %p", )[ unit == "time" ]
        # if we're debugging xbmc module is not available
        if ( not DEBUG and unit == "time" ):
            id = xbmc.getRegion( id="time" )
            # print id
        # 24 hour ?
        if ( id.startswith( "%H" ) ):
            hour = int( value.split( ":" )[ 0 ] )
            if (hour < 0 ):
               hour += 12
            hour += ( 12 * ( value_specifier == "PM" and int( value.split( ":" )[ 0 ] ) != 12 ) )
            hour -= ( 12 * ( value_specifier == "AM" and int( value.split( ":" )[ 0 ] ) == 12 ) )
            time = "%d:%s" % ( hour, value.split( ":" )[ 1 ], )
            # print "[Weather.com+] Converting Time : "+value + " " + value_specifier+ " -> " + time
        else : 
            hour = int( value.split( ":" )[ 0 ] )
            if (hour < 0 ):
               hour += 24

            if ( hour > 12 and value_specifier == value) :
                 value_specifier = "PM"
                 hour -= 12
            elif (value_specifier == value) :
                 value_specifier = "AM"
            # hour -= ( 12 * ( value_specifier == "PM" and int( value.split( ":" )[ 0 ] ) != 12 ) )
            time = "%d:%s" % ( hour, value.split( ":" )[ 1 ], )            
            if (unit == "time") :
                 time = "%s %s" % ( time, value_specifier, ) 
                 # print value + " -> " + time


        # add am/pm if used
        # if ( id.endswith( "xx" ) ):
            # time = "%s %s" % ( time, value_specifier, ) 
        # return localized time
        return time
    else:
        # we need a float
        value = float( value )
        # temp conversion
        if ( unit == "temp" or  unit == "tempdiff" ):
            # set our default temp unit
            id = "C"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = xbmc.getRegion( id="tempunit" )[ -1 ]
            # calculate the localized temp if C is required
            if ( id == "F" ):
                # C/F difference or temperature conversion
                if ( unit == "tempdiff" ):
                    # 9 degrees of F equal 5 degrees of C
                    value = round( float( 9 * value ) / 5 )
                else:
                    # convert to F
                    value = round( float( value * 1.8 ) + 32 )
            # return localized temp
            return "%s%d" % ( ( "", "+", )[ value >= 0 and unit == "tempdiff" ], value )
        # speed conversion
        elif ( unit == "speed" ):
            # set our default temp unit
            id = "km/h"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = xbmc.getRegion( id="speedunit" )
            # calculate the localized speed
            if ( id == "mph" ):
                value = round( value * 0.621371 )
            elif ( id == "m/s" ):
                value = round( value * 0.277778 )
            elif ( id == "ft/min" ):
                value = round( value * 0.911344 * 60 )
            elif ( id == "ft/s" ):
                value = round( value * 0.911344 )
            elif ( id == "yard/s" ):
                value = round( value * 0.333333 * 0.911344 )
            # return localized speed
            return "%d %s" % ( value, id, )
        # depth conversion
        elif ( unit == "depth" ):
            # set our default depth unit
            id = "cm."
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "in.", "cm.", )[ xbmc.getRegion( id="tempunit" )[ -1 ] == "C" ]
            # calculate the localized depth
            if ( id == "in." ):
                value = float( value * 0.393701 )
            # return localized depth
            return "%.2f %s" % ( value, id, )
        # pressure conversion
        elif ( unit == "pressure" ):
            # set our default pressure unit
            id = "mb."
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "in.", "mb.", )[ xbmc.getRegion( id="tempunit" )[ -1 ] == "C" ]
            # calculate the localized pressure
            if ( id == "in." ):
                value = float( value * 0.02953 )
            # return localized pressure
            return "%.2f %s" % ( value, id, )
        # distance conversion
        elif ( unit == "distance" ):
            # set our default distance unit
            id = "kilometer"
            # if we're debugging xbmc module is not available
            if ( not DEBUG ):
                id = ( "kilometer", "mile", )[ xbmc.getRegion( id="speedunit" ) == "mph" ]
            # calculate the localized distance
            if ( id == "mile" ):
                value = float( value * 0.621371 )
            # pluralize for values != 1
            if ( value != 1.0 ):
                id += "s"
            # return localized distance
            return "%.1f %s" % ( value, id, )

class WeatherAlert:
    def __init__( self, htmlSource ):
        self.alert = ""
        self.title = ""
        self.alert_rss = ""
        try:            
            self._get_alert( htmlSource )
        except:
            pass

    def _get_alert( self, htmlSource ):
        # regex patterns

        # pattern_alert = "<h1>([^<]+)</h1>"      
        # pattern_issuedby = "<p class=\"alIssuedBy\">(.+?)</p>"
        pattern_narrative = "<p class=\"alNarrative\">(.*?)</p>"
        # pattern_expires = "<p>(<b>.+?</b>[^<]+)</p>" 
        
        pattern_moreinfo = "<h2>([^<]+)</h2>\n.+?<p class=\"alSynopsis\">"
        pattern_synopsis = "<p class=\"alSynopsis\">(.+?)</p>"
        
        pattern_alert_ = "</span>([^<]+)</h2>"
        pattern_issuedby_ = "Issued by (.+?)</h3>"
        pattern_narrative_ = "\.\.\. (.*?)<br class=\"clear-content\">"
        pattern_expires_ = "<h3 class=\"twc-module-sub-header twc-timestamp twc-alert-timestamp\">([^<]+)</h3>"

        # fetch alert
        alert = re.findall( pattern_alert_, htmlSource )[ 0 ].replace("\n", "").replace("\t","")

        # fetch expires
        try:
            expires = re.findall( pattern_expires_, htmlSource )[ 0 ].replace( "\n", "" ).replace( "\t", "" )
        except:
            expires = ""
        # TODO : localizing expire time?
        expires = ""
        # fetch issued by
        try:
            issuedby_list = re.findall( pattern_issuedby_, htmlSource, re.DOTALL )[ 0 ].split( "<br>" )
            issuedby = "[I]Issued by "
            for item in issuedby_list:
                issuedby += item.strip()
                issuedby += "\n"
            issuedby += "[/I]"
            # fetch narrative
	    narrative = ""
 	    description_list = re.findall( pattern_narrative, htmlSource, re.DOTALL )
	    if (not len(description_list)):
	        description_list = re.findall( pattern_narrative_, htmlSource, re.DOTALL )
		narrative = "... "
            
            for item in description_list:
                narrative += "%s\n\n" % ( item.strip().replace("\n", "").replace("\t","").replace("</p>","\n\n").replace("<p>","").replace("</div>","").replace("<h2>","").replace("</h2>",""), )
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
            # we use this for adding titles at the begining of the alerts text for multiple alerts
            self.title = "[B]%s[/B]" % ( alert, )
            # set the alert rss
            self.alert_rss = "[COLOR=rss_headline]%s:[/COLOR] %s %s - %s" % ( alert, alert, expires, issuedby.replace( "\n", " " ), )
        except:
            self.alert = None
            self.title = ""
            self.alert_rss = ""

class Forecast36HourParser:
    def __init__( self, htmlSource, htmlSource_5, localtime, translate=None ):
        self.forecast = []
        self.extras = []
        self.alerts = []
        self.alertscolor = []
        self.video_location = []
        self.translate = translate
        self.sun = []

        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource, htmlSource_5, localtime )

    def _get_forecast( self, htmlSource, htmlSource_5, localtime ):
        # regex patterns
        pattern_locstate = "wx.config.loc.state=\"([^\"]+)\""
        pattern_video_location = "US_Current_Weather:([^\"]+)\""
        pattern_video_local_location = "/outlook/videos/(.+?)-60-second-forecast-(.+?)\""
        pattern_alert_color = "alert-bullet-(.+?)\"></div>"
        pattern_alerts = "location.href='/weather/alerts/(.+?)'"
        pattern_days = "<td class=\"twc-col-[0-9]+ twc-forecast-when\">(.+?)</td>"
        pattern_icon = "<img src=\"http://s\.imwx\.com/v\.20100719\.135915/img/wxicon/[0-9]+/([0-9]+)\.png\" width=\"72\""
        pattern_forecast_brief = "<td class=\"twc-col-[0-9]+\">(.+?)</td>"
        pattern_temp_info = "<td class=\"twc-col-[0-9]+ twc-forecast-temperature-info\">(.+?)</td>"
        pattern_temp = "<td class=\"twc-col-[0-9]+ twc-forecast-temperature\"><strong>(.+?)\&deg;</strong>"
        pattern_precip_title = "Chance of ([^\:]+):"
        pattern_precip_amount = "<br><strong>(.+?)</strong>"
        #pattern_outlook = "</td><!-- Column [0-9]+ -->\n\s<td class=\"twc-col-[0-9]+\">(.+?)</td>"
        pattern_daylight = "<td class=\"twc-col-[0-9]+ twc-line-daylight\">(.+?)<strong>\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\s(.+?)\n"
        pattern_pressure = "Pressure:</span>(.+?)<img src=\"http://s.imwx.com/v.20100719.135915/img/common/icon-(.+?).gif\""	                     
        pattern_visibility = "Visibility:</span>(.+?)</td>"	        
        # pattern_sunrise_now = "Time Until Sunrise: <strong>(.+?)</strong>"
        # pattern_sunset_now = "Daylight Remaining: <strong>(.+?)</strong>"
        pattern_sunrise_now = "Sunrise:</span> <br><strong>\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\s(.+?)\n"
        pattern_sunset_now = "Sunset:</span> <br><strong>\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\s(.+?)\n"
					
        # fetch days
        days = re.findall( pattern_days, htmlSource )
        # print "Tonight = "+days[0]+" Tomorrow = "+days[1]
        # enumerate thru and combine the day with it's forecast
        if ( len( days ) ):
            try:
                # fetch state
                locstate = re.findall( pattern_locstate, htmlSource )[ 0 ].lower()
               
            except:
                pass
            
            # fetch video location
            # print htmlSource
            vl = re.findall( pattern_video_location, htmlSource )
            vl2 = re.findall( pattern_video_local_location, htmlSource )
            print vl, vl2
            try :
                if (vl2 is not None) : 
                   self.video_local_location = vl2[0][0]
                   self.video_local_number = vl2[0][1]
                else :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            except :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            try :
                if (vl is not None) :
                   self.video_location = vl [0]
                else :
                   self.video_location = "Non US"
            except :
                self.video_location = "Non US"
            print "[Weather.com+] video_location : "+self.video_location + " Local_location : " + self.video_local_location
            # fetch alerts
            self.alertscolor += re.findall(pattern_alert_color, htmlSource)
            self.alerts = re.findall( pattern_alerts, htmlSource )
            
            # fetch icon
            icon = re.findall( pattern_icon, htmlSource )
            # fetch brief description
            brief = re.findall( pattern_forecast_brief, htmlSource )
            # fetch temperature
            temperature = re.findall( pattern_temp, htmlSource )
            temperature_info = re.findall( pattern_temp_info, htmlSource)
	  # fetch precip title
            precip_title = re.findall( pattern_precip_title, htmlSource )
            # print precip_title
            # fetch precip title
            precip_amount = re.findall( pattern_precip_amount, htmlSource )
            # fetch forecasts
            #outlook = re.findall( pattern_outlook, htmlSource )
            # fetch daylight
            daylight = re.findall( pattern_daylight, htmlSource )
            sunrise_ = re.findall( pattern_sunrise_now, htmlSource_5)
            sunset_ =  re.findall( pattern_sunset_now, htmlSource_5)
            try : 
               time_diff = int(sunrise_[ 0 ].split( " " )[ 3 ][:2])-localtime
            except :
               time_diff = 0
            # print str(int(sunrise_[ 0 ].split( " " )[ 3 ][:2]))+" asdasd "+ str(localtime)
            print "[Weather.com+] Timezone : " + str(time_diff)
            
            # fetch extra info
            pressure_ = re.findall( pattern_pressure, htmlSource, re.DOTALL )
            visibility_ = re.findall( pattern_visibility, htmlSource, re.DOTALL )
            # sun_ = re.findall( pattern_sun, htmlSource, re.DOTALL )
            # sun = []
            pressure = "N/A"
            visibility = "N/A"
            sunrise = "N/A"
            sunset = "N/A"
            
            if ( pressure_ ) :
                    pressure = "".join(pressure_[0][0].split("\n"))
                    pressure = "".join(pressure.split("\t"))
                    pressure = pressure.replace("in", "")
                    # pressure = pressure + { "pressure-up": u"\u2191", "pressure-down": u"\u2193", "pressure-steady": u"\u2192" }[ pressure_[0][1] ]
                    try : 
                       print "[Weather.com+] pressure : " + pressure_[0][1]
                    except :
                       print "[Weather.com+] there's no info about pressure-up or down"                     
            if ( visibility_ ) :
                   visibility = "".join(visibility_[0].split("\n"))
                   visibility = "".join(visibility.split("\t"))
                   visibility = visibility.replace("mi", "")
                   # print visibility
            if ( sunrise_ ) :
                   sunrise = "".join(sunrise_[0].split("\n"))
                   sunrise = "".join(sunrise.split("\t"))
                   # print sunrise
                   try : 
                      sunrise = _localize_unit( str(int(sunrise.split(" ")[3].split(":")[0])-time_diff) + ":" + sunrise.split(" ")[3].split(":")[1], "time" )
                   except :
                      sunrise = "N/A"
            if ( sunset_ ) :
                   sunset = "".join(sunset_[0].split("\n"))
                   sunset = "".join(sunset.split("\t"))
                   try : 
                      sunset = _localize_unit( str(int(sunset.split(" ")[3].split(":")[0])-time_diff) + ":" + sunset.split(" ")[3].split(":")[1], "time" )
                   except :
                      sunset = "N/A"
            print "[Weather.com+] pressure : "+pressure
            if ( pressure == "N/A" ) :
                   self.extras += [(pressure, _localize_unit(visibility, "distance"), sunrise, sunset)]
            elif ( pressure == pressure.replace("mb", "") ) :
                   self.extras += [(_localize_unit(pressure, "pressure") + { "pressure-up": u"\u2191", "pressure-down": u"\u2193", "pressure-steady": u"\u2192" }[ pressure_[0][1] ], _localize_unit(visibility, "distance"), sunrise, sunset)]
            else :  
                   self.extras += [(pressure + { "pressure-up": u"\u2191", "pressure-down": u"\u2193", "pressure-steady": u"\u2192" }[ pressure_[0][1] ], _localize_unit(visibility, "distance"), sunrise, sunset)]

            # localize our extra info
            # convert outlook wind/temp values
            brief = _normalize_outlook( brief )
            # translate brief and outlook if user preference
            if ( self.translate is not None ):
                # we only need outlook and brief. the rest the skins or xbmc language file can handle
                # we separate each item with single pipe
                # text = "|".join( outlook )
                # separator for different info
                # text += "|||||"
                # we separate each item with single pipe
                text = "|".join( brief )
                # translate text
                text = _translate_text( text, self.translate )
                # split text into it's original list
                # outlook = text.split( "|||||" )[ 0 ].split( "|" )
                brief = text.split( "|" )
            for count, day in enumerate( days ):
                # make icon path
                try :
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", icon[ count ] + ".png" ] )
                except :
                  print "[Weather.com+] Icon is not available"
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", "0.png" ] ) 
                # add result to our class variable
                # self.forecast += [ ( days, iconpath, brief[ count ], temperature[ count ][ 0 ], _localize_unit( temperature[ count ][ 1 ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), outlook[ count ].strip(), daylight[ count ].split( ": " )[ 0 ], _localize_unit( daylight[ count ].split( ": " )[ 1 ], "time" ), ) ]
                # print days[count]
                # print iconpath
                # print brief[ count+1 ]
                # print temperature_info[ count ]
                # print _localize_unit( temperature[ count ] )
                # print precip_title[ count ]
                # print precip_amount[ count ].replace( "%", "" )
                # print brief[ count+4 ]
                # print daylight[ count ][ 0 ]
                # print "[Weather.com+] " + _localize_unit( str(int(daylight[count][1].split(" ")[3].split(":")[0])-time_diff) + ":" + daylight[count][1].split(" ")[3].split(":")[1], "time"  )
                try :
                  print "[Weather.com+] " + days[count]
                except :
                  print "[Weather.com+] days["+str(count)+"] is not available"
                  days += [ ("N/A", ) ]              
                print "[Weather.com+] " + iconpath
                try :
                  print "[Weather.com+] " + brief[ count+1 ]
                except :
                  print "[Weather.com+] iconpath is not available"
                  brief += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + temperature_info[ count ]
                except :
                  print "[Weather.com+] temperature_info["+str(count)+"] is not available"
                  temperature_info += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( temperature[ count ] )
                except :
                  print "[Weather.com+] temperature["+str(count)+"] is not available"
                  temperature += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_title[ count ]
                except :
                  print "[Weather.com+] precip_title["+str(count)+"] is not available"
                  precip_title += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_amount[ count ].replace( "%", "" )
                except :
                  print "[Weather.com+] precip_amount["+str(count)+"] is not available"
                  precip_amount += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + brief[ count+4 ]
                except :
                  print "[Weather.com+] brief["+str(count+4)+"] is not available"
                  brief += [ ("N/A", "N/A", "N/A", "N/A", ) ]
                try :
                  print "[Weather.com+] " + daylight[ count ][ 0 ]
                except :
                  print "[Weather.com+] daylight["+str(count)+"] is not available"
                  daylight += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( str(int(daylight[count][1].split(" ")[3].split(":")[0])-time_diff) + ":" + daylight[count][1].split(" ")[3].split(":")[1], "time"  )
                except :
                  print "[Weather.com+] daylight["+str(count)+"] is not available"
                  daylight += [ ("00:00", ) ]

                self.forecast += [ ( days[count], iconpath, brief[ count+1 ], temperature_info[ count ], _localize_unit( temperature[ count ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), brief[ count+4 ], daylight[ count ][ 0 ], _localize_unit( str(int(daylight[count][1].split(" ")[3].split(":")[0])-time_diff) + ":" + daylight[count][1].split(" ")[3].split(":")[1], "time"  ), ) ]

class ACCU_Forecast36HourParser:
    def __init__( self, htmlSource, htmlSource_1, htmlSource_2, translate=None ):
        self.forecast = []
        self.extras = []
        self.alerts = []
        self.alertscolor = []
        self.video_location = []
        self.translate = translate
        self.sun = []

        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource, htmlSource_1, htmlSource_2 )

    def _get_forecast( self, htmlSource, htmlSource_1, htmlSource_2 ):
        # regex patterns
        # pattern_video_location = ""
        # pattern_video_local_location = ""
        # pattern_alert_color = ""
        # pattern_alerts = ""
        # pattern_days = ""
        pattern_icon = "/wxicons/87x79_blue/([0-9]+)_int.jpg"
	pattern_current_brief = "<span id=\"ctl00_cphContent_lblCurrentText\" style=\"display: block; font-size: 11px;line-height: 17px;\">(.+?)</span>"
        pattern_forecast_brief = "<span id=\"ctl00_cphContent_lbl(.+?)Text\">(.+?)</span>"
	pattern_temp = "<span id=\"ctl00_cphContent_lbl(.+?)Value\">(.+?)\&deg"
	pattern_current_temp = "<span id=\"ctl00_cphContent_lblCurrentTemp\" style=\"display: block; font-weight: bold;font-size: 18px; line-height: 24px;\">(.+?)\&deg"
	pattern_current_feel_like = "<span id=\"ctl00_cphContent_lblRealFeelValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)\&deg"
	pattern_current_time = "<span id=\"ctl00_cphContent_lblCurrentTime\" style=\"display: block; font-size: 11px;line-height: 17px;\">(.+?)</span>"
	pattern_current_wind = "<span id=\"ctl00_cphContent_lblWindsValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
	pattern_current_humidity = "<span id=\"ctl00_cphContent_lblHumidityValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
	pattern_current_dew = "<span id=\"ctl00_cphContent_lblDewPointValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)\&deg"
	# pattern_precip_title = "Chance of ([^\:]+):"
        # pattern_precip_amount = "<br><strong>(.+?)</strong>"
        # pattern_outlook = "</td><!-- Column [0-9]+ -->\n\s<td class=\"twc-col-[0-9]+\">(.+?)</td>"
        # pattern_daylight = "<td class=\"twc-col-[0-9]+ twc-line-daylight\">(.+?)<strong>\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\s(.+?)\n"
        pattern_pressure = "<span id=\"ctl00_cphContent_lblPressureValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"	                     
        pattern_visibility = "<span id=\"ctl00_cphContent_lblVisibilityValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"	        
        pattern_current_sunrise = "<span id=\"ctl00_cphContent_lblSunRiseValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
        pattern_current_sunset = "<span id=\"ctl00_cphContent_lblSunSetValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
	pattern_sunrise = "Sunrise: (.+?)</span>"
	pattern_sunset = "Sunset: (.+?)</span>"
					
        # fetch icons
	icon = []
	icondir = {"1":"32", "2":"30", "3":"28", "4":"30", "5":"34", "6":"28", "7":"26", "8":"26", "11":"19", "12":"11", "13":"39", "14":"39", "15":"3", "16":"37", "17":"37", "18":"12", "19":"14", "20":"14", "21":"14", "22":"16", "23":"16", "24":"25", "25":"25", "26":"25", "29":"25", "30":"36", "31":"32", "32":"23", "33":"31", "34":"29", "35":"27", "36":"27", "38":"27", "37":"33", "39":"45", "40":"45", "41":"47", "42":"47", "43":"46", "44":"46" }
	current_icon = "/".join( [ "special://temp", "weather", "128x128", icondir.get( re.findall( pattern_icon, htmlSource )[0] ) + ".png" ] )
	icon_day1 = re.findall( pattern_icon, htmlSource_1 )
	icon_day2 = re.findall( pattern_icon, htmlSource_2 )
	icon = [ icondir.get(icon_day1[0]), icondir.get(icon_day1[1]), icondir.get(icon_day2[0]), icondir.get(icon_day2[1]) ]
	        
        # enumerate thru and combine the day with it's forecast
        if ( len( icon ) ):
	    """
            # fetch video location
            vl = re.findall( pattern_video_location, htmlSource )
            vl2 = re.findall( pattern_video_local_location, htmlSource )
            print vl, vl2
            try :
                if (vl2 is not None) : 
                   self.video_local_location = vl2[0][0]
                   self.video_local_number = vl2[0][1]
                else :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            except :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            try :
                if (vl is not None) :
                   self.video_location = vl [0]
                else :
                   self.video_location = "Non US"
            except :
                self.video_location = "Non US"
            print "[Weather.com+] video_location : "+self.video_location + " Local_location : " + self.video_local_location

            # fetch alerts
            self.alertscolor += re.findall(pattern_alert_color, htmlSource)
            self.alerts = re.findall( pattern_alerts, htmlSource )       
	    """
            
            # fetch brief description
            current_brief = re.findall( pattern_current_brief, htmlSource )[0]
	    day1_brief = re.findall( pattern_forecast_brief, htmlSource_1 )
	    day2_brief = re.findall( pattern_forecast_brief, htmlSource_2 )
	    if ( day1_brief is not None and day2_brief is not None):
		brief = [ day1_brief[0][1], day1_brief[1][1], day2_brief[0][1], day2_brief[1][1] ]
	    else:
		brief = [ "", "", "", "" ]
            # fetch temperature
            current_temp = _english_localize_unit( re.findall( pattern_current_temp, htmlSource )[0] )
	    current_feel_like = _english_localize_unit( re.findall( pattern_current_feel_like, htmlSource )[0] )
            day1_temp = re.findall( pattern_temp, htmlSource_1 )
	    day2_temp = re.findall( pattern_temp, htmlSource_2 )
	    temperature_info = ["High", "Low", "High", "Low"]
	    temperature = [ day1_temp[0][1], day1_temp[2][1], day2_temp[0][1], day2_temp[2][1] ]
	    # fecth current infos
	    current_humidity = re.findall( pattern_current_humidity, htmlSource )[0]
	    current_dew = _english_localize_unit( re.findall( pattern_current_dew, htmlSource )[0] )
	    current_wind = re.findall( pattern_current_wind, htmlSource )[0]
	    if ( current_wind.split(" ")[-1] == "km/h" ):
		current_wind = current_wind.split(" ")[0]+" "+_english_localize_unit( current_wind.split(" ")[1], "speed" )

	    """
	    # fetch precip title
            precip_title = re.findall( pattern_precip_title, htmlSource )
            # fetch precip title
            precip_amount = re.findall( pattern_precip_amount, htmlSource )
            # fetch forecasts
            #outlook = re.findall( pattern_outlook, htmlSource )
	    """

	    precip_title = []
	    precip_amount = []

            # fetch sunrise and sunset
	    try:
	        current_sunrise = _localize_unit( re.findall( pattern_current_sunrise, htmlSource)[0], "time" )
	    except:
		current_sunrise = "N/A"
	    try:
		current_sunset = _localize_unit( re.findall( pattern_current_sunset, htmlSource)[0], "time" )                      
	    except:
		current_sunset = "N/A"
	    try:
		sunrise = re.findall( pattern_sunrise, htmlSource_2 )[0]
	    except:
		sunrise = "N/A"
	    try:
	        sunset = re.findall( pattern_sunset, htmlSource_2 )[0]
	    except:
	        sunset = "N/A"
	    daylight = [ ("Sunrise", current_sunrise), ("Sunset", current_sunset), ("Sunrise", sunrise), ("Sunset", sunset) ]
            # fetch extra info
	    try:
		pressure = _english_localize_unit( re.findall( pattern_pressure, htmlSource, re.DOTALL )[0], "pressure" )
	    except:
		pressure = "N/A"
	    try:
		visibility = _english_localize_unit( re.findall( pattern_visibility, htmlSource, re.DOTALL )[0], "distance" )
	    except:
		visibility = "N/A"
            # print "[Weather.com+] pressure : " + pressure
	    self.extras += [( pressure, visibility, current_sunrise, current_sunset, current_temp, current_feel_like, current_brief, current_wind, current_humidity, current_dew, current_icon )]
	    # am or pm now?
            try: 
	        current_time = re.findall( pattern_current_time, htmlSource )[0]
	    except:
	        current_time = xbmc.getInfoLabel("System.Time")
	    ampm = 0
	    if ( current_time.split(" ")[1] == "PM" ):
		ampm = 1	    
	    # print "[Weather.com+] Current Time : " + current_time
	    days = ["Today", "Tonight", "Tomorrow", "Tomorrow Night"]
            for count in range(0, 3):
                # make icon path
                try :
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", icon[ count+ampm ] + ".png" ] )
                except :
                  print "[Weather.com+] Icon is not available"
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", "0.png" ] ) 
                # add result to our class variable
                # self.forecast += [ ( days, iconpath, brief[ count ], temperature[ count ][ 0 ], _localize_unit( temperature[ count ][ 1 ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), outlook[ count ].strip(), daylight[ count ].split( ": " )[ 0 ], _localize_unit( daylight[ count ].split( ": " )[ 1 ], "time" ), ) ]
                # print days[count]
                # print iconpath
                # print brief[ count+1 ]
                # print temperature_info[ count ]
                # print _localize_unit( temperature[ count ] )
                # print precip_title[ count ]
                # print precip_amount[ count ].replace( "%", "" )
                # print brief[ count+4 ]
                # print daylight[ count ][ 0 ]
                # print "[Weather.com+] " + _localize_unit( str(int(daylight[count][1].split(" ")[3].split(":")[0])-time_diff) + ":" + daylight[count][1].split(" ")[3].split(":")[1], "time"  )
                print "[Weather.com+] " + days[count+ampm]          
                print "[Weather.com+] " + iconpath
		# print daylight
                try :
                  print "[Weather.com+] " + brief[ count+1 ]
                except :
                  print "[Weather.com+] iconpath is not available"
                  brief += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + temperature_info[ count ]
                except :
                  print "[Weather.com+] temperature_info["+str(count)+"] is not available"
                  temperature_info += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( temperature[ count ] )
                except :
                  print "[Weather.com+] temperature["+str(count)+"] is not available"
                  temperature += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_title[ count ]
                except :
                  print "[Weather.com+] precip_title["+str(count)+"] is not available"
                  precip_title += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_amount[ count ].replace( "%", "" )
                except :
                  print "[Weather.com+] precip_amount["+str(count)+"] is not available"
                  precip_amount += [ "N/A" ]
                try :
                  print "[Weather.com+] " + brief[ count+ampm ]
                except :
                  print "[Weather.com+] brief["+str(count+ampm)+"] is not available"
                  brief += [ ("N/A", "N/A", "N/A", "N/A", ) ]
                try :
                  print "[Weather.com+] " + daylight[ count+ampm ][ 0 ]
                except :
                  print "[Weather.com+] daylight["+str(count+ampm)+"] is not available"
                  daylight += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( daylight[ count+ampm ][ 1 ], "time"  )
                except :
                  print "[Weather.com+] daylight["+str(count+ampm)+"] is not available"
                  daylight += [ ("00:00", ) ]

                self.forecast += [ ( days[count+ampm], iconpath, "", temperature_info[ count ], _english_localize_unit( temperature[ count ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), brief[ count+ampm ], daylight[ count+ampm ][ 0 ], _localize_unit( daylight[ count+ampm ][ 1 ], "time"  ), ) ]

class NOAA_Forecast36HourParser:
    def __init__( self, htmlSource, htmlSource_2, translate=None ):
        self.forecast = []
        self.extras = []
        self.alerts = []
        self.alertscolor = []
        self.video_location = []
        self.translate = translate
        self.sun = []

        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource, htmlSource_2 )

    def _get_forecast( self, htmlSource, htmlSource_2 ):
	# print "Fetching 36 Hour..."
        # regex patterns
        # pattern_video_location = ""
        # pattern_video_local_location = ""
        # pattern_alert_color = ""
        # pattern_alerts = ""
        # pattern_days = ""
	pattern_temperature = "Temp</font></a><br /><font style=\"font-size:18px\">([0-9]+)\&deg;</font>"
	pattern_icon = "<img width=\"50\" height=\"50\" src=\"http://forecast.weather.gov/images/wtf/(.+?).jpg\""
        # pattern_info = "<td width=\"11\%\"><b>(.+?)</b><br><img src=\"/images/wtf/(.+?).jpg\" width=\"55\" height=\"58\" alt=\"[^\"]+\" title=\"[^\"]+\" ><br>(.+?)<br>(.+?)<br>(.+?) <font color=\"[^\"]+\">([0-9]+) \&deg;F</font></td>"
        pattern_forecast_brief = "<td class=\"weekly_weather\">(.+?)</td>"
	pattern_current_info = "<span class=\"obs_wxtmp\"> (.+?)<br />([0-9]+)\&deg;</span>"
	pattern_current_info_2 = "<span class=\"obs_wxtmp\">(.+?)<br />([0-9]+)\&deg;</span>"
	pattern_current_feel_like = "<td><b>Wind Chill</b>:</td>[^<]+<td align=\"right\">(.+?)</td>"
	# pattern_current_time = "<span id=\"ctl00_cphContent_lblCurrentTime\" style=\"display: block; font-size: 11px;line-height: 17px;\">(.+?)</span>"
	pattern_current_wind = "<td><b>Wind Speed</b>:</td>[^<]+<td align=\"right\">(.+?)</td>"
	pattern_current_humidity = "<td><b>Humidity</b>:</td>[^<]+<td align=\"right\">(.+?) \%</td>"
	pattern_current_dew = "<td><b>Dewpoint</b>:</td>[^<]+<td align=\"right\">(.+?)</td>"
	# pattern_precip_title = "Chance of ([^\:]+):"
        pattern_precip_amount = "no-repeat;\">([0-9]+)\%</td><td class=\"weekly_wind\">"
        # pattern_outlook = "</td><!-- Column [0-9]+ -->\n\s<td class=\"twc-col-[0-9]+\">(.+?)</td>"
        # pattern_daylight = "<td class=\"twc-col-[0-9]+ twc-line-daylight\">(.+?)<strong>\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\s(.+?)\n"
        pattern_pressure = "<td><b>Barometer</b>:</td>[^<]+<td align=\"right\" nowrap>(.+?)</td>"	                     
        pattern_visibility = "<td><b>Visibility</b>:</td>[^<]+<td align=\"right\">(.+?)</td>"	        
        # pattern_current_sunrise = "<span id=\"ctl00_cphContent_lblSunRiseValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
        # pattern_current_sunset = "<span id=\"ctl00_cphContent_lblSunSetValue\" class=\"fltRight\" style=\"width: 80px; display: block;\">(.+?)</span>"
	# pattern_sunrise = "Sunrise: (.+?)</span>"
	# pattern_sunset = "Sunset: (.+?)</span>"
	
	# fetch icons
	icons = re.findall( pattern_icon, htmlSource_2 )
	icon = [ icons[-11], icons[-10], icons[-9] ]

        # enumerate thru and combine the day with it's forecast
        if ( len( icon ) ):
	    """
            # fetch video location
            vl = re.findall( pattern_video_location, htmlSource )
            vl2 = re.findall( pattern_video_local_location, htmlSource )
            print vl, vl2
            try :
                if (vl2 is not None) : 
                   self.video_local_location = vl2[0][0]
                   self.video_local_number = vl2[0][1]
                else :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            except :
                   self.video_local_location = "Not Available"
                   self.video_local_number = ""
            try :
                if (vl is not None) :
                   self.video_location = vl [0]
                else :
                   self.video_location = "Non US"
            except :
                self.video_location = "Non US"
            print "[Weather.com+] video_location : "+self.video_location + " Local_location : " + self.video_local_location

            # fetch alerts
            self.alertscolor += re.findall(pattern_alert_color, htmlSource)
            self.alerts = re.findall( pattern_alerts, htmlSource )       
	    """
            
            # fetch brief description
	    current_info = re.findall( pattern_current_info, htmlSource_2 )
	    if ( len(current_info) ):
		current_brief = current_info[0][0]
	    else:
		current_info = re.findall ( pattern_current_info_2, htmlSource_2 )
		current_brief = current_info[0][0]
            
	    brief = re.findall( pattern_forecast_brief, htmlSource_2 )   

            # fetch temperature
            current_temp = current_info[0][1]
	    current_feel_like = "N/A"
	    temp = re.findall( pattern_temperature, htmlSource_2 )
	    temperature_info = ["High", "Low", "High", "Low"]
	    temperature = [ temp[0], temp[1], temp[2] ]

	    # fecth current infos
	    current_humidity = re.findall( pattern_current_humidity, htmlSource )[0]
	    current_dew = re.findall( pattern_current_dew, htmlSource )[0]
	    current_wind = re.findall( pattern_current_wind, htmlSource )[0]
	    try:
		current_wind = current_wind.split(" ")[0]+" "+_localize_unit( current_wind.split(" ")[1], "speed" ).replace(" mph","").replace(" km/h","") +" Gust "+_localize_unit( current_wind.split(" ")[3], "speed" )
	    except:	
		current_wind = current_wind.split(" ")[0]+" "+_localize_unit( current_wind.split(" ")[1], "speed" )
	
            # fetch precip
            precip_amount = re.findall( pattern_precip_amount, htmlSource_2 )
	    print precip_amount, htmlSource

            # fetch forecasts
            # outlook = re.findall( pattern_outlook, htmlSource )

            # fetch extra info
	    try:
		pressure = re.findall( pattern_pressure, htmlSource, re.DOTALL )[0].replace("&quot;","\"")
	    except:
		pressure = "N/A"
	    try:
		visibility = _localize_unit( re.findall( pattern_visibility, htmlSource, re.DOTALL )[0].replace("mi.","miles"), "distance" )
	    except:
		visibility = "N/A"
            # print "[Weather.com+] pressure : " + pressure, visibility
	    self.extras += [( pressure, visibility, current_sunrise, current_sunset, current_temp, current_feel_like, current_brief, current_wind, current_humidity, current_dew, current_icon )]
	    # am or pm now?
            try: 
	        current_time = re.findall( pattern_current_time, htmlSource )[0]
	    except:
	        current_time = xbmc.getInfoLabel("System.Time")
	    ampm = 0
	    if ( current_time.split(" ")[1] == "PM" ):
		ampm = 1	    
	    # print "[Weather.com+] Current Time : " + current_time
	    days = ["Today", "Tonight", "Tomorrow", "Tomorrow Night"]
            for count in range(0, 3):
                # make icon path
                try :
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", icon[ count+ampm ] + ".png" ] )
                except :
                  print "[Weather.com+] Icon is not available"
                  iconpath = "/".join( [ "special://temp", "weather", "128x128", "0.png" ] ) 
                # add result to our class variable
                # self.forecast += [ ( days, iconpath, brief[ count ], temperature[ count ][ 0 ], _localize_unit( temperature[ count ][ 1 ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), outlook[ count ].strip(), daylight[ count ].split( ": " )[ 0 ], _localize_unit( daylight[ count ].split( ": " )[ 1 ], "time" ), ) ]
                # print days[count]
                # print iconpath
                # print brief[ count+1 ]
                # print temperature_info[ count ]
                # print _localize_unit( temperature[ count ] )
                # print precip_title[ count ]
                # print precip_amount[ count ].replace( "%", "" )
                # print brief[ count+4 ]
                # print daylight[ count ][ 0 ]
                # print "[Weather.com+] " + _localize_unit( str(int(daylight[count][1].split(" ")[3].split(":")[0])-time_diff) + ":" + daylight[count][1].split(" ")[3].split(":")[1], "time"  )
                print "[Weather.com+] " + days[count+ampm]          
                print "[Weather.com+] " + iconpath
		# print daylight
                try :
                  print "[Weather.com+] " + brief[ count+1 ]
                except :
                  print "[Weather.com+] iconpath is not available"
                  brief += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + temperature_info[ count ]
                except :
                  print "[Weather.com+] temperature_info["+str(count)+"] is not available"
                  temperature_info += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( temperature[ count ] )
                except :
                  print "[Weather.com+] temperature["+str(count)+"] is not available"
                  temperature += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_title[ count ]
                except :
                  print "[Weather.com+] precip_title["+str(count)+"] is not available"
                  precip_title += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + precip_amount[ count ].replace( "%", "" )
                except :
                  print "[Weather.com+] precip_amount["+str(count)+"] is not available"
                  precip_amount += [ "N/A" ]
                try :
                  print "[Weather.com+] " + brief[ count+ampm ]
                except :
                  print "[Weather.com+] brief["+str(count+ampm)+"] is not available"
                  brief += [ ("N/A", "N/A", "N/A", "N/A", ) ]
                try :
                  print "[Weather.com+] " + daylight[ count+ampm ][ 0 ]
                except :
                  print "[Weather.com+] daylight["+str(count+ampm)+"] is not available"
                  daylight += [ ("N/A", ) ]
                try :
                  print "[Weather.com+] " + _localize_unit( daylight[ count+ampm ][ 1 ], "time"  )
                except :
                  print "[Weather.com+] daylight["+str(count+ampm)+"] is not available"
                  daylight += [ ("00:00", ) ]

                self.forecast += [ ( days[count+ampm], iconpath, "", temperature_info[ count ], _english_localize_unit( temperature[ count ] ), precip_title[ count ], precip_amount[ count ].replace( "%", "" ), brief[ count+ampm ], daylight[ count+ampm ][ 0 ], _localize_unit( daylight[ count+ampm ][ 1 ], "time"  ), ) ]


class ForecastHourlyParser:
    def __init__( self, htmlSource, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        # pattern_headings = "<div class=\"hbhTD[^\"]+\"><div title=\"[^>]+>([^<]+)</div></div>"
        pattern_date = "<div class=\"hbhDateHeader\">([^<]+)</div>"
        pattern_sunrise = "<img src=\"http://i.imwx.com/web/local/hourbyhour/icon_sunrise.gif\"[^>]+>([^<]+)"
        pattern_sunset = "<img src=\"http://i.imwx.com/web/local/hourbyhour/icon_sunset.gif\"[^>]+>([^<]+)"
        # use this to grab the 15 minutes details
        # pattern_info = "<div class=\"hbhTDTime[^>]+><div>([^<]+)</div></div>\
        # use this to grab only 1 hour details
        pattern_info = "<div class=\"hbhTDTime\"><div>([^<]+)</div></div>\
[^<]+<div class=\"hbhTDConditionIcon\"><div><img src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/(gray/)?([0-9]+).gif\"[^>]+></div></div>\
[^<]+<div class=\"hbhTDCondition\"><div><b>([^<]+)</b><br>([^<]+)</div></div>\
[^<]+<div class=\"hbhTDFeels\"><div>([^<]*)</div></div>\
[^<]+<div class=\"hbhTDPrecip\"><div>([^<]*)</div></div>\
[^<]+<div class=\"hbhTDHumidity\"><div>([^<]*)</div></div>\
[^<]+<div class=\"hbhTDWind\"><div>([^<]*)(<br>)?([^<]*)</div></div>"
        """
        pattern_time = "<div class=\"hbhTDTime[^>]+><div>([^<]+)</div>"
        pattern_icon = "<div class=\"hbhTDConditionIcon\"><div><img src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/(gray/)?([0-9]+).gif\""
        pattern_brief = "<div class=\"hbhTDCondition\"><div><b>([^<]+)</b><br>([^<]+)</div>"
        pattern_feels = "<div class=\"hbhTDFeels\"><div>([^<]*)</div>"
        pattern_precip = "<div class=\"hbhTDPrecip\"><div>([^<]*)</div>"
        pattern_humidity = "<div class=\"hbhTDHumidity\"><div>([^<]*)</div>"
        pattern_wind = "<div class=\"hbhTDWind\"><div>([^<]*)<br>([^<]*)</div>"
        """
        # fetch info
        info = re.findall( pattern_info, htmlSource )
        # fetch dates
        dates = re.findall( pattern_date, htmlSource )
        # hack for times when weather.com, does not display date
        dates += [ ", " ]
        # fetch sunrise
        sunrises = re.findall( pattern_sunrise, htmlSource )
        # fetch sunset
        sunsets = re.findall( pattern_sunset, htmlSource )
        # enumerate thru and create heading and forecast
        if ( len( info ) ):
            # we convert wind direction to full text
            windir = {    
                            "From N": "From the North",
                            "From NNE": "From the North Northeast",
                            "From NE": "From the Northeast",
                            "From ENE": "From the East Northeast",
                            "From E": "From the East",
                            "From ESE": "From the East Southeast",
                            "From SE": "From the Southeast",
                            "From SSE": "From the South Southeast",
                            "From S": "From the South",
                            "From SSW": "From the South Southwest",
                            "From SW": "From the Southwest",
                            "From WSW": "From the West Southwest",
                            "From W": "From the West",
                            "From WNW": "From the West Northwest",
                            "From NW": "From the Northwest",
                            "From NNW": "From the North Northwest"
                        }
            brief = []
            wind = []
            for item in info:
                wind += [ windir.get( item[ 8 ], item[ 8 ] ) ]
                brief += [ item[ 4 ] ]
            # translate brief and outlook if user preference
            if ( self.translate is not None ):
                # we only need outlook and brief. the rest the skins or xbmc language file can handle
                # we separate each item with single pipe
                text = "|".join( wind )
                # separator for different info
                text += "|||||"
                # we separate each item with single pipe
                text += "|".join( brief )
                # translate text
                text = _translate_text( text, self.translate )
                # split text into it's original list
                wind = text.split( "|||||" )[ 0 ].split( "|" )
                brief = text.split( "|||||" )[ 1 ].split( "|" )
            # counter for date
            date_counter = 0
            # create our forecast list
            for count, item in enumerate( info ):
                # make icon path
                iconpath = "/".join( [ "special://temp", "weather", "128x128", item[ 2 ] + ".png" ] )
                # do we need to increment date_counter
                if ( item[ 0 ] == "12 am" and count > 0 ):
                    date_counter += 1
                # does sunrise/sunset fit in this period
                sunrise = ""
                sunset = ""
                # we want 24 hour as the math is easier
                period = _localize_unit( item[ 0 ], "time24" )
                # set to a high number, we use this for checking next time period
                period2 = "99:00"
                if ( count < len( info ) - 2 ):
                    period2 = _localize_unit( info[ count + 1 ][ 0 ], "time24" )
                    period2 = ( period2, "24:%s" % ( period2.split( ":" )[ 1 ], ), )[ period2.split( ":" )[ 0 ] == "0" ]
                # sunrise
                if ( sunrises ):
                    # get the 24 hour sunrise time
                    sunrise_check = _localize_unit( sunrises[ 0 ].strip().split( "Sunrise" )[ 1 ].strip(), "time24" )
                    # if in the correct time range, set our variable
                    if ( int( sunrise_check.split( ":" )[ 0 ] ) == int( period.split( ":" )[ 0 ] ) and int( sunrise_check.split( ":" )[ 1 ] ) >= int( period.split( ":" )[ 1 ] ) and 
                        ( int( sunrise_check.split( ":" )[ 1 ] ) < int( period2.split( ":" )[ 1 ] ) or int( sunrise_check.split( ":" )[ 0 ] ) < int( period2.split( ":" )[ 0 ] ) ) ):
                        sunrise = _localize_unit( sunrises[ 0 ].strip().split( "Sunrise" )[ 1 ].strip(), "time" )
                # sunset
                if ( sunsets ):
                    # get the 24 hour sunset time
                    sunset_check = _localize_unit( sunsets[ 0 ].strip().split( "Sunset" )[ 1 ].strip(), "time24" )
                    # if in the correct time range, set our variable
                    if ( int( sunset_check.split( ":" )[ 0 ] ) == int( period.split( ":" )[ 0 ] ) and int( sunset_check.split( ":" )[ 1 ] ) >= int( period.split( ":" )[ 1 ] ) and 
                        ( int( sunset_check.split( ":" )[ 1 ] ) < int( period2.split( ":" )[ 1 ] ) or int( sunset_check.split( ":" )[ 0 ] ) < int( period2.split( ":" )[ 0 ] ) ) ):
                        sunset = _localize_unit( sunsets[ 0 ].strip().split( "Sunset" )[ 1 ].strip(), "time" )
                # add result to our class variable
                self.forecast += [ ( _localize_unit( item[ 0 ], "time" ), dates[ date_counter ].split( ", " )[ -1 ], iconpath, _localize_unit( item[ 3 ] ), brief[ count ], _localize_unit( item[ 5 ] ), item[ 6 ].replace( "%", "" ), item[ 7 ].replace( "%", "" ), wind[ count ], _localize_unit( item[ 10 ], "speed" ), item[ 8 ].split( " " )[ -1 ], sunrise, sunset, ) ]

class ACCU_ForecastHourlyParser:
    def __init__( self, htmlSource, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
	pattern_date = "([0-9]+)/([0-9]+)/20"
        pattern_info = "<div class=\".+?textBold\">([^<]+)</div>"
	pattern_brief = "<div class=\".+?hbhWxText\">([^<]+)</div>"
	pattern_icon = "wxicons/31x24/(.+?).gif"
	pattern_wind = "winds/24x24/(.+?).gif"
        # fetch info
	date = re.findall( pattern_date, htmlSource )
        raw_info = re.findall( pattern_info, htmlSource )
	raw_brief = re.findall( pattern_brief, htmlSource )
	icon = re.findall( pattern_icon, htmlSource )
	wind = re.findall( pattern_wind, htmlSource )
	info_ = []
	info = []
	brief = []
	dates = [ ( date[0][0], date[0][1] ), ( date[3][0], date[3][1] ) ]
	for item in raw_info:
	    info_ += [ item.replace("\n","").replace("\r","").replace("\t","").replace("&deg;C", "") ]
	for item in raw_brief:
	    brief += [ item.replace("\n","").replace("\r","").replace("\t","").replace("&deg;C", "") ]
	icondir = {"1":"32", "2":"30", "3":"28", "4":"30", "5":"34", "6":"28", "7":"26", "8":"26", "11":"19", "12":"11", "13":"39", "14":"39", "15":"3", "16":"37", "17":"37", "18":"12", "19":"14", "20":"14", "21":"14", "22":"16", "23":"16", "24":"25", "25":"25", "26":"25", "29":"25", "30":"36", "31":"32", "32":"23", "33":"31", "34":"29", "35":"27", "36":"27", "38":"27", "37":"33", "39":"45", "40":"45", "41":"47", "42":"47", "43":"46", "44":"46" }       
	# we convert wind direction to full text
        windir = {    
                            "N": "From the North",
                            "NNE": "From the North Northeast",
                            "NE": "From the Northeast",
                            "ENE": "From the East Northeast",
                            "E": "From the East",
                            "ESE": "From the East Southeast",
                            "SE": "From the Southeast",
                            "SSE": "From the South Southeast",
                            "S": "From the South",
                            "SSW": "From the South Southwest",
                            "SW": "From the Southwest",
                            "WSW": "From the West Southwest",
                            "W": "From the West",
                            "WNW": "From the West Northwest",
                            "NW": "From the Northwest",
                            "NNW": "From the North Northwest"
		}
	for count in range(0, 7):
	    info += [ ( info_[count], icondir.get( icon[count] ), brief[count], info_[count+7], info_[count+14], info_[count+21], info_[count+28], windir.get( wind[count] ), info_[count+35], info_[count+42] ) ]
	for count in range(49, 56):
	    info += [ ( info_[count], icondir.get( icon[count-43] ), brief[count-43], info_[count+7], info_[count+14], info_[count+21], info_[count+28], windir.get( wind[count-43] ), info_[count+35], info_[count+42] ) ]
        if ( len( info ) ):
            # counter for date
            date_counter = 0
            # create our forecast list
            for count, item in enumerate( info ):
                # make icon path
                iconpath = "/".join( [ "special://temp", "weather", "128x128", item[ 1 ] + ".png" ] )
                # do we need to increment date_counter
                if ( item[ 0 ] == "12:00 AM" and count > 0 ):
                    date_counter += 1
                # does sunrise/sunset fit in this period
                sunrise = ""
                sunset = ""
                # we want 24 hour as the math is easier
                period = _localize_unit( item[ 0 ], "time24" )
                # set to a high number, we use this for checking next time period
                period2 = "99:00"
                if ( count < len( info ) - 2 ):
                    period2 = _localize_unit( info[ count + 1 ][ 0 ], "time24" )
                    period2 = ( period2, "24:%s" % ( period2.split( ":" )[ 1 ], ), )[ period2.split( ":" )[ 0 ] == "0" ]
                # add result to our class variable
                self.forecast += [ ( _localize_unit( item[ 0 ], "time" ), " ".join( dates[ date_counter ] ), iconpath, _english_localize_unit( item[ 3 ] ), item[ 2 ], _english_localize_unit( item[ 4 ] ), item[ 9 ].replace( "%", "" ), item[ 6 ].replace( "%", "" ), item[ 7 ], _english_localize_unit( item[ 8 ], "speed" ), item[ 7 ].split( " " )[ -1 ], "", "", ) ]



class ForecastWeekendParser:
    def __init__( self, htmlSource, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        pattern_heading = "from=[\"]*weekend[\"]+>([^<]+)</A>.*\s.*\s\
[^<]+<TD width=\"[^\"]+\" class=\"wkndButton[A-Z]+\" align=\"[^\"]+\" valign=\"[^\"]+\"><FONT class=\"[^\"]+\">([^\&]+)&nbsp;.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s\
[^>]+>[^>]+>([^<]+)<"
        pattern_observed = ">(Observed:)+"
        pattern_brief = "<IMG src=\"http://(?:i.imwx.com)?(?:image.weather.com)?/web/common/wxicons/(?:pastwx/)?[0-9]+/([0-9]+).gif.*alt=\"([^\"]+)\""
        pattern_past = "<TD align=\"left\" class=\"grayFont10\">([^<]+)</TD>"
        pattern_past2 = "<TD align=\"[left|right]+\" class=\"blueFont10\">[<B>]*<FONT color=\"[^\"]+\">([^\s|^<]+)[^\n]+"
        pattern_avg = "<tr><td align=\"right\" valign=\"top\" CLASS=\"blueFont10\">([^<]+)<.*\s.*\s[^[A-Z0-9]+(.*&deg;[F|C]+)"
        pattern_high = "<FONT class=\"[^\"]+\">([^<]+)<BR><FONT class=\"[^\"]+\"><NOBR>([^<]+)</FONT></NOBR>"
        pattern_low = "<FONT class=\"[^\"]+\">([^<]+)</FONT><BR><FONT class=\"[^\"]+\"><B>([^<]+)</B></FONT>"
        pattern_precip = "<TD valign=\"top\" width=\"50%\" class=\"blueFont10\" align=\"[left|right]+\">(.*)"
        pattern_wind = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)</td><td align=\"[^\"]+\">&nbsp;</td><td valign=\"[^\"]+\" CLASS=\"[^\"]+\"><B>.*\n[^A-Z]+([A-Z]+)<br>([^<]+)</B>"
        pattern_uv = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)</td>\s[^>]+>[^>]+>[^>]+><B>([^<]+)"
        pattern_humidity = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)[^>]+>[^>]+>[^>]+>[^>]+><B>([0-9]+%)"
        pattern_daylight = "<td align=\"[^\"]+\" valign=\"[^\"]+\" CLASS=\"[^\"]+\">([^<]+)[^>]+>[^>]+>[^>]+>[^>]+><B>([0-9]+:[0-9]+[^<]+)</B></td>"
        pattern_outlook = "<TD colspan=\"3\" class=\"blueFont10\" valign=\"middle\" align=\"left\">([^<]+)</TD>"
        pattern_departures = "<FONT COLOR=\"#7d8c9f\"><B>\s.*\s\s+(.+?F)"
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
        # fetch departue from normal
        departures = re.findall( pattern_departures, htmlSource )
        for i in range( 6 - len( departures ) ):
            departures.append( "" )
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
        tmp_winds = re.findall( pattern_wind, htmlSource )
        # insert necessary dummy entries
        for i in range( 3 - len( tmp_winds ) ):
            tmp_winds.insert( 0, ( "", "", "", ) )
        winds = []
        for i in range( len( tmp_winds ) ):
            if ( tmp_winds[ i ][ 0 ] != "" ):
                winds += [ ( tmp_winds[ i ][ 0 ], "%s at %s" % ( tmp_winds[ i ][ 1 ], _localize_unit( tmp_winds[ i ][ 2 ].split()[ 1 ], "speed" ), ) ), ]
            else:
                winds += [ ( "", "", ) ]
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
        # separate briefs
        brief = []
        icon = []
        for item in briefs:
            brief += [ item[ 1 ] ]
            icon += [ item[ 0 ] ]
        # convert outlook wind/temp values
        # normalize turned off due to variety of expressions : 'upper', 'single digits', etc.
        # TODO : getting most expressions covered
        # outlooks = _normalize_outlook( outlooks )
        # translate brief and outlook if user preference
        if ( self.translate is not None ):
            # we only need outlook and brief. the rest the skins or xbmc language file can handle
            # we separate each item with single pipe
            text = "|".join( outlooks )
            # separator for different info
            text += "|||||"
            # we separate each item with single pipe
            text += "|".join( brief )
            # translate text
            text = _translate_text( text, self.translate )
            # split text into it's original list
            outlooks = text.split( "|||||" )[ 0 ].split( "|" )
            brief = text.split( "|||||" )[ 1 ].split( "|" )
        # no need to run if none found
        if ( len( headings ) ):
            # set our previous variables to the first items
            prevday = int( headings[ 0 ][ 1 ].split( " " )[ -1 ] )
            prevmonth = headings[ 0 ][ 1 ].split( " " )[ 0 ]
            # use a dictionary for next month
            nextmonth = { "Jan": "Feb", "Feb": "Mar", "Mar": "Apr", "Apr": "May", "May": "Jun", "Jun": "Jul", "Jul": "Aug", "Aug": "Sep", "Sep": "Oct", "Oct": "Nov", "Nov": "Dec", "Dec": "Jan" }
            # enumerate thru and create our forecast list
            for count, ( day, date, alert, ) in enumerate( headings ):
                # add a month to the date
                month = date.split( " " )[ 0 ]
                mday = int( date.split( " " )[ -1 ] )
                # month change
                if ( mday < prevday ):
                    prevmonth = nextmonth[ prevmonth ]
                # set the new date
                date = "%s %d" % ( prevmonth, mday, )
                prevday = mday
                # if no icon, set it to na
                if ( not briefs[ count ][ 0 ] ):
                    pass
                # make icon path
                iconpath = "/".join( [ "special://temp", "weather", "128x128", icon[ count ] + ".png" ] )
                # add result to our class variable
                self.forecast += [ ( day, date, iconpath, brief[ count ], highs[count][ 0 ], _localize_unit( highs[ count ][ 1 ] ),
                lows[ count ][ 0 ], _localize_unit( lows[ count ][ 1 ] ), precips[ count * 2 ], precips[ count * 2 + 1 ].replace( "%", "" ).replace( "<B>", "" ).replace( "</B>", "" ),
                winds[ count ][ 0 ], winds[ count ][ 1 ], uvs[ count ][ 0 ], uvs[ count ][ 1 ],
                humids[ count ][ 0 ], humids[ count ][ 1 ].replace( "%", "" ), daylights[ count * 2 ][ 0 ], _localize_unit( daylights[ count * 2 ][ 1 ], "time" ), daylights[ count * 2 + 1 ][ 0 ],
                _localize_unit( daylights[ count * 2 + 1 ][ 1 ], "time" ), outlooks[ count ], observeds[ count ], pasts[ count * 3 + 2 ].split( "&nbsp;" )[ 0 ], _localize_unit( pasts[ count * 3 + 2 ].split( "&nbsp;" )[ 1 ], "depth" ),
                avgs[ count * 4 ][ 0 ], _localize_unit( avgs[ count * 4 ][ 1 ] ), avgs[ count * 4 + 1 ][ 0 ], _localize_unit( avgs[ count * 4 + 1 ][ 1 ] ),
                avgs[ count * 4 + 2 ][ 0 ], _localize_unit( avgs[ count * 4 + 2 ][ 1 ] ), avgs[ count * 4 + 3 ][ 0 ], _localize_unit( avgs[ count * 4 + 3 ][ 1 ] ),
                alert.strip(), _localize_unit( departures[ count * 2 ], "tempdiff" ), _localize_unit( departures[ count * 2 + 1 ], "tempdiff" ), ) ]


class ACCU_Forecast10DayParser:
    def __init__( self, htmlSource_1, htmlSource_2, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource_1 and htmlSource_2 ):
            self._get_forecast( htmlSource_1, htmlSource_2 )

    def _get_forecast( self, htmlSource_1, htmlSource_2 ):
        # regex patterns
        pattern_day = "Day_ctl0[0-9]+_lblDate\">(.+?)</span>"
	pattern_outlook = "Day_ctl0[0-9]+_lblDesc\">(.+?)</span>"
        pattern_hightemp = "Day_ctl0[0-9]+_lblHigh\">(.+?)\&deg;"
	pattern_lowtemp = "Night_ctl0[0-9]+_lblHigh\">(.+?)\&deg;"
        pattern_icon = "/wxicons/87x79_blue/([0-9]+)_int.jpg"

	icondir = {"1":"32", "2":"30", "3":"28", "4":"30", "5":"34", "6":"28", "7":"26", "8":"26", "11":"19", "12":"11", "13":"39", "14":"39", "15":"3", "16":"37", "17":"37", "18":"12", "19":"14", "20":"14", "21":"14", "22":"16", "23":"16", "24":"25", "25":"25", "26":"25", "29":"25", "30":"36", "31":"32", "32":"23", "33":"31", "34":"29", "35":"27", "36":"27", "38":"27", "37":"33", "39":"45", "40":"45", "41":"47", "42":"47", "43":"46", "44":"46" }

        # fetch info
	htmlSource = htmlSource_1 + htmlSource_2
        days = re.findall( pattern_day, htmlSource )
	outlook = re.findall( pattern_outlook, htmlSource )
	hightemp = re.findall( pattern_hightemp, htmlSource )
	lowtemp = re.findall( pattern_lowtemp, htmlSource )
	icon = re.findall( pattern_icon, htmlSource )
	# enumerate thru and create heading and forecast
	for count, day in enumerate(days):
            if (count<7):
		iconpath = "/".join( [ "special://temp", "weather", "128x128", icondir.get( icon[count] ) + ".png" ] )
	    else:
	        iconpath = "/".join( [ "special://temp", "weather", "128x128", icondir.get( icon[count+7] ) + ".png" ] )
	    self.forecast += [ ( day.split(" ")[0], day.split(" ")[1], iconpath, outlook[count], _english_localize_unit( hightemp[count] ), _english_localize_unit( lowtemp[count] ), "N/A", "N/A", "N/A", "N/A" ) ]

class Forecast10DayParser:
    def __init__( self, htmlSource, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
        # regex patterns
        pattern_headings = "<p id=\"tdHead[A-Za-z]+\">(.*)</p>"
        pattern_headings2 = "<OPTION value=\"windsdp\" selected>([^<]+)</OPTION>"
        pattern_info = "<p><[^>]+>([^<]+)</a><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s\
[^<]+<p><img src=\"http://i.imwx.com/web/common/wxicons/[0-9]+/([0-9]+).gif[^>]+><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s[^<]+<p><strong>([^<]+)</strong><br>([^<]+)</p>\s.*\s.*\s.*\s.*\s.*\s[^<]+<p>([^<]+)</p>\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s[^<]+<td><p>([^<]+)</p></td>\s.*\s.*\s\
[^<]+<[^<]+<[^<]+<[^<]+<strong>([^<]+</strong>[^<]+)</p>"
        # fetch info
        info = re.findall( pattern_info, htmlSource )
        # enumerate thru and create heading and forecast
        if ( len( info ) ):
            # we convert wind direction to abbreviated text for ShortWindDirection property
            windir = {    
                            "From the North": "N",
                            "From the North Northeast": "NNE",
                            "From the Northeast": "NE",
                            "From the East Northeast": "ENE",
                            "From the East": "E",
                            "From the East Southeast": "ESE",
                            "From the Southeast": "SE",
                            "From the South Southeast": "SSE",
                            "From the South": "S",
                            "From the South Southwest": "SSW",
                            "From the Southwest": "SW",
                            "From the West Southwest": "WSW",
                            "From the West": "W",
                            "From the West Northwest": "WNW",
                            "From the Northwest": "NW",
                            "From the North Northwest": "NNW"
                        }
            brief = []
            wind = []
            for item in info:
                wind += [ item[ 7 ] ]
                brief += [ item[ 3 ] ]
            # translate brief and outlook if user preference
            if ( self.translate is not None ):
                # we only need outlook and brief. the rest the skins or xbmc language file can handle
                # we separate each item with single pipe
                text = "|".join( wind )
                # separator for different info
                text += "|||||"
                # we separate each item with single pipe
                text += "|".join( brief )
                # translate text
                text = _translate_text( text, self.translate )
                # split text into it's original list
                wind = text.split( "|||||" )[ 0 ].split( "|" )
                brief = text.split( "|||||" )[ 1 ].split( "|" )
            # create our forecast list
            for count, item in enumerate( info ):
                # make icon path
                iconpath = "/".join( [ "special://temp", "weather", "128x128", item[ 2 ] + ".png" ] )
                # add result to our class variable
                self.forecast += [ ( item[ 0 ], item[ 1 ], iconpath, brief[ count ], _localize_unit( item[ 4 ] ), _localize_unit( item[ 5 ] ), item[ 6 ].replace( "&#37;", "" ).replace( "%", "" ), wind[ count ], _localize_unit( item[ 8 ].replace( "</strong>", "" ), "speed" ), windir.get( item[ 7 ], "N/A" ), ) ]


class MaplistParser:
    def __init__( self, htmlSource ):
        self.map_list = []
        self._get_map_list( htmlSource )

    def _get_map_list( self, htmlSource ):
        try:
            # regex patterns
            pattern_map_list = "<option.+?value=\"([^\"]+)\".*?>([^<]+)</option>"
            # fetch avaliable maps
            map_list = re.findall( pattern_map_list, htmlSource, re.IGNORECASE )
            # enumerate thru list and eliminate bogus items
            for map in map_list:
                # eliminate bogus items
                if ( len( map[ 0 ] ) > 7 ):
                    self.map_list += [ map + ( "", ) ]
        except:
            pass


class MapParser:
    def __init__( self, htmlSource ):
        self.maps = ()
        self._get_maps( htmlSource )

    def _get_maps( self, htmlSource ):
        try:
            # initialize our animated maps list
            animated_maps = []
            # regex patterns
            pattern_maps = "<img name=\"mapImg\" src=\"([^\"]+)\""
            # fetch static map
            static_map_ = re.findall( pattern_maps, htmlSource, re.IGNORECASE )
            static_map_ = str(static_map_).replace("http://i.imwx.com/", "http://image.weather.com").replace("[", "").replace("]","").replace("\'","")
            static_map = []
            static_map += [static_map_]
            # print "stat : ", static_map            
            # does this map support animation?
            motion = re.findall( ">Weather In Motion<", htmlSource, re.IGNORECASE )
            if ( len( motion ) ):
                # get our map
                region = os.path.splitext( os.path.basename( static_map[ 0 ] ) )[ 0 ]
                # enumerate thru and create our animated map urls
                for i in range( 1, 6 ):
                    animated_maps += [ "http://image.weather.com/looper/archive/%s/%dL.jpg" % ( region, i, ) ]
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        # set our maps object
        self.maps += ( static_map, animated_maps, "", )
        # print "self.maps", self.maps


class WeatherClient:
    # base urls
    BASE_URL = "http://www.weather.com"
    BASE_FORECAST_URL = "http://www.weather.com/weather/%s/%s?bypassredirect=true%s"
    BASE_ACCU_FORECAST_URL = "http://www.accuweather.com/%s.aspx?partner=accuweather&metric=0&loc=%s&day=%s&week=%s&hour=%s"
    BASE_NOAA_FORECAST_URL = "http://forecast.weather.gov/MapClick.php?%s"
    BASE_NOAA_QUICK_URL = "http://forecast.weather.gov/afm/PointClick.php?%s"
    BASE_VIDEO_URL = "http://v.imwx.com/v/wxflash/%s.flv"
    BASE_MAPS = ( 
                                # Main local maps (includes some regional maps) #0
                                ( "", "", ),
                                # Main local maps (includes some regional maps) #1
                                ( "Local", "/weather/%s/%s?bypassredirect=true%s", ),
                                # weather details #2
                                ( "Weather Details (Alaska)", "/maps/geography/alaskaus/index_large.html", ),
                                ( "Weather Details (Current Weather)", "/maps/maptype/currentweatherusnational/index_large.html", ),
                                ( "Weather Details (Doppler Radar)", "/maps/maptype/dopplerradarusnational/index_large.html", ),
                                ( "Weather Details (Extended Forecasts)", "/maps/maptype/tendayforecastusnational/index_large.html", ),
                                ( "Weather Details (Hawaii)", "/maps/geography/hawaiius/index_large.html", ),
                                ( "Weather Details (Satellite - US)", "/maps/maptype/satelliteusnational/index_large.html", ),
                                ( "Weather Details (Satellite - World)", "/maps/maptype/satelliteworld/index_large.html", ),
                                ( "Weather Details (Severe Alerts - US)", "/maps/maptype/severeusnational/index_large.html", ),
                                ( "Weather Details (Severe Alerts - Regional)", "/maps/maptype/severeusregional/index_large.html", ),
                                ( "Weather Details (Short Term Forecast)", "/maps/maptype/forecastsusnational/index_large.html", ),
                                ( "Weather Details (Weekly Planner)", "/maps/maptype/weeklyplannerusnational/index_large.html", ),
                                ( "Weather Details (US Regions - Current)", "/maps/maptype/currentweatherusregional/index_large.html", ),
                                ( "Weather Details (US Regions - Forecasts)", "/maps/maptype/forecastsusregional/index_large.html", ),
                                ( "Weather Details (US Regions - Central)", "/maps/geography/centralus/index_large.html", ),
                                ( "Weather Details (US Regions - East Central)", "/maps/geography/eastcentralus/index_large.html", ),
                                ( "Weather Details (US Regions - Midwest)", "/maps/geography/midwestus/index_large.html", ),
                                ( "Weather Details (US Regions - North Central)", "/maps/geography/northcentralus/index_large.html", ),
                                ( "Weather Details (US Regions - Northeast)", "/maps/geography/northeastus/index_large.html", ),
                                ( "Weather Details (US Regions - Northwest)", "/maps/geography/northwestus/index_large.html", ),
                                ( "Weather Details (US Regions - South Central)", "/maps/geography/southcentralus/index_large.html", ),
                                ( "Weather Details (US Regions - Southeast)", "/maps/geography/southeastus/index_large.html", ),
                                ( "Weather Details (US Regions - Southwest)", "/maps/geography/southwestus/index_large.html", ),
                                ( "Weather Details (US Regions - West )", "/maps/geography/westus/index_large.html", ),
                                ( "Weather Details (US Regions - West Central)", "/maps/geography/westcentralus/index_large.html", ),
                                ( "Weather Details (World - Africa & Mid East)", "/maps/geography/africaandmiddleeast/index_large.html", ),
                                ( "Weather Details (World - Asia)", "/maps/geography/asia/index_large.html", ),
                                ( "Weather Details (World - Australia)", "/maps/geography/australia/index_large.html", ),
                                ( "Weather Details (World - Central America)", "/maps/geography/centralamerica/index_large.html", ),
                                ( "Weather Details (World - Europe)", "/maps/geography/europe/index_large.html", ),
                                ( "Weather Details (World - North America)", "/maps/geography/northamerica/index_large.html", ),
                                ( "Weather Details (World - Pacific)", "/maps/geography/pacific/index_large.html", ),
                                ( "Weather Details (World - Polar)", "/maps/geography/polar/index_large.html", ),
                                ( "Weather Details (World - South America)", "/maps/geography/southamerica/index_large.html", ),
                                # activity #35
                                ( "Outdoor Activity (Lawn and Garden)", "/maps/activity/garden/index_large.html", ),
                                ( "Outdoor Activity (Aviation)", "/maps/activity/aviation/index_large.html", ),
                                ( "Outdoor Activity (Boat & Beach)", "/maps/activity/boatbeach/index_large.html", ),
                                ( "Outdoor Activity (Business Travel)", "/maps/activity/travel/index_large.html", ),
                                ( "Outdoor Activity (Driving)", "/maps/activity/driving/index_large.html", ),
                                ( "Outdoor Activity (Fall Foliage)", "/maps/activity/fallfoliage/index_large.html", ),
                                ( "Outdoor Activity (Golf)", "/maps/activity/golf/index_large.html", ),
                                ( "Outdoor Activity (Outdoors)", "/maps/activity/nationalparks/index_large.html", ),
                                ( "Outdoor Activity (Oceans)", "/maps/geography/oceans/index_large.html", ),
                                ( "Outdoor Activity (Pets)", "/maps/activity/pets/index_large.html", ),
                                ( "Outdoor Activity (Ski)", "/maps/activity/ski/index_large.html", ),
                                ( "Outdoor Activity (Special Events)", "/maps/activity/specialevents/index_large.html", ),
                                ( "Outdoor Activity (Sporting Events)", "/maps/activity/sportingevents/index_large.html", ),
                                ( "Outdoor Activity (Vacation Planner)", "/maps/activity/vacationplanner/index_large.html", ),
                                ( "Outdoor Activity (Weddings - Spring)", "/maps/activity/weddings/spring/index_large.html", ),
                                ( "Outdoor Activity (Weddings - Summer)", "/maps/activity/weddings/summer/index_large.html", ),
                                ( "Outdoor Activity (Weddings - Fall)", "/maps/activity/weddings/fall/index_large.html", ),
                                ( "Outdoor Activity (Weddings - Winter)", "/maps/activity/weddings/winter/index_large.html", ),
                                ( "Outdoor Activity (Holidays)", "/maps/activity/holidays/index_large.html", ),
                                # health and safety #54
                                ( "Health & Safety (Aches & Pains)", "/maps/activity/achesandpains/index_large.html", ),
                                ( "Health & Safety (Air Quality)", "/maps/activity/airquality/index_large.html", ),
                                ( "Health & Safety (Allergies)", "/maps/activity/allergies/index_large.html", ),
                                ( "Health & Safety (Cold & Flu)", "/maps/activity/coldandflu/index_large.html", ),
                                ( "Health & Safety (Earthquake Reports)", "/maps/maptype/earthquakereports/index_large.html", ),
                                ( "Health & Safety (Home Planner)", "/maps/activity/home/index_large.html", ),
                                ( "Health & Safety (Schoolday)", "/maps/activity/schoolday/index_large.html", ),
                                ( "Health & Safety (Severe Weather Alerts)", "/maps/maptype/severeusnational/index_large.html", ),
                                ( "Health & Safety (Skin Protection)", "/maps/activity/skinprotection/index_large.html", ),
                                ( "Health & Safety (Fitness)", "/maps/activity/fitness/index_large.html", ),
                                # user defined #64
                                ( "User Defined - (Maps & Radars)", "*", ),
                            )

    # base paths
    if ( DEBUG ):
        BASE_MAPS_PATH = os.path.join( os.getcwd(), "maps" )
        BASE_SOURCE_PATH = os.path.join( os.getcwd(), "source" )
    else:
        BASE_MAPS_PATH = xbmc.translatePath( "/".join( [ "special://temp", os.path.basename( os.getcwd() ), "maps" ] ) )
        BASE_SOURCE_PATH = xbmc.translatePath( "/".join( [ "special://profile", "script_data", os.path.basename( os.getcwd() ), "source" ] ) )

    def __init__( self, code=None, translate=None ):
        # only check for compatibility if not debugging
        if ( not DEBUG ):
            # we raise an error if not compatible
            if ( not self._compatible() ):
                raise
        # set users locale
        self.code = code
        # set users translate preference
        self.translate = translate

    def _compatible( self ):
        # check for compatibility
        return ( not "%s" % ( str( [ chr( c ) for c in ( 98, 111, 120, 101, 101, ) ] ).replace( "'", "" ).replace( ", ", "" )[ 1 : -1 ], ) in xbmc.translatePath( "%s" % ( str( [ chr( c ) for c in ( 115, 112, 101, 99, 105, 97, 108, 58, 47, 47, 120, 98, 109, 99, 47, ) ] ).replace( "'", "" ).replace( ", ", "" )[ 1 : -1 ], ) ).lower() )

    def fetch_36_forecast( self, video ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_FORECAST_URL % ( "local", self.code, "", ), 15 )
        htmlSource_5 = self._fetch_data( self.BASE_URL + "/weather/5-day/"+ self.code, 15 )
        _localtime_source_ = self._fetch_data( "http://xoap.weather.com/weather/local/"+self.code+"?cc=f&dayf=1&par=1004124588&key=079f24145f208494", )
        # print "http://xoap.weather.com/weather/local/"+self.code+"?cc=f&dayf=1&par=1004124588&key=079f24145f208494", "localtime_source = "+_localtime_source_
	try:
             _localtime_ = int(re.findall ("([0-9]+):([0-9]+)", _localtime_source_)[1][0])
	except:
	     _localtime_ = None

        print "[Weather.com+] Area code = "+self.code
        # parse source for forecast
        parser = Forecast36HourParser( htmlSource, htmlSource_5, _localtime_, self.translate )
        # print parser.alertscolor[0]
        # fetch any alerts
        alerts, alertsrss, alertsnotify = self._fetch_alerts( parser.alerts )
        # print alerts, alertsrss, alertsnotify
        # create video url
        video, video_local = self._create_video( parser.video_location, parser.video_local_location, parser.video_local_number, video )
        print "[Weather.com+] Weather Video = "+video
        print "[Weather.com+] Local Video = "+video_local
        # return forecast
        if ( parser.alertscolor is not None ) :
             try : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor[0], len(parser.alerts), parser.forecast, parser.extras, video, video_local
             except : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor, len(parser.alerts), parser.forecast, parser.extras, video, video_local

    def accu_36_forecast( self, video ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "quick-look", self.code, "", "", "" ), 15 )
        htmlSource_1 = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "details", self.code, "1", "", "" ), 15 )
	htmlSource_2 = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "details", self.code, "2", "", "" ), 15 )
        print "[Weather.com+] Area code = "+self.code
        # parse source for forecast
        parser = ACCU_Forecast36HourParser( htmlSource, htmlSource_1, htmlSource_2, self.translate )
        # print parser.alertscolor[0]
        # fetch any alerts
        alerts, alertsrss, alertsnotify = self._fetch_alerts( parser.alerts )
        # print alerts, alertsrss, alertsnotify
        # create video url
        # video, video_local = self._create_video( parser.video_location, parser.video_local_location, parser.video_local_number, video )
	video = ""
	video_local = ""
        print "[Weather.com+] Weather Video = "+video
        print "[Weather.com+] Local Video = "+video_local
        # return forecast
        if ( parser.alertscolor is not None ) :
             try : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor[0], len(parser.alerts), parser.forecast, parser.extras, video, video_local
             except : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor, len(parser.alerts), parser.forecast, parser.extras, video, video_local

    def noaa_36_forecast( self, video ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_NOAA_FORECAST_URL % ( self.code ), 15 )
	htmlSource_2 = self._fetch_data( self.BASE_NOAA_QUICK_URL % ( self.code ), 15 )
        print "[Weather.com+] Area code = " + self.code
        # parse source for forecast
        parser = NOAA_Forecast36HourParser( htmlSource, htmlSource_2, self.translate )
        # print parser.alertscolor[0]
        # fetch any alerts
        alerts, alertsrss, alertsnotify = self._fetch_alerts( parser.alerts )
        # print alerts, alertsrss, alertsnotify
        # create video url
        # video, video_local = self._create_video( parser.video_location, parser.video_local_location, parser.video_local_number, video )
	video = ""
	video_local = ""
        print "[Weather.com+] Weather Video = "+video
        print "[Weather.com+] Local Video = "+video_local
        # return forecast
        if ( parser.alertscolor is not None ) :
             try : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor[0], len(parser.alerts), parser.forecast, parser.extras, video, video_local
             except : 
                 return alerts, alertsrss, alertsnotify, parser.alertscolor, len(parser.alerts), parser.forecast, parser.extras, video, video_local

    def _fetch_alerts( self, urls ):
        alerts = ""
        #alertscolor = ""
        alertsrss = ""
        alertsnotify = ""
        
        if ( urls ):
            #alertscolor = urls[ 0 ][ 0 ]
            titles = []
            # enumerate thru the alert urls and add the alerts to one big string
            for url in urls:
                # fetch source refresh every 15 minutes
                htmlSource = self._fetch_data( self.BASE_URL + "/weather/alerts/"+ url, 15 )
                # parse source for alerts
                parser = WeatherAlert( htmlSource )
                # needed in case a new alert format was used and we errored
                if ( parser.alert is not None ):
                    # add result to our alert string
                    alerts += parser.alert
                    titles += [ parser.title ]
                    alertsrss += "%s  |  " % ( parser.alert_rss, )
                    alertsnotify += "%s  |  " % ( parser.title.replace( "[B]", "" ).replace( "[/B]", "" ), )
            # TODO: maybe handle this above passing count to the parser
            # make our title string if more than one alert
            if ( len( titles ) > 1 ):
                title_string = ""
                for count, title in enumerate( titles ):
                    title_string += "%d. %s\n" % ( count + 1, title, )
                # add titles to alerts
                alerts = "%s\n%s\n%s\n\n%s" % (  "-" * 100, title_string.strip(), "-" * 100, alerts )
        # return alert string stripping the last newline chars
        # return alerts.strip(), alertsrss.strip().rstrip( "|" ).strip(), alertsnotify.rstrip( " |" ), alertscolor
        return alerts.strip(), alertsrss.strip().rstrip( "|" ).strip(), alertsnotify.rstrip( " |" )

    def _create_video( self, location, local_location, local_number, video ):
        url = ""
        local_url = ""
        print "[Weather.com+] Video Location : "+location
        # video = location
        # US
        if ( len( location ) and (self.code.startswith( "US" ) or len(self.code) == 5) and video == "" ):
            # Regional Video
            if ( location == "NE" or location == "MW" or location == "SE" or location == "W" or location == "S" or location == "SW" or location == "NW" or location == "NC" or location == "CN" or location == "WC"):               
                if ( location == "NE" ):
                    video = "northeast"
                elif ( location == "MW" ):
                    video = "midwest"
                elif ( location == "SE"):
                    video = "south"
                elif ( location == "W" ):
                    video = "west"
                elif ( location == "S" ):
                    video = "south"
                elif ( location == "SW" ):
                    video = "west"
                elif ( location == "NW" ):
                    video = "west"
                elif ( location == "WC" ):
                    video = "west"
                elif ( location == "NC" or location == "CN" ):
                    video="midwest"        
               # create the url
                url = self.BASE_VIDEO_URL % ( video, )
               # print "url : "+url
                           
           # Local Video
            if ( local_location == "new-yorks" or local_location == "washington-dcs") :
                if ( local_location == "new-yorks" ) :
                    local_location = "newyorkcity"
                    # print local_location
                if ( local_location == "washington-dcs" ) :
                    local_location = "washingtondc"
                local_url = self.BASE_VIDEO_URL % ( local_location, )
            elif ( local_location != "Not Available" ) :
                htmlSource = self._fetch_data("http://www.weather.com/outlook/videos/" + local_location + "-60-second-forecast-" + local_number)
                pattern_local = "<TITLE>(.+?)\'"
                local_location = re.findall( pattern_local, htmlSource )
                # print local_location, htmlSource
                if (local_location is not None) :
                   local_url = self.BASE_VIDEO_URL % ( local_location[0].replace(" ", "").lower(), )
                   print "[Weather.com+] Local Video Location : " + local_location[0].replace(" ", "").lower()
            
            # all failed use national
            if ( url == "" ) : 
                url = self.BASE_VIDEO_URL % ( "national", )
            return url, local_url

        # already have a video or non US
        # UK
        if (len( location ) and self.code.startswith( "UK" ) and video == "" ):
            url = "http://static1.sky.com/feeds/skynews/latest/daily/ukweather.flv"
            print "[Weather.com+] Local Video Location : UK"
            return url, local_url
        # Canada
        if (len( location ) and self.code.startswith("CA") and video == "" ):
            print "[Weather.com+] Local Video Location : Canada"
            accu_canada = "http://www.accuweather.com/video/1681759716/canadian-national-weather-fore.asp?channel=world"
            htmlSource = self._fetch_data( accu_canada, 15 )
            pattern_video = "http://brightcove.vo.llnwd.net/d([0-9]+)/unsecured/media/1612802193/1612802193_([0-9]+)_(.+?)-thumb.jpg"
            pattern_playerID = "name=\"playerID\" value=\"(.+?)\""
            pattern_publisherID = "name=\"publisherID\" value=\"(.+?)\""
            pattern_videoID = "name=\"\@videoPlayer\" value=\"(.+?)\""
            video_ = re.findall( pattern_video, htmlSource )
            playerID = re.findall( pattern_playerID, htmlSource )
            publisherID = re.findall( pattern_publisherID, htmlSource )
            videoID = re.findall( pattern_videoID, htmlSource )
	    try:
		if (int(video_[0][1][7:])-1000 < 10000) :
			video= video_[0][1][:7] + "0" + str(int(video_[0][1][7:])-1000)
		else :
			video= video_[0][1][:7] + str(int(video_[0][1][7:])-1000)  
		if (video is not None and video_[0][2][15:] == "cnnational") :
			url = "http://brightcove.vo.llnwd.net/d" + video_[0][0] + "/unsecured/media/1612802193/1612802193_" + video + "_" + video_[0][2] + ".mp4" + "?videoId="+videoID[0]+"&pubId="+publisherID[0]+"&playerId="+playerID[0]
		else : 
			url = ""
	    except:
		url = ""
            print url
            return url, local_url

        # Europe
        if (len( location ) and (self.code.startswith("FR") or self.code.startswith("SP") or self.code.startswith("IT") or self.code.startswith("GM") or self.code.startswith("NL") or self.code.startswith("GR") or self.code.startswith("PO") or self.code.startswith("EI")) and video == "" ):
            print "[Weather.com+] Local Video Location : Europe"
            accu_europe = "http://www.accuweather.com/video/1681759717/europe-weather-forecast.asp?channel=world"
            htmlSource = self._fetch_data( accu_europe, 15 )
            pattern_video = "http://brightcove.vo.llnwd.net/d([0-9]+)/unsecured/media/1612802193/1612802193_([0-9]+)_(.+?)-thumb.jpg"
            pattern_playerID = "name=\"playerID\" value=\"(.+?)\""
            pattern_publisherID = "name=\"publisherID\" value=\"(.+?)\""
            pattern_videoID = "name=\"\@videoPlayer\" value=\"(.+?)\""
            video_ = re.findall( pattern_video, htmlSource )
            playerID = re.findall( pattern_playerID, htmlSource )
            publisherID = re.findall( pattern_publisherID, htmlSource )
            videoID = re.findall( pattern_videoID, htmlSource )
	    # print video_
	    try:
		if (int(video_[0][1][7:])-1000 < 10000) :
			video= video_[0][1][:7] + "0" + str(int(video_[0][1][7:])-1000)
		else :
			video= video_[0][1][:7] + str(int(video_[0][1][7:])-1000)
	        if (video_[0][2][15:] == "europe") :
                        url = "http://brightcove.vo.llnwd.net/d" + video_[0][0] + "/unsecured/media/1612802193/1612802193_" + video + "_" + video_[0][2] + ".mp4" + "?videoId="+videoID[0]+"&pubId="+publisherID[0]+"&playerId="+playerID[0]
	        else : 
	                url = "http://static1.sky.com/feeds/skynews/latest/weather/europeweather.flv"
            except:
                url = "http://static1.sky.com/feeds/skynews/latest/weather/europeweather.flv"
            print url
            return url, local_url
        # No available video
        return video, video

    def fetch_hourly_forecast( self ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_FORECAST_URL % ( "hourbyhour", self.code, "", ), 15 )
        # parse source for forecast
        parser = ForecastHourlyParser( htmlSource, self.translate )
        # return forecast
        return parser.forecast

    def accu_fetch_hourly_forecast( self ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "hourly", self.code, "", "", "1" ), 1 )
	pattern_date = "<option selected=\"selected\" value=\"([0-9]+)\">"
	date = re.findall( pattern_date, htmlSource )
        htmlSource = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "hourly", self.code, "", "", date[1] ), 1 )
	htmlSource_2 = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "hourly", self.code, "", "", str(int(date[1])+7) ), 1 )
        # parse source for forecast
        parser = ACCU_ForecastHourlyParser( htmlSource + htmlSource_2, self.translate )
        # return forecast
        return parser.forecast

    def fetch_weekend_forecast( self ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_FORECAST_URL % ( "weekend", self.code, "", ), 15 )
        # parse source for forecast
        parser = ForecastWeekendParser( htmlSource, self.translate )
        # return forecast
        return parser.forecast

    def accu_fetch_10day_forecast( self ):
        # fetch source
        htmlSource_1 = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "forecast", self.code, "", "1", "" ), 15 )
	htmlSource_2 = self._fetch_data( self.BASE_ACCU_FORECAST_URL % ( "forecast", self.code, "", "2", "" ), 15 )
        # parse source for forecast
        parser = ACCU_Forecast10DayParser( htmlSource_1, htmlSource_2, self.translate )
        # return forecast
        return parser.forecast

    def fetch_10day_forecast( self ):
        # fetch source
        htmlSource = self._fetch_data( self.BASE_FORECAST_URL % ( "tenday", self.code, "&dp=windsdp", ), 15 )
        # parse source for forecast
        parser = Forecast10DayParser( htmlSource, self.translate )
        # return forecast
        return parser.forecast

    def fetch_map_list( self, provider=0, maptype=0, userfile=None, locationindex=None ):
        # set url
        url = self.BASE_URL + self.BASE_MAPS[ maptype ][ 1 ]        
        # we handle None, local and custom map categories differently
        if ( maptype == 0 ):
            # return None if none category was selected
            return None, None
        elif ( maptype == 1 ):
            # add locale to local map list if local category
            url = url % ( "map", self.code, "", )
        print "[Weather.com+] maptype = " + str(maptype)
        print "[Weather.com+] map_list_url = " + url
        # handle user definde maps special
        if ( maptype == ( len( self.BASE_MAPS ) - 1 ) ):
            # initialize our map list variable
            map_list = []
            # get correct location source
            category_title, titles, locationindex = self._get_user_file( userfile, locationindex )
            # if user file not found return None
            if ( category_title is None ):
                return None, None
            # enumerate thru and create map list
            for count, title in enumerate( titles ):
                # add title, we use an locationindex for later usage, since there is no html source to parse for images, we use count to know correct map to use
                map_list += [ ( str( count ), title[ 0 ], locationindex, ) ]
            # return results
            return category_title, map_list
        else:
            # fetch source, only refresh once a week
            htmlSource = self._fetch_data( url, 60 * 24 * 7, subfolder="maps" )
            # print htmlSource
            # parse source for map list
            parser = MaplistParser( htmlSource )
            # return map list
            print parser.map_list
            return None, parser.map_list

    def _get_user_file( self, userfile, locationindex ):
        # get user defined file source
        xmlSource = self._fetch_data( userfile )
        # if no source, then file moved so return
        if ( xmlSource == "" ):
            return None, None, None
        # default pattern
        pattern = "<location id=\"%s\" title=\"(.+?)\">(.+?)</location>"
        # get location, if no location for index, use default 1, which is required
        try:
            location = re.findall( pattern % ( locationindex, ), xmlSource, re.DOTALL )[ 0 ]
        except:
            # we need to set the used location id
            locationindex = "1"
            # use default "1"
            location = re.findall( pattern % ( locationindex, ), xmlSource, re.DOTALL )[ 0 ]
        # get title of maps for list and source for images
        titles = re.findall( "<map title=\"([^\"]+)\">(.+?)</map>", location[ 1 ], re.DOTALL )
        # return results
        return location[0], titles, locationindex

    def fetch_map_urls( self, map, userfile=None, locationindex=None ):
        # handle user defined maps special
        if ( map.isdigit() ):
            # convert map to int() for list index
            map = int( map )
            # get correct location source
            category_title, titles, locationindex = self._get_user_file( userfile, locationindex )
            # check if map is within the index range
            if ( map >= len( titles ) ):
                map = 0
            # grab all image urls
            urls = re.findall( "<image_url>([^<]+)</image_url>", titles[ map ][ 1 ] )
            # if image urls return results
            if ( urls ):
                # only set multi image list if more than one
                urls2 = ( [], urls, )[ len( urls ) > 1 ]
                # get a legend if it is separate from inages
                try:
                    legend = re.findall( "<legend_url>([^<]*)</legend_url>", titles[ map ][ 1 ] )[ 0 ]
                except:
                    legend = ""
                # return results
                return ( [ urls[ -1 ] ], urls2, legend, )
            # no image urls, find map urls
            map = re.findall( "<map_url>([^<]+)</map_url>", titles[ map ][ 1 ] )[ 0 ]
        # set url
        if ( map.endswith( ".html" ) ):
            url = self.BASE_URL + map
            # print "made url = " + url
        else:
            url = self.BASE_FORECAST_URL % ( "map", self.code, "&mapdest=%s" % ( map, ), )
        # fetch source
        print "[Weather.com+] map_url = " + url
        htmlSource = self._fetch_data( url, subfolder="maps" )
        # parse source for static map and create animated map list if available
        parser = MapParser( htmlSource )
        # return maps
        return parser.maps

    def fetch_images( self, map ):
        # print "fetch_images map", map
        # are there multiple images?
        maps = map[ 1 ] or map[ 0 ]
        # initailize our return variables
        legend_path = ""
        base_path_maps = ""
        # enumerate thru and fetch images
        for count, url in enumerate( maps ):
            # used for info in progress dialog
            self.image = os.path.basename( url )
            print "[Weather.com+] Fetch image = " + self.image + " ||| url = "+ url
            # fetch map
            base_path_maps = self._fetch_data( url, -1 * ( count + 1 ), self.image, len( maps ) > 1, subfolder="" )
            # no need to continue if the first map of multi image map fails
            if ( base_path_maps == "" ):
                break
        # fetch legend if available
        if ( map[ 2 ] and base_path_maps != "" ):
            # fetch legend
            legend_path = self._fetch_data( map[ 2 ], -1, os.path.basename( map[ 2 ] ), False, subfolder="" )
            # we add the image filename back to path since we don't use a multiimage control
            legend_path = os.path.join( legend_path, os.path.basename( map[ 2 ] ) )
        # we return path to images or empty string if an error occured
        print base_path_maps
        return base_path_maps, legend_path

    def _fetch_data( self, base_url, refreshtime=0, filename=None, animated=False, subfolder="forecasts", retry=True ):
        try:
            # set proper base path
            if ( not base_url.startswith( "http://" ) ):
                # user defined maps file
                base_path = base_url
                base_refresh_path = None
            elif ( filename is None ):
                # anything else except map/radar images (basically htmlSource)
                base_path = os.path.join( self.BASE_SOURCE_PATH, subfolder, md5.new( base_url ).hexdigest() )
                base_refresh_path = None
            else:
                # set proper path for md5 hash
                if ( animated ):
                    # animated maps include map name in base url, so don't use filename (each jpg would be in a seperate folder if you did)
                    path = os.path.dirname( base_url )
                else:
                    # non animated maps share same base url, so use full name
                    path = base_url
                # set base paths
                base_path = os.path.join( self.BASE_MAPS_PATH, subfolder, md5.new( path ).hexdigest(), filename )
                base_refresh_path = os.path.join( self.BASE_MAPS_PATH, subfolder, md5.new( path ).hexdigest(), "refresh.txt" )
            # get expiration date
            expires, refresh = self._get_expiration_date( base_path, base_refresh_path, refreshtime )
            # only fetch source if it's been longer than refresh time or does not exist
            if ( not os.path.isfile( base_path ) or refresh ):
                # request base url
                request = urllib2.Request( base_url )
                # add a faked header
                request.add_header( "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)" )
                #request.add_header( "Connection", "Keep-Alive" )
                #request.add_header( "Accept-Encoding", "gzip, deflate" )
                # open requested url
                usock = urllib2.urlopen( request )
                # get expiration
                try:
                    expires = time.mktime( time.strptime( usock.info()[ "expires" ], "%a, %d %b %Y %H:%M:%S %Z" ) )
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
            # return results
            return data
        except urllib2.HTTPError, e:
            # if error 503 and this is the first try, recall function after sleeping, otherwise return ""
            if ( e.code == 503 and retry ):
                # TODO: this is so rare, but try and determine if 3 seconds is enogh
                print "Trying url %s one more time." % base_url
                time.sleep( 3 )
                # try one more time
                return self._fetch_data( base_url, refreshtime, filename, animated, subfolder, False )
            else:
                # we've already retried, return ""
                print "Second error 503 for %s, increase sleep time." % base_url
                return ""
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            # some unknown error, return ""
            return ""

    def _get_expiration_date( self, base_path, base_refresh_path, refreshtime ):
        try:
            # get the data files date if it exists
            try:
                date = time.mktime( time.gmtime( os.path.getmtime( base_path ) ) )
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

