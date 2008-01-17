"""
Scraper for http://www.google.com/movies

Nuka1195
"""

import sys
import os

if ( __name__ != "__main__" ):
    import xbmc

from sgmllib import SGMLParser
import urllib
import datetime


__title__ = "Google"
__credit__ = "Nuka1195"


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class _TheaterListParser( SGMLParser ):
    """ 
        Parser Class: parses an html document for a list of theaters 
    """
    def reset( self ):
        SGMLParser.reset( self )
        self.theater_list = {}
        self.current_theater = ""
        self.theater_id = None
        self.theater_name_found = False

    def start_a( self, attrs ):
        for key, value in attrs:
            if ( key == "href" and "&tid=" in value ):
                self.theater_id = value
                self.current_theater = ""

    def end_a( self ):
        if ( self.theater_id is not None ):
            self.theater_list[ self.current_theater ] = _Info( imdb="", label2="", mpaa="", duration="", genre="", premiered="", plot="", thumbnail="", url="http://www.google.com%s" % self.theater_id )
            self.theater_name_found = True
            self.theater_id = None

    def handle_data( self, text ):
        if ( self.theater_id is not None ):
            self.current_theater += text
        elif ( text == "Map" ):
            phone = self.theater_list[ self.current_theater ].duration.find( " - " )
            self.theater_list[ self.current_theater ].label2 = self.theater_list[ self.current_theater ].duration[ phone + 3 : -2 ].strip()
            self.theater_list[ self.current_theater ].duration = self.theater_list[ self.current_theater ].duration[ : phone ]
            self.theater_name_found = False
        elif ( self.theater_name_found ):
            self.theater_list[ self.current_theater ].duration += "%s " % text.strip()


class _ShowtimesParser( SGMLParser ):
    """ 
        Parser Class: parses an html document for movie showtimes
        - creates a key { theater: [#:##] }
    """
    def reset( self ):
        SGMLParser.reset( self )
        self.theaters = {}
        self.current_theater = ""
        self.theater_id = ""
        self.theater_set = False
        self.start_theaters = False

    def start_a( self, attrs ):
        for key, value in attrs:
            if ( key == "href" and value.startswith( "/movies?near=" ) ):
                self.theater_id = value
                self.current_theater = ""
            elif ( key == "href" and "www.imdb.com" in value and self.theaters.has_key( self.current_theater ) ):
                url = value.split( "&" )[ 0 ]
                url = url.split( "=" )[ 1 ]
                self.theaters[ self.current_theater ].imdb = url

    def end_a( self ):
        if ( self.start_theaters ):
            if ( self.theater_id ):
                self.theaters[ self.current_theater ] = _Info( imdb="", label2="", mpaa="", duration="", genre="", premiered="", plot="", thumbnail="", url="http://www.google.com%s" % self.theater_id )
                self.theater_id = ""
                self.show_info = ""
                self.theater_set = True

    def handle_data( self, text ):
        if ( self.start_theaters and text.strip() ):
            if ( self.theater_id ):
                self.current_theater += text
            elif ( text.strip()[ 0 ].isdigit() and ":" in text ):
                if ( self.theaters[ self.current_theater ].premiered ):
                    self.theaters[ self.current_theater ].premiered += ", "
                self.theaters[ self.current_theater ].premiered += text.strip()
                self.theater_set = False
            elif ( self.theater_set and text != "Map" and text != "Trailer" and text != "IMDb" ):
                self.show_info += "%s " % text.strip()
            elif ( self.theater_set and self.show_info ):
                try:
                    self.theaters[ self.current_theater ].duration = self.show_info.split( "-" )[ 0 ].strip()
                    self.theaters[ self.current_theater ].mpaa = self.show_info.split( "-" )[ 1 ].strip()
                    self.theaters[ self.current_theater ].genre = self.show_info.split( "-" )[ 2 ].strip()
                except:
                    pass
        elif ( text == "Show more movies" or text == "Show more films" or text == "Show more theaters" ):
            self.start_theaters = True
            self.theater_id = ""


class ShowtimesFetcher:
    def __init__( self ):
        self.base_url = "http://www.google.com"

    def get_theater_list( self, location ):
        """ *REQUIRED: Returns a list of theaters in your local """
        # format the location
        location = self._format_param( location )
        # get the list of theaters
        theaters = self._get_theater_list( self.base_url + "/movies?near=%s" % ( location, ) )
        # return the list
        return theaters
    
    def get_selection( self, url, day=0 ):
        """ *REQUIRED: Returns movie listing and date for the selected theater or
        theater listing for a specific movie """
        # fetch the list of showtimes
        date, showtimes = self._fetch_showtimes( url, day )
        # if no showtimes, try todays date
        if ( showtimes is None and day > 0 ):
            date, showtimes = self._fetch_showtimes( url, 0 )
        # return our results
        return date, showtimes

    def _fetch_showtimes( self, url, day ):
        """ Fetch showtimes if available """
        try:
            # add the appropriate number of days to todays date
            date = datetime.date.today() + datetime.timedelta( days=day )
            # get the current locals long date format and convert it to what strftime() expects
            if ( __name__ != "__main__" ):
                format = xbmc.getRegion( "datelong" ).replace( "DDDD", "%A" ).replace( "MMMM", "%B" ).replace( "D", "%d" ).replace( "YYYY", "%Y" )
            else:
                format = "%A, %B %d, %Y"
            # format our date
            date = date.strftime( format )
            # create our url
            url = "%s&date=%d" % ( url, day, )
            # open url or local file (if debug)
            if ( not debug ):
                usock = urllib.urlopen( url )
            else:
                usock = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source.txt" ), "r" )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            # if no showtimes were found raise an error
            if ( htmlSource.find( "No showtimes were found" ) >= 0 ):
                raise
            # save htmlSource to a file for testing scraper (if debugWrite)
            if ( debugWrite ):
                file_object = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source.txt" ), "w" )
                file_object.write( htmlSource )
                file_object.close()
            # parse htmlSource for showtimes
            parser = _ShowtimesParser()
            parser.feed( htmlSource )
            parser.close()
            return date, parser.theaters
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return date, None
        
    def _format_param( self, param ):
        """ Converts param to the form expected by www.google.com/movies """
        result = urllib.quote_plus( param )
        return result

    def _get_theater_list( self, url ):
        try:
            # open url or local file (if debug)
            if ( not debug ):
                usock = urllib.urlopen( url )
            else:
                usock = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source3.txt" ), "r" )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            # save htmlSource to a file for testing scraper (if debugWrite)
            if ( debugWrite ):
                file_object = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source3.txt" ), "w" )
                file_object.write( htmlSource )
                file_object.close()
            # parse htmlSource for theaters
            parser = _TheaterListParser()
            parser.feed( htmlSource )
            parser.close()
            return parser.theater_list
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return None


# used for testing only
debug = False
debugWrite = False

if ( __name__ == "__main__" ):
    # used to test get_lyrics() 
    movie = [ "Bee Movie", "The Seeker: the Dark is Rising", "el cantante", "Rush Hour 3", "The Simpsons Movie", "Transformers", "I Now Pronounce You Chuck & Larry", "Transformers", "I Now Pronounce You Chuck & Larry" ]
    location = [ "detroit", "Houston", "detroit", "new york", "London", "Toronto", "33102", "W2 4YL", "T1A 3T9" ]
    #url = [ "http://www.google.com/movies?near=London&tid=6642f6f298729f38" ]
    url = [ "http://www.google.com/movies?near=monroe,+mi&tid=5dae5b1eb982b608" ]

    for cnt in range( 1 ):
        #theaters = ShowtimesFetcher().get_theater_list( location[ cnt ] )
        date, theaters = ShowtimesFetcher().get_selection( url[ cnt ], 5 )
        print date
        print
        if ( theaters ):
            theater_names = theaters.keys()
            theater_names.sort()
            for theater in theater_names:
                for attr in dir( theaters[ theater ] ):
                    if ( not attr.startswith( "__" ) ):
                        print "%s:" % attr.replace( "_", " " ).title(), getattr( theaters[ theater ], attr )
                print "---------------"
