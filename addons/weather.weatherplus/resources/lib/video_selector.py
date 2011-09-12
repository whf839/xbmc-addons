# main imports
import sys
import os

try:
    import xbmc
    DEBUG = False
except:
    DEBUG = True

import xbmcgui
import re
import time
from xbmcaddon import Addon

__Settings__ = Addon(id="weather.weatherplus")

class Main:
	def __init__(self, loc=1):
		base_url = "http://v.imwx.com/v/wxcom/"
		dialog = xbmcgui.Dialog()
		video_num = dialog.select("Which Video Slot Would You Change?", ["Video #1", "Video #2", "Video #3"])
		if ( video_num != -1 ):
			slot = video_num
		else:
			__Settings__.openSettings()
			return
		category = dialog.select("Choose a Category", ["National", "Northeast", "South", "Midwest", "West", "Travel"])
		if ( category == 0 ):
			video = dialog.select("Select a Video You Want", ["A National Look at the Next 3 Days", "Latest forecast for severe weather", "Today's top forecasts", "Weekly Planner"])
			video_url = base_url + ("national.mov", "stormwatch.mov", "topstory.mov", "weekly.mov")[video]
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("A National Look at the Next 3 Days", "Latest forecast for severe weather", "Today's top forecasts", "Weekly Planner")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		elif ( category == 1 ):
			video = dialog.select("Select a Video You Want", ["Northeast Regional Forecast", "Albany", "Baltimore", "Boston", "Buffalo", "Burlington", "Charleston", "Cincinnati", "Cleveland", "Columbus", "Harrisburg", "Hartford", "Johnstown", "New York", "Norfolk", "Philadephia", "Pittsburgh", "Providence", "Richmond", "Roanoke", "Rochester", "Syracuse", "Toledo", "Washington, DC", "Wilkes-Barre"])
			video_url = base_url + ("northeast", "albany", "baltimore", "boston", "buffalo", "burlington", "charleston", "cincinnati", "cleveland", "columbus", "harrisburg", "hartford", "johnstown", "newyorkcity", "norfolk", "philadephia", "pittsburgh", "providence", "richmond", "roanoke", "rochester", "syracuse", "toledo", "washingtondc", "wilkes-barre")[video] + ".mov"
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("Northeast Regional Forecast", "Albany", "Baltimore", "Boston", "Buffalo", "Burlington", "Charleston", "Cincinnati", "Cleveland", "Columbus", "Harrisburg", "Hartford", "Johnstown", "New York", "Norfolk", "Philadephia", "Pittsburgh", "Providence", "Richmond", "Roanoke", "Rochester", "Syracuse", "Toledo", "Washington, DC", "Wilkes-Barre")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		elif ( category == 2 ):
			video = dialog.select("Select a Video You Want", ["Southeast Regional Forecast", "Atlanta", "Baton Rouge", "Birmingham", "Charlotte", "Chattanooga", "Columbia", "Ft. Myers", "Greensboro", "Greenville", "Huntsville", "Jackson", "Jacksonville", "Knoxville", "Memphis", "Miami", "Mobile", "Nashville", "New Orleans", "Orlando", "Raleigh", "Savannah", "Shreveport", "Tampa", "Tri-Cities", "West Palm Beach"])
			video_url = base_url + ("south", "atlanta", "batonrouge", "birmingham", "charlotte", "chattanooga", "columbia", "ftmyers", "greensboro", "greenville", "huntsville", "jackson", "jacksonville", "knoxville", "memphis", "miami", "mobile", "nashville", "neworleans", "orlando", "raleigh", "savannah", "shreveport", "tampa", "tricities", "westpalm")[video] + ".mov"
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("Southeast Regional Forecast", "Atlanta", "Baton Rouge", "Birmingham", "Charlotte", "Chattanooga", "Columbia", "Ft. Myers", "Greensboro", "Greenville", "Huntsville", "Jackson", "Jacksonville", "Knoxville", "Memphis", "Miami", "Mobile", "Nashville", "New Orleans", "Orlando", "Raleigh", "Savannah", "Shreveport", "Tampa", "Tri-Cities", "West Palm Beach")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		elif ( category == 3 ):
			video = dialog.select("Select a Video You Want", ["Midwest Regional Forecast", "Cedar Rapids", "Champaign", "Chicago", "Davenport", "Dayton", "Des Moines", "Detroit", "Evansville", "Flint", "Grand Rapids", "Green Bay", "Indianapolis", "Kansas City", "Lexington", "Little Rock", "Louisville", "Madison", "Milwaukee", "Minneapolis", "Oklahoma City", "Omaha", "Paducah", "South Bend", "Springfield", "St. Louis", "Tulsa", "Wichita"])
			video_url = base_url + ("midwest", "cedarrapids", "champaign", "chicago", "davenport", "dayton", "desmoines", "detroit", "evansville", "flint", "grandrapids", "greenbay", "indianapolis", "kansascity", "lexington", "littlerock", "louisville", "madison", "milwaukee", "minneapolis", "okc", "omaha", "paducah", "southbend", "springfield", "stlouis", "tulsa", "wichita")[video] + ".mov"
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("Midwest Regional Forecast", "Cedar Rapids", "Champaign", "Chicago", "Davenport", "Dayton", "Des Moines", "Detroit", "Evansville", "Flint", "Grand Rapids", "Green Bay", "Indianapolis", "Kansas City", "Lexington", "Little Rock", "Louisville", "Madison", "Milwaukee", "Minneapolis", "Oklahoma City", "Omaha", "Paducah", "South Bend", "Springfield", "St. Louis", "Tulsa", "Wichita")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		elif ( category == 4 ):
			video = dialog.select("Select a Video You Want", ["West Regional Forecast", "Albuquerque", "Austin", "Colorado Spring", "Dallas", "Denver", "El Paso", "Fresno", "Harlingen", "Honolulu", "Houston", "Las Vegas", "Los Angeles", "Phoenix", "Portland", "Sacramento", "Salt Lake City", "San Antonio", "San Diego", "San Francisco", "Seattle", "Spokane", "Tucson", "Waco"])
			video_url = base_url + ("west", "albuquerque", "austin", "coloradospring", "dallas", "denver", "elpaso", "fresno", "harlingen", "honolulu", "houston", "vegas", "losangeles", "phoenix", "portland", "sacramento", "saltlake", "sanantonio", "sandiego", "sanfrancisco", "seattle", "spokane", "tucson", "waco")[video] + ".mov"
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("West Regional Forecast", "Albuquerque", "Austin", "Colorado Spring", "Dallas", "Denver", "El Paso", "Fresno", "Harlingen", "Honolulu", "Houston", "Las Vegas", "Los Angeles", "Phoenix", "Portland", "Sacramento", "Salt Lake City", "San Antonio", "San Diego", "San Francisco", "Seattle", "Spokane", "Tucson", "Waco")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		elif ( category == 5 ):
			video = dialog.select("Select a Video You Want", ["Driving Forecast", "Boat and Beach Forecast", "Mexico Vacation Forecast", "Hawaii Vacation Forecast", "Florida Vacation Forecast", "Alaska Vacation Forecast", "European Vaccation Forecast", "Bahamas Vacation Forecast", "Canada Vacation Forecast", "Caribbean Vacation Forecast"])
			video_url = base_url + ("driving", "boatandbeach", "mexico", "hawaii", "florida", "alaska", "europe", "bahamas", "canada", "caribbean")[video] + ".mov"
			__Settings__.setSetting( ("video1", "video2", "video3")[slot], ("Driving Forecast", "Boat and Beach Forecast", "Mexico Vacation Forecast", "Hawaii Vacation Forecast", "Florida Vacation Forecast", "Alaska Vacation Forecast", "European Vaccation Forecast", "Bahamas Vacation Forecast", "Canada Vacation Forecast", "Caribbean Vacation Forecast")[video] )
			__Settings__.setSetting( ("video1_url", "video2_url", "video3_url")[slot], video_url )
		__Settings__.openSettings()

	
Main()
