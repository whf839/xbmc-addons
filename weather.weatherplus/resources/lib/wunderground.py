# coding: utf-8

#*****************************************************
# 
#     Weather Client for Wunderground.com
#
#                           created by brightsr
#
#*****************************************************

import sys, os, urllib2, re, time
import xbmcaddon, xbmcgui
from threading import Thread
from utilities import _fetch_data, _translate_text, printlog
from utilities import _translate_text, _normalize_outlook, _localize_unit, _english_localize_unit, _getFeelsLike
from utilities import MapParser, MaplistParser, BASE_URL, BASE_MAPS

try:
    import xbmc
    DEBUG = False
except:
    DEBUG = True

try:
    import hashlib
except:
    import md5

WEATHER_WINDOW = xbmcgui.Window( 12600 )
Addon = xbmcaddon.Addon( id="weather.weatherplus" )
TSource = {}
windir = {}
icondir = { 
	"chanceflurries": "13",
	"chancerain": "11",
	"chancesleet": "5",
	"chancesnow": "13",
	"chancetstorms": "38",	
	"clear": "32",
	"cloudy": "26",
	"flurries": "13",
	"fog": "22",
	"hazy": "19",
	"mostlycloudy": "28",
	"mostlysunny": "30",	
	"partlycloudy": "30",
	"partlysunny": "30",	
	"sleet": "5",	
	"rain": "10",
	"snow": "16",
	"sunny": "32",
	"tstorms": "35",
	"nt_chanceflurries": "13",
	"nt_chancerain": "11",
	"nt_chancesleet": "5",
	"nt_chancesnow": "13",
	"nt_chancetstorms": "38",	
	"nt_clear": "31",
	"nt_cloudy": "26",
	"nt_flurries": "13",
	"nt_fog": "22",
	"nt_hazy": "19",
	"nt_mostlycloudy": "27",
	"nt_mostlysunny": "29",	
	"nt_partlycloudy": "29",
	"nt_partlysunny": "29",	
	"nt_sleet": "5",	
	"nt_rain": "10",
	"nt_snow": "16",
	"nt_sunny": "32",
	"nt_tstorms": "35",
	"unknown": "na"	
}

uvindex_dir = {	"0": "Low", "1": "Low", "2": "Low", "3": "Minimal", "4": "Minimal", "5": "Moderate", "6": "Moderate",
		"7": "High", "8": "High", "9": "High", 
		"10": "Very high", "11": "Very high", "12": "Very high", "13": "Very high", "14": "Very high", "15": "Very high", "16": "Very high" }

month_dir = {
	"January": "1",
	"February": "2",
	"March": "3",
	"April": "4",
	"May": "5",
	"June": "6",
	"July": "7",
	"August": "8",
	"September": "9",
	"October": "10",
	"November": "11",
	"December": "12"
}
month_list = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]

areadir = { "asia" : "KSXX0037",
	   "europe" : "FRXX0076",
	   "canada" : "CAXX0504",
	   "Mexico" : "MXDF0132",
	   "camerica" : "PMXX0004",
	   "samerica" : "CIXX0020",
	   "oceania" : "ASXX0112",
	   "africa" : "UGXX0001",
	   "middle" : "IRXX0036" }

class WeatherClient:
	# variables for fetching maps
	wunder_country = ""
	wunder_area = ""
	# base url
	BASE_FORECAST_URL = "http://www.wunderground.com/%s"
	BASE_WEATHER_COM_URL = "http://www.weather.com/weather/%s/%s?%s"

	def __init__( self, code=None, translate=None ):
		# set users locale
		self.code = code
		# set users translate preference
		self.translate = translate
		self.wunderSource = _fetch_data( self.BASE_FORECAST_URL % ( self.code ), 3 )
		self._set_windir()

	def _set_windir ( self ):
		global windir
		windir_en = "From the North|From the North Northeast|From the Northeast|From the East Northeast|From the East|From the East Southeast|From the Southeast|From the South Southeast|From the South|From the South Southwest|From the Southwest|From the West Southwest|From the West|From the West Northwest|From the Northwest|From the North Northwest"
		if (self.translate == "en-us"):
			windir_tr = windir_en.split("|")
		else:
			windir_tr = _translate_text( windir_en, self.translate ).split("|")
			windir = {    
		                    "N": windir_tr[0],
				    "North": windir_tr[0],
		                    "NNE": windir_tr[1],
		                    "NE": windir_tr[2],
		                    "ENE": windir_tr[3],
		                    "E": windir_tr[4],
				    "East": windir_tr[4],
		                    "ESE": windir_tr[5],
		                    "SE": windir_tr[6],
		                    "SSE": windir_tr[7],
		                    "S": windir_tr[8],
		                    "South": windir_tr[8],
		                    "SSW": windir_tr[9],
		                    "SW": windir_tr[10],
		                    "WSW": windir_tr[11],
		                    "W": windir_tr[12],
		                    "West": windir_tr[12],
		                    "WNW": windir_tr[13],
		                    "NW": windir_tr[14],
		                    "NNW": windir_tr[15]
			}
	def _lookup_area( self, country ):
		if ( country == "Mexico" ): return country
		asia = "Bangladesh/Bhutan/Brunei/Burma (Myanmar)/Cambodia/China/Hong Kong/Macau/East Timor/India/Indonesia/Japan/Kazakhstan/Laos/Malaysia/Maldives/Mongolia/Nepal/North Korea/Pakistan/Philippines/Singapore/South Korea/Sri Lanka/Taiwan/Thailand/Turkey/Vietnam"
		middle_east = "Iran/Iraq/Israel/Jordan/Kuwait/Kyrgyzstan/Lebanon/Oman/Palestine/Qatar/Saudi Arabia/Syria/Tajikistan/Turkmenistan/United Arab Emirate (UAE)/Uzbekistan/Yemen"
		africa = "Algeria/Angola/Benin/Botswana/Burkina Faso/Burundi/Cameroon/Cape Verde/Central African Republic/Chad/Comoros/Congo/Cote d'Ivoire/Djibouti/Egypt/Equatorial Guinea/Eritrea/Ethiopia/Gabon/Gambia/Ghana/Guinea/Guinea-Bissau/Kenya/Lesotho/Liberia/Libya/Madagascar/Malawi/Mali/Mauritania/Mauritius/Morocco/Mozambique/Namibia/Niger/Nigeria/Rwanda/Sao Tome And Principe/Senegal/Seychelles/Sierra Leone/Somalia/South Africa/South Sudan/Sudan/Swaziland/Tanzania/Togo/Tunisia/Uganda/Western Sahara/Zambia/Zimbabwe"
		oceania = "Australia/New Zealand/New South Wales/Victoria/Queensland/Northern Territory/Western Australia/South Australia"
		central_america = "Belize/Guatemala/Honduras/Nicaragua/Costa Rica/El Salvador/Panama/Cayman Islands/Jamica/Cuba/Bahamas/Bermuda/Haiti/Dominican Republic/Trinidad And Tobago"
		europe = "Iceland/Ireland/United Kingdom/Portugal/Spain/Andorra/France/Luxembourg/Monaco/Switzerland/Slovenia/Liechtenstein/Germany/Denmark/Netherlands/Belgium/Norway/Sweden/Finland/San Marino/Italy/Malta/Austria/Czech Republic/Poland/Slovakia/Hungary/Croatia/Montenegro/Serbia/Albania/Bosnia And Herzegovina/Bulgaria/Macedonia/Greece/Romania/Moldova/Ukraine/Belarus/Lithuania/Latvia/Estonia/Russia/Georgia/Armenia/Azerbaijan/Cyprus"
		south_america = "Venezuela/Colombia/Guyana/Suriname/French Guiana/Ecuador/Peru/Brazil/Bolivia/Paraguay/Argentina/Uruguay/Chile"
		canada = "Northwest Territories/British Columbia/Yukon/Alberta/Saskatchewan/Manitoba/Ontario/Nunavut/Quebec/New Brunswick/Nova Scotia/Labarador/Newfoundland/Prince Edward Island"
		if ( re.search( country, asia ) ): return "asia"
		elif ( re.search( country, europe ) ): return "europe"
		elif ( re.search( country, south_america ) ): return "samerica"
		elif ( re.search( country, central_america ) ): return "camerica"
		elif ( re.search( country, middle_east ) ): return "middle"
		elif ( re.search( country, oceania ) ): return "oceania"
		elif ( re.search( country, africa ) ): return "africa"
		elif ( re.search( country, canada ) ): 
			self.wunder_country = "Canada"		
			return "canada"
		return "unknown"	

	def _fetch_36_forecast( self, video ):
		printlog( "Trying to fetch 36 hour and extended forecast.." )
		printlog( "Area code = " + self.code )
		# parse source for forecast
		parser = WUNDER_Forecast36HourParser( self.wunderSource, self.translate )
		if ( parser.forecast[0] == "ERROR" ):
			printlog( "ERROR : Failed to load 36 hour forecast from Wunderground.com!" )
		# lookup local area for local map selection
		if ( self.code.startswith("/q/zmw:00000") ):
			pattern_country = "<h1 id=\"locationName\"[^>]+>[^,]+, ([^<]+)</h1>"
			country = re.findall( pattern_country, self.wunderSource )
			if ( len(country) ):
				self.wunder_country = country[0]
				self.wunder_area = self._lookup_area( self.wunder_country )
		else:
			self.wunder_country = "US"
			self.wunder_area = re.findall( "/q/zmw:([0-9]+).", self.code )[0]
		printlog( "Country = %s" % self.wunder_country )
		printlog( "Area = %s" % self.wunder_area )
		# fetch any alerts
		try:
			alerts, alertsrss, alertsnotify, alertscolor = self._fetch_alerts( parser.alerts, parser.alerts[-1][1] == "US Severe Weather" )
		except:
			alerts = ""
			alertsrss = ""
			alertsnotify = ""
			alertscolor = ""
		# create video url
		if ( self.wunder_country == "US" ):
			from video_us import _create_video
			video_title = [Addon.getSetting("video1"), Addon.getSetting("video2"), Addon.getSetting("video3")]
			video = _create_video ( video_title )
		else:
			from video_non_us import _create_video
			video, video_title = _create_video( self.wunder_country, self.wunder_area )
		# return forecast
		printlog( "Fetching 36 hour forecast... Done!" )
		return alerts, alertsrss, alertsnotify, alertscolor, len(parser.alerts), parser.forecast, parser.extras, video, video_title             

    	def _fetch_10day_forecast( self ):
		printlog( "Trying to fetch extended forecast.." )
		# parse source for forecast
		parser = WUNDER_Forecast10DayParser( self.wunderSource, self.translate )
		# print parser.forecast
		# print parser.forecast[0]
		if ( parser.forecast[0] == "ERROR" ):
			printlog( "ERROR : Failed to load extended forecast from Wunderground.com!" )
		# return forecast
		return parser.forecast

    	def _fetch_hourly_forecast( self ):
		printlog( "Trying to fetch hourly forecast.." )
		# parse source for forecast
		pattern_url = "<a href=\"/(.+?)[&]yday=([0-9]+)[&]weekday=[^\"]+\">Hourly Forecast"
		url = re.findall( pattern_url, self.wunderSource )
		htmlSource = _fetch_data( "http://www.wunderground.com/%s&yday=%s" % ( url[0][0], url[0][1] ), 15 )
		htmlSource = htmlSource.split("Extended Forecast")[0] + _fetch_data( "http://www.wunderground.com/%s&yday=%d" % ( url[0][0], [ int(url[0][1])+1, 1 ][int(url[0][1])==365] ), 15 )
		htmlSource = htmlSource.split("Extended Forecast")[0]
		parser = WUNDER_ForecastHourlyParser( htmlSource + self.wunderSource, self.translate )
		if ( parser.forecast[0] == "ERROR" ):
			printlog( "ERROR : Failed to load hourly forecast from Wunderground.com!" )
		# return forecast
		return parser.forecast

	def _fetch_alerts( self, raw_alerts, area ):
		alerts = ""
		alertsrss = ""
		alertsnotify = ""
		alertscolor = ""
		if ( raw_alerts ):
			if ( area ):
				htmlSource = _fetch_data( self.BASE_WUNDER_FORECAST_URL % raw_alerts[0][0], 15 ).replace("\n","").replace("\t","")
				htmlSource = re.sub( "<[!]--[^-]+-->", "", htmlSource )
				pattern_title = "<br />\.\.\.(.+?)\.\.\."
				pattern_state = "<div class=\"primeHeader\">(.+?)</div>"
				pattern_text = "<div class=\"taL\" >(.+?)</div>"
				titles = re.findall( pattern_title, htmlSource )
				states = re.findall( pattern_state, htmlSource )
				texts = re.findall( pattern_text, htmlSource )
				alertscolor = "2"
				printlog( "Fetching Alerts... Trying" )
				for count in range( len(raw_alerts) - 1 ):
					if ( re.search( "Warning", raw_alerts[count][1] ) ): alertscolor = "1"
					text = re.sub( "<[^>]+>", "", texts[count].replace("<br /><br /><br />","\n").replace("<br />","\n").strip() )
					alerts += "[B]%s[/B]\n\n" % raw_alerts[count][1]
					alerts += "\n[I]%s[/I]\n\n" % re.sub( "<[^>]+>", "", states[count].strip() )
					alerts += "%s\n\n%s\n\n" % ( text, "-"*100 )
					try:
						alertsrss += "%s  |  " % re.sub( "<[^>]+>", " ", titles[count].strip() )
					except:
						alertsrss += "%s  |  " % text[:100]
					alertsnotify += "%s,  " % raw_alerts[count][1]
				alertsrss = alertsrss.strip().rstrip( "|" ).strip()
				alertsnotify = alertsnotify.strip().rstrip( "," ).strip()
				# print alerts, alertsrss, alertsnotify, alertscolor
				printlog( "Fetching Alerts... Done!" )
			else:
				colordir = { "FFFF00" : "2",
					     "FFC400" : "2",
					     "FF0000" : "1" }
				htmlSource = _fetch_data( self.BASE_WUNDER_FORECAST_URL % raw_alerts[0][0], 15 )
				pattern_title = "<span class=\"fLeft b med\">(.+?)</span>"
				pattern_color = "background-color: #(.+?);"
				colors = re.findall( pattern_color, htmlSource )
				#titles = re.findall( pattern_title, htmlSource )
				alertscolor = colordir.get( colors[0] )
				printlog( "Fetching Alerts... Trying" )
				for alert in raw_alerts:
					alerts += "%s\n\n" % alert[1]
					alertsrss += "%s  |  " % alert[1]
					titles = _translate_text ( alert[1], "en" )
					alertsnotify += "%s |  " % titles
				alertsrss = alertsrss.strip().rstrip( "|" ).strip()
				alertsnotify = alertsnotify.strip().rstrip( "|" ).strip()
				printlog( "Fetching Alerts... Done!" )
		return alerts, alertsrss, alertsnotify, alertscolor

	def fetch_map_list( self, maptype=0, userfile=None, locationindex=None ):
		# set url
		url = BASE_URL + BASE_MAPS[ maptype ][ 1 ]        
		# we handle None, local and custom map categories differently
		if ( maptype == 0 ):
			# return None if none category was selected
			return None, None
		elif ( maptype == 1 ):
		    # add locale to local map list if local category
			if ( self.wunder_country == "US" ):
				url = url % ( "map", self.wunder_area, "", )
			else:
				url = url % ( "map", areadir.get(self.wunder_area, ""), "", )
			Addon.setSetting( "wunder_country", self.wunder_country )
			Addon.setSetting( "wunder_area", self.wunder_area )
		printlog( "maptype = " + str(maptype) )
		printlog( "map_list_url = " + url )
		# fetch source, only refresh once a week
		htmlSource = _fetch_data( url, 60 * 24 * 7, subfolder="maps" )
		# print htmlSource
		# parse source for map list
		parser = MaplistParser( htmlSource )
		# return map list
		# print parser.map_list
		return None, parser.map_list

	def fetch_map_urls( self, map, userfile=None, locationindex=None ):
		# set url
		if ( map.endswith( ".html" ) ):
			url = BASE_URL + map
		else:
			wunder_country  = Addon.getSetting( "wunder_country" )
			wunder_area = Addon.getSetting( "wunder_area" )
			if ( wunder_country == "US" ):
				url = self.BASE_WEATHER_COM_URL % ( "map", wunder_area, "&mapdest=%s" % ( map, ), )
			else:
				url = self.BASE_WEATHER_COM_URL % ( "map", areadir.get(wunder_area, ""), "&mapdest=%s" % ( map, ), )
		# fetch source
		htmlSource = _fetch_data( url, 60*60*24*7, subfolder="maps",  )
		# parse source for static map and create animated map list if available
		parser = MapParser( htmlSource )
		# return maps
		return parser.maps

class WUNDER_Forecast36HourParser:
    def __init__( self, htmlSource, translate=None ):
        self.forecast = []
        self.extras = []
        self.alerts = []
        self.alertscolor = []
        self.video_location = []
        self.translate = translate
        self.sun = []

        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
	printlog( "Fetching Forecast from Wunderground.com..." )
        # regex patterns
        pattern_days = "<div class=\"titleSubtle\">(.+?)</div>"
	pattern_low_temp = "([0-9]+) \&deg;"
	pattern_high_temp = "<span class=\"b\">([.0-9]+)</span>"
	pattern_icon = "http://icons-ak.wxug.com/i/c/k/(.+?).gif"
        pattern_brief = "<div class=\"foreCondition\">([^<]+)<[^>]+>([^<]+)<"
	pattern_current_brief = "alt=\"([^\"]+)\" class=\"condIcon\""
	pattern_current_date = "<div id=\"infoTime\"><span>(.+?)</span>"
	pattern_current_temp = "<div id=\"tempActual\"><[^>]+>[^<]+<span class=\"nobr\"><span class=\"b\">([^<]+)</span>\&nbsp;\&deg;"
	pattern_current_feelslike = "Feels Like[^<]+<span class=\"nobr\"><span class=\"b\">([^<]+)</span>\&nbsp;\&deg;"
	pattern_current_wind = "metric=\"\" value=\"(.+?)\""
	pattern_current_windspeed = "pwsvariable=\"windspeedmph\" english=\"\" metric=\"\">(.+?)</span>"
	pattern_current_humidity = "pwsvariable=\"humidity\" english=\"\" metric=\"\" value=\"(.+?)\""
	pattern_current_dew = "pwsvariable=\"dewptf\" english=\"\&deg;F\" metric=\"\&deg;C\" value=\"(.+?)\""
	pattern_current_uvindex = "<div class=\"dataCol4\"><span class=\"b\">([^<]+)</span> out of 16</div>"
	pattern_current_time = "<div id=\"infoTime\"><span>(.+?)</span>"
        pattern_precip_amount = "no-repeat;\">([0-9]+)\%</td><td class=\"weekly_wind\">"
        pattern_outlook = "<td class=\"vaT full\">(.+?)</td>"
        pattern_pressure = "pwsvariable=\"baromin\" english=\"in\" metric=\"hPa\" value=\"([^>]+)\">"	
        pattern_visibility = "<div class=\"dataCol1\"><dfn>Visibility</dfn></div>[^<]+<div class=\"dataCol4\">[^<]+<span class=\"nobr\"><span class=\"b\">([^<]+)</span>"	
	pattern_sunrise = "<div id=\"sRise\"><span class=\"b\">(.+?)</span> AM</div>"
	pattern_sunset = "<div id=\"sSet\"><span class=\"b\">(.+?)</span> PM</div>"
	pattern_next_sunrise = "<div id=\"sRiseHr\" style=\"[^\"]+\"><span class=\"b\">(.+?)</span> AM</div>"
	pattern_next_sunset = "<div id=\"sSetHr\" style=\"[^\"]+\"><span class=\"b\">(.+?)</span> PM</div>"
	pattern_date = "<div class=\"fctDayDate\">[^,]+, ([0-9]+)</div>"
	pattern_wind = "<td class=\"weekly_wind\"><img class=\"wind\" src=\"image/(.+?).png\" width=\"50\" height=\"22\" alt=\"[^\"]+\" /><br />(.+?)</td>"
	pattern_alert_block = "<div class=\"alertItems\"><span>Active Advisory:</span>(.+?)</div>"
	# pattern_alert_exclude = "Active Notice:</span>(.+?)"
	pattern_alert = "<a href=\"([^\"]+)\"[^>]+>([^<]+)</a>"
	pattern_alert_2 = "<a href=\"([^\"]+)\">([^<]+)</a>"

        # fetch info.
	raw_days = re.findall( pattern_days, htmlSource )
	high_temp = re.findall( pattern_high_temp, htmlSource )
	low_temp = re.findall( pattern_low_temp, htmlSource )
	raw_brief = re.findall( pattern_brief, htmlSource )
	raw_icons = re.findall( pattern_icon, htmlSource )
	raw_outlook = re.findall( pattern_outlook, htmlSource )
	current_date = re.findall( pattern_current_date, htmlSource )
	current_brief = re.findall( pattern_current_brief, htmlSource )
	current_temp = re.findall( pattern_current_temp, htmlSource )
	current_feelslike = re.findall( pattern_current_feelslike, htmlSource )
	current_wind = re.findall( pattern_current_wind, htmlSource )
	current_windspeed = re.findall( pattern_current_windspeed, htmlSource )
	current_pressure = re.findall( pattern_pressure, htmlSource )
	current_visibility = re.findall( pattern_visibility, htmlSource )
	current_dew = re.findall( pattern_current_dew, htmlSource )
	current_humidity = re.findall( pattern_current_humidity, htmlSource )
	current_uvindex = re.findall( pattern_current_uvindex, htmlSource )
	current_precip = "N/A"
	current_sunrise = re.findall( pattern_sunrise, htmlSource )
	current_sunset = re.findall( pattern_sunset, htmlSource )
	next_sunrise = re.findall( pattern_next_sunrise, htmlSource )
	next_sunset = re.findall( pattern_next_sunset, htmlSource )
	dates = re.findall( pattern_date, htmlSource )
	alerts = re.findall( pattern_alert_block, htmlSource.replace("\n","").replace("\t","") )
	if ( alerts ):
		alerts = alerts[0].split("Active Notice:")[0]
		self.alerts = re.findall ( pattern_alert, alerts )
		if ( not self.alerts ): self.alerts = re.findall ( pattern_alert_2, alerts )

	'''
	print raw_days, high_temp, low_temp, raw_brief, raw_icons, raw_outlook, current_temp, current_date, dates, current_feelslike, current_wind, current_windspeed
	print current_pressure, current_visibility, current_dew, current_humidity, current_uvindex, current_sunrise, current_sunset
	'''
	
	try:
		days = [ raw_days[6], raw_days[7], raw_days[8] ]
		icons = [ raw_icons[1], raw_icons[2], raw_icons[3] ]
		brief = [ raw_brief[0][0], raw_brief[1][0], raw_brief[2][0] ]
		outlook = [ raw_outlook[0].replace("&deg;", ""), raw_outlook[1].replace("&deg;", ""), raw_outlook[2].replace("&deg;", "") ]
		precips = [ raw_brief[0][1], raw_brief[1][1], raw_brief[2][1] ]
		printlog( "Icons, Briefs, Outlooks, Precips OK!" )
		current_ampm = current_date[0].split(",")[0].split(" ")[1]
		current_date = current_date[0].split(",")[0].split(" ")[-1]
		printlog( "Current Date, Time OK!" )
		current_icon = raw_icons[1]
		current_brief = current_brief[0]
		printlog( "Current Icon, Brief OK!" )
		current_temp = _localize_unit( current_temp[0], "tempf2c" )
		current_feelslike = _localize_unit( current_feelslike[0], "tempf2c" )
		printlog( "Current Temperature, Feels like OK!" )
		try:
			current_pressure = _localize_unit( current_pressure[0], "pressure" )
		except:
			current_pressure = "N/A"
		try:
			current_visibility = _localize_unit ( current_visibility[0], "distance" )
		except:
			current_visibility = "N/A"
		printlog( "Pressure, Visibility OK!" )
		current_dew = _localize_unit( current_dew[0], "tempf2c" )
		current_humidity = current_humidity[0]
		printlog( "Dew point, Humidity OK!" )
		try:
			current_uvindex = "%s - %s" % ( current_uvindex[0].split(".")[0], uvindex_dir.get( current_uvindex[0].split(".")[0], "" ) )
		except:
			current_uvindex = "N/A"
		printlog( "UV Index OK!" )
		# current sunrise, sunset
		current_sunrise = _localize_unit( current_sunrise[0]+" AM", "time" )
		current_sunset = _localize_unit( current_sunset[0]+" PM", "time" )
		# making daylight info.
		if ( current_date != dates[0] ): 
			if ( days[0] == "Today" ):
				daylight = [ current_sunrise, current_sunset, _localize_unit( next_sunrise[0]+" AM", "time" ) ]
			else:
				daylight = [ current_sunset, _localize_unit( next_sunrise[0]+" AM", "time" ),  _localize_unit( next_sunset[0]+" PM", "time" ) ]  
		else:
			if ( days[0] == "Today" ):
				daylight = [ current_sunrise, current_sunset, _localize_unit( next_sunrise[1]+" AM", "time" ) ]
			elif ( current_ampm == "PM" ):
				daylight = [ current_sunset, _localize_unit( next_sunrise[1]+" AM", "time" ),  _localize_unit( next_sunset[1]+" PM", "time" ) ]  
			else:
				daylight = [ "N/A", _localize_unit( next_sunrise[0]+" AM", "time" ),  _localize_unit( next_sunset[0]+" PM", "time" ) ]  
				
		printlog( "sunrise, sunset OK!" )
		# print current_wind[0]
		# print current_windspeed[0]
		current_wind = int(current_wind[0])
		current_windspeed = str(int(float(current_windspeed[0])))
		printlog ("wind = %d" % current_wind)
		printlog ("windspeed = %s" % current_windspeed)

		if ( current_wind < 11.25 ):
			current_wind = "N"
		elif ( current_wind < 11.25 + 22.5 * 1 ):
			current_wind = "NNE"
		elif ( current_wind < 11.25 + 22.5 * 2 ):
			current_wind = "NE"
		elif ( current_wind < 11.25 + 22.5 * 3 ):
			current_wind = "ENE"
		elif ( current_wind < 11.25 + 22.5 * 4 ):
			current_wind = "E"
		elif ( current_wind < 11.25 + 22.5 * 5 ):
			current_wind = "ESE"
		elif ( current_wind < 11.25 + 22.5 * 6 ):
			current_wind = "SE"
		elif ( current_wind < 11.25 + 22.5 * 7 ):
			current_wind = "SSE"
		elif ( current_wind < 11.25 + 22.5 * 8 ):
			current_wind = "S"
		elif ( current_wind < 11.25 + 22.5 * 9 ):
			current_wind = "SSW"
		elif ( current_wind < 11.25 + 22.5 * 10 ):
			current_wind = "SW"
		elif ( current_wind < 11.25 + 22.5 * 11 ):
			current_wind = "WSW"
		elif ( current_wind < 11.25 + 22.5 * 12 ):
			current_wind = "W"
		elif ( current_wind < 11.25 + 22.5 * 13 ):
			current_wind = "WNW"
		elif ( current_wind < 11.25 + 22.5 * 14 ):
			current_wind = "NW"
		elif ( current_wind < 11.25 + 22.5 * 15 ):
			current_wind = "NNW"
		else:
			current_wind = "N"

		current_windDirection = current_wind
		current_wind = _localize_unit(current_windspeed, "speedmph2kmh")
		printlog( "Wind OK!" )

		if ( days[0] == " Today" ):
			temperature = [ high_temp[4], low_temp[4], high_temp[5] ]
			temperature_info = [ "High", "Low", "High" ]
			daylight_title = [ "Sunrise", "Sunset", "Sunrise" ]
			days = [ "Today", "Tonight", "Tomorrow" ]
		else:
			temperature = [ low_temp[4], high_temp[4], low_temp[6] ]
			temperature_info = [ "Low", "High", "Low" ]
			daylight_title = [ "Sunset", "Sunrise", "Sunset" ]
			days = [ "Tonight", "Tomorrow", "Tomorrow Night" ]

		printlog( "Day OK!" )

		current_icon = icondir.get( current_icon, "na" ) + ".png"	

	except:
		self.forecast = [ "ERROR", ]
		return
	
	# print "[Weather Plus] Wunderground.com, Modified Info :"
	# print days, temperature, brief, icons, outlook, current_date, current_icon, current_brief, current_temp, current_feelslike, current_wind, current_windDirection
	# print current_pressure, current_visibility, current_dew, current_humidity, current_uvindex, current_sunrise, current_sunset

	normalized_outlook = _normalize_outlook ( outlook )

	if ( self.translate is not None ):
		# we separate each item with single pipe
		text = current_brief
		text += "|||||"
		text += "|".join( brief )
		text += "|||||"
		text += "|".join( normalized_outlook )
		# translate text
		text = _translate_text( text, self.translate )
		# split text into it's original list
		current_brief = text.split("|||||")[0]
		brief = text.split("|||||")[1].split( "|" )
		normalized_outlook = text.split("|||||")[2].split( "|" )


   	self.extras += [( current_pressure, current_visibility, current_sunrise, current_sunset, current_temp, current_feelslike, current_brief, current_wind, current_humidity, current_dew, current_icon, current_uvindex, current_windDirection )]

	for count in range(0,3) :
		iconpath = "/".join( [ "special://temp", "weather", "128x128", "%s.png" % icondir.get( icons[ count ], "na" ) ] )
		if ( precips[ count ] == "\n\t\t" ):
			precip = "0"
		else:
			precip = precips[ count ].split("%")[0]
		try:
			self.forecast += [ ( days[count], iconpath, brief[ count ], temperature_info[ count ], _localize_unit( temperature[ count ] ), "", precip, normalized_outlook[ count ], daylight_title[ count ], daylight[ count ], "N/A", "N/A", "" ) ]	
		except:
			self.forecast = [ "ERROR", ]
			return

class WUNDER_Forecast10DayParser:
    def __init__( self, htmlSource, translate ):
	self.forecast = []
	self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
	# regex patterns
        pattern_first_heading = "<div class=\"titleSubtle\">(.+?)</div>"
	pattern_time = "<div id=\"infoTime\"><span>(.+?)</span>"
	pattern_date = "<div class=\"fctDayDate\">([^,]+), ([0-9]+)</div>"
	pattern_icon_cond = "<div class=\"fctCondIcon\"><a href=\"\" class=\"iconSwitchMed\"><img src=\"http://icons-ak.wxug.com/i/c/k/(.+?).gif\" alt=\"(.+?)\""
	pattern_hi_low = "<div class=\"fctHiLow\">[^<]+<span class=\"b\">([0-9]+)</span> [|] (.+?)\n"
	pattern_precip = "<div class=\"popValue\">(.+?)%</div>"
	pattern_wind_block = "<td class=\"hrType\">Wind</td>(.+?)</tr>"
	pattern_daylight_block = "<td class=\"hrType\">Sunrise \&amp; Sunset</td>(.+?)</tr>"
	pattern_humidity_block = "<td class=\"hrType\"><dfn>Humidity</dfn></td>(.+?)</tr>"
	pattern_value = "<span class=\"b\">(.+?)</span>"

	# fetch info.
	local_time = re.findall( pattern_time, htmlSource )
	dates = re.findall( pattern_date, htmlSource )
	icon_cond = re.findall( pattern_icon_cond, htmlSource )
	hi_low = re.findall( pattern_hi_low, htmlSource )
	precip = re.findall( pattern_precip, htmlSource )
	wind_block = re.findall( pattern_wind_block, htmlSource.replace("\n","").replace("\t","") )
	daylight_block = re.findall( pattern_daylight_block, htmlSource.replace("\n","").replace("\t","") )
	humidity_block = re.findall( pattern_humidity_block, htmlSource.replace("\n","").replace("\t","") )
	
	try:
		first_heading = re.findall( pattern_first_heading, htmlSource )[6]
		current_ampm = local_time[0].split(",")[0].split(" ")[1]
		# print first_heading
		today = local_time[0].split(",")[0].split(" ")[-1]
		# print today
		month = local_time[0].split(" ")[4]
		# print month
		month = month_dir.get( month )
		# print month
		
		brief = [icon_cond[i][1] for i in range(0, 7)]

                if ( self.translate is not None ):
			# we separate each item with single pipe
			text = ""
			try:
			   text += "|".join( brief )
			except:
			   printlog( "No Info : 10day Brief" )
			# translate text
			print text, self.translate
			text = _translate_text( text, self.translate )
			print text
			# split text into it's original list
			brief = text.split( "|" )

		for count in range( 0, 7 ):
			iconpath = "/".join( [ "special://temp", "weather", "128x128", "%s.png" % icondir.get( icon_cond[ count ][0], "na" ) ] )
			# print iconpath, dates[count], icon_cond[count], hi_low[count], precip[count]
			# print today, dates[0][1], current_ampm
			wind = re.findall( pattern_value, wind_block[count] )
			wind_short_direction = wind[3]
			wind_speed = wind[2]
			wind_direction = windir.get( wind_short_direction, wind_short_direction )
			wind_speed = _localize_unit( wind_speed, "speed" )
			daylight = re.findall( pattern_value, daylight_block[count] )
			sunrise = _localize_unit( "%s AM" % daylight[0], "time" )
			sunset = _localize_unit( "%s PM" % daylight[1], "time" )
			humidity = re.findall( pattern_value, humidity_block[count] )[1]
			if( count == 0 and int(today) == int(dates[0][1]) ):
				if( first_heading == "Tonight" ):
					if( current_ampm == "PM" ):				
						self.forecast += [ ( "CACHE", "%s %s" % ( month_list[int(month)-1], today ), "", "", "", "", "", "", "", "" ) ]
						continue		
			if( count != 0 ):
				if( int( dates[count][1] ) < int( dates[count-1][1] ) ):
					month = str( int(month) + 1 )
			try:
				self.forecast += [ ( ["Today", dates[count][0]][ count != 0 ], "%s %s" % ( month_list[int(month)-1], dates[count][1] ), iconpath, brief[count], _localize_unit(hi_low[count][0], "temp"), _localize_unit(hi_low[count][1], "temp"), precip[count], wind_direction, wind_speed, wind_short_direction, sunrise, sunset, humidity ) ]
			except:
				self.forecast += [ ( ["Today", dates[count][0]][ count != 0 ], "%s %s" % ( month_list[int(month)-1], dates[count][1] ), iconpath, brief[count], _localize_unit(hi_low[count][0], "temp"), "N/A", precip[count], wind_direction, wind_speed, wind_short_direction, sunrise, sunset, humidity ) ]
			# print self.forecast
		
		printlog( "Extended Forecast Done.." )
		return
		
	except:
		self.forecast = [ "ERROR", ]
		return

class WUNDER_ForecastHourlyParser:
    def __init__( self, htmlSource, translate ):
        self.forecast = []
        self.translate = translate
        # only need to parse source if there is source
        if ( htmlSource ):
            self._get_forecast( htmlSource )

    def _get_forecast( self, htmlSource ):
	# regex patterns
	pattern_hour = "<th class=\"taC\">([^<]+)</th>"
	pattern_temp = "<div>([0-9]+) / [0-9]+</div>[^<]+<div class=\"hourlyBars\">"
	pattern_icon = "<img src=\"http://icons-ak.wxug.com/i/c/k/(.+?).gif\""
	pattern_cond = "alt=\"\" class=\"condIcon\" /></a></div>([^<]+)</td>"
	pattern_percent = "([0-9]+)[%]"
	pattern_wind = "<img src=\"http://icons-ak.wxug.com/graphics/[^.]+.gif\" width=\"[^\"]+\" height=\"[^\"]+\" alt=\"[^\"]+\" /></div>[^<]+<div>([^<]+)</div>"
	pattern_time = "<div id=\"infoTime\"><span>(.+?)</span>"

	# fetch info.
	printlog( "Fetching Hourly Forecast from Wunderground.com..." )
	raw_hour = re.findall( pattern_hour, htmlSource )
	temp = re.findall( pattern_temp, htmlSource )
	icon = re.findall( pattern_icon, htmlSource )
	cond = re.findall( pattern_cond, htmlSource )
	percent = re.findall( pattern_percent, htmlSource )
	wind = re.findall( pattern_wind, htmlSource )
	local_time = re.findall( pattern_time, htmlSource )
	# print "icons", icon, "cond", cond, "percent", percent, "wind", wind, "raw_hour", raw_hour, "temp", temp, "wind", wind, "local_time", local_time

	try:
		# making hour table
		printlog( "Making Forecast Table.." )
                if ( self.translate is not None ):
			# we separate each item with single pipe
			text = ""
			try:
			   text += "|".join( cond ).replace("\n","").replace("\t","")
			except:
			   printlog( "No Info : 10day Brief" )
			# translate text
			text = _translate_text( text, self.translate )
			# split text into it's original list
			cond = text.split( "|" )
		current_hour = int( local_time[0].split(":")[0] )
		if ( local_time[0].split(" ")[1] == "PM" and current_hour != 12 ): current_hour += 12
		elif ( local_time[0].split(" ")[1] == "AM" and current_hour == 12 ): current_hour = 0
		localdate = " ".join( local_time[0].split(" ")[4:] )
		year = localdate.split(" ")[-1]
		date = time.strptime( localdate, "%B %d, %Y" )
		yeardate = time.strftime( "%j", date )
		for count in range(0, len(raw_hour)):
			yeardate_new = str( int(yeardate) + ( count > 7 ) + ( current_hour == 23 ) )
			date = time.strptime( "%s %s" % ( yeardate_new, year ), "%j %Y" )
			date = time.strftime( "%b %d", date )
			iconpath = "/".join( [ "special://temp", "weather", "128x128", "%s.png" % icondir.get( icon[ count ], "na" ) ] )	
			feelslike = _getFeelsLike( int(_localize_unit( temp[count], "tempf2c" )), int(_localize_unit( wind[count].split(" mph ")[0], "speedmph2kmh" ).split(" ")[0]), int(percent[ [count, count+16][count>7] ]) )
			windspeed = _localize_unit( wind[count].split(" mph ")[0], "speed" )
			winddirection = wind[count].split(" mph ")[1]
			hour = raw_hour[count].replace("&nbsp;"," ")
			hour24 = int( hour.split(" ")[0] ) + 12 * ( hour.split(" ")[1] == "PM" ) + 24 * ( count > 7 ) - 12 * ( int( hour.split(" ")[0] ) == 12 )
			if ( current_hour <= hour24 ):
				self.forecast += [ ( _localize_unit("%s:00 %s" % ( hour.split(" ")[0], hour.split(" ")[1] ), "time"), date, iconpath, _localize_unit(temp[count]), cond[count].replace("\n","").replace("\t",""), _english_localize_unit(feelslike), percent[ [count+8, count+24][count>7] ], percent[ [count, count+16][count>7] ], windir.get( winddirection, winddirection ), windspeed, winddirection.replace("North","N").replace("East","E").replace("South","S").replace("West","W") ) ]
				
	except:
		self.forecast = [ "ERROR", ]
		return

