"""
    Plugin for streaming Apple Movie Trailers
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

import time
import xml.dom.minidom
import urllib


# plugin constants
__plugin__ = "Apple Movie Trailers II"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Apple%20Movie%20Trailers%II"
__credits__ = "Team XBMC"
__version__ = "1.0"


class _Parser:
    """
        Parses an xml document for videos
    """
    def __init__( self, xml_path, source, settings ):
        # initialize our videos list
        self.success = True
        self.settings = settings
        # get the list
        if ( source == 0 ):
            self._get_current_videos( xml_path )
        else:
            pass#self._get_recent_videos( xml_path )

    def _get_current_videos( self, xml_path ):
        """
    <movieinfo id="2566">
        <info>
            <title>88 Minutes</title>
            <runtime>2:30</runtime>
            <rating>R</rating>
            <studio>Sony Pictures</studio>
            <postdate>2008-01-28</postdate>
            <releasedate>2008-04-18</releasedate>
            <copyright>© Copyright 2008 Sony Pictures</copyright>
            <director>Jon Avnet</director>
            <description>Al Pacino stars as Dr. Jack Gramm, a college professor who moonlights as a forensic psychiatrist for the FBI. When Gramm receives a death threat claiming he has only 88 minutes to live, he must use all his skills and training to narrow down the possible suspects, who include a disgruntled student, a jilted former lover, and a serial killer who is already on death row, before his time runs out.</description>
        </info>
        <cast>
            <name>Al Pacino</name>
            <name>Alicia Witt</name>
            <name>Leelee Sobieski</name>
            <name>Amy Brenneman</name>
            <name>Deborah Kara Unger</name>
        </cast>
        <genre>
            <name>Thriller</name>
        </genre>
        <poster>
            <location>http://images.apple.com/moviesxml/s/sony_pictures/posters/88minutes_l200801281619.jpg</location>
            <xlarge>http://images.apple.com/moviesxml/s/sony_pictures/posters/88minutes_xl200801281619.jpg</xlarge>
        </poster>
        <preview>
            <large filesize="22891611">http://movies.apple.com/movies/sony_pictures/88_minutes/88_minutes-tlr1_h640w.mov</large>
        </preview>

        """
        # load and parse xmlSource
        doc = xml.dom.minidom.parse( xml_path )
##        # gather all video records <movieinfo>
##        movies = doc.getElementsByTagName( "movieinfo" )
        # enumerate thru the movie list and gather info
        for movie in doc.getElementsByTagName( "movieinfo" ):
            try:
                info = movie.getElementsByTagName( "info" )
                print
                print repr(info[ 0 ].toxml())
                cast = movie.getElementsByTagName( "cast" )
                genre = movie.getElementsByTagName( "genre" )
                poster = movie.getElementsByTagName( "poster" )
                preview = movie.getElementsByTagName( "preview" )
                # info
                title = info[ 0 ].getElementsByTagName( "title" )[ 0 ].firstChild.nodeValue
                runtime = info[ 0 ].getElementsByTagName( "runtime" )[ 0 ].firstChild.nodeValue
                mpaa = info[ 0 ].getElementsByTagName( "rating" )[ 0 ].firstChild.nodeValue
                studio = info[ 0 ].getElementsByTagName( "studio" )[ 0 ].firstChild.nodeValue
                postdate = info[ 0 ].getElementsByTagName( "postdate" )[ 0 ].firstChild.nodeValue
                releasedate = info[ 0 ].getElementsByTagName( "releasedate" )[ 0 ].firstChild.nodeValue
                copyright = info[ 0 ].getElementsByTagName( "copyright" )[ 0 ].firstChild.nodeValue
                director = info[ 0 ].getElementsByTagName( "director" )[ 0 ].firstChild.nodeValue
                plot = info[ 0 ].getElementsByTagName( "description" )[ 0 ].firstChild.nodeValue
                # actors
                actors = []
                if ( cast ):
                    for actor in cast[ 0 ].getElementsByTagName( "name" ):
                        actors += [ actor.firstChild.nodeValue ]
                # genres
                genres = []
                for g in genre[ 0 ].getElementsByTagName( "name" ):
                    genres += [ g.firstChild.nodeValue ]
                genre = " / ".join( genres )
                # poster
                if ( self.settings[ "poster" ] ):
                    poster = movie.getElementsByTagName( "poster" )[ 0 ].getElementsByTagName( "xlarge" )[ 0 ].firstChild.nodeValue
                else:
                    poster = movie.getElementsByTagName( "poster" )[ 0 ].getElementsByTagName( "location" )[ 0 ].firstChild.nodeValue
                # trailer
                trailer = movie.getElementsByTagName( "preview" )[ 0 ].getElementsByTagName( "large" )[ 0 ].firstChild.nodeValue
                size = movie.getElementsByTagName( "preview" )[ 0 ].getElementsByTagName( "large" )[ 0 ].getAttribute( "filesize" )
                """
                <poster>
                    <location>http://images.apple.com/moviesxml/s/sony_pictures/posters/88minutes_l200801281619.jpg</location>
                    <xlarge>http://images.apple.com/moviesxml/s/sony_pictures/posters/88minutes_xl200801281619.jpg</xlarge>
                </poster>
                <preview>
                    <large filesize="22891611">http://movies.apple.com/movies/sony_pictures/88_minutes/88_minutes-tlr1_h640w.mov</large>
                </preview>
                """
                
                # add the item to our media list
                ok = self._add_video( { "title": title, "runtime": runtime, "mpaa": mpaa, "studio": studio, "postdate": postdate, "releasedate": releasedate, "copyright": copyright, "director": director, "plot": plot, "cast": actors, "genre": genre, "poster": poster, "trailer": trailer, "size": size }, 0 )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise

            except:
                # oops print error message
                print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        # clean-up document object
        try: doc.unlink()
        except: pass

    def _add_video( self, video, total ):
        try:
            # set the default icon
            icon = "DefaultVideo.png"
            # only need to add label and thumbnail, setInfo() and addSortMethod() takes care of label2
            listitem = xbmcgui.ListItem( video[ "title" ], iconImage=icon, thumbnailImage=video[ "poster" ] )
            # set the key information
            listitem.setInfo( "video", { "Title": video[ "title" ], "Size": video[ "size" ], "Plot": video[ "plot" ], "PlotOutline": video[ "plot" ], "MPAA": video[ "mpaa" ], "Genre": video[ "genre" ], "Studio": video[ "studio" ], "Director": video[ "director" ], "Duration": video[ "runtime" ], "Cast": video[ "cast" ] } )
            # add the item to the media list
            ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=video[ "trailer" ], listitem=listitem, isFolder=False, totalItems=total )
            # return
            return ok
        except:
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return False


class Main:
    # base url
    BASE_CURRENT_URL = "http://www.apple.com/trailers/home/xml/current.xml"

    # base paths
    BASE_DATA_PATH = xbmc.translatePath( os.path.join( "P:\\plugin_data", "video", __plugin__ ) )
    BASE_CURRENT_SOURCE_PATH = xbmc.translatePath( os.path.join( "P:\\plugin_data", "video", __plugin__, "current.xml" ) )

    def __init__( self ):
        # get users preference
        self._get_settings()
        # fetch videos
        ok = self.get_videos()
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def _get_settings( self ):
        self.settings = {}
        self.settings[ "source" ] = int( xbmcplugin.getSetting( "source" ) )
        self.settings[ "poster" ] = ( xbmcplugin.getSetting( "poster" ) == "true" )
        self.settings[ "rating" ] = int( xbmcplugin.getSetting( "rating" ) )
        self.settings[ "mode" ] = int( xbmcplugin.getSetting( "mode" ) )
        self.settings[ "download_path" ] = xbmcplugin.getSetting( "download_path" )

    def get_videos( self ):
        # fetch xml source
        ok = self.get_xml_source()
        if ( ok ):
            ok = self.parse_xml_source()
        return ok

    def get_xml_source( self ):
        try:
            ok = True
            # set proper source
            base_path = ( self.BASE_CURRENT_SOURCE_PATH, )[ self.settings[ "source" ] ]
            base_url = ( self.BASE_CURRENT_URL, )[ self.settings[ "source" ] ]
            # get the source files date if it exists
            try: date = os.path.getmtime( base_path )
            except: date = 0
            # we only refresh if it's been more than a day, 24hr * 60min * 60sec
            refresh = ( ( time.time() - ( 24 * 60 * 60 ) ) >= date )
            # only fetch source if it's been more than a day
            if ( refresh ):
                # open url
                usock = urllib.urlopen( base_url )
            else:
                # open path
                usock = open( base_path, "r" )
            # read source
            xmlSource = usock.read()
            # close socket
            usock.close()
            # save the xmlSource for future parsing
            if ( refresh ):
                ok = self.save_xml_source( xmlSource )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        return ok

    def save_xml_source( self, xmlSource ):
        try:
            # set proper source
            base_path = ( self.BASE_CURRENT_SOURCE_PATH, )[ self.settings[ "source" ] ]
            # if the path to the source file does not exist create it
            if ( not os.path.isdir( self.BASE_DATA_PATH ) ):
                os.makedirs( self.BASE_DATA_PATH )
            # open source path for writing
            file_object = open( base_path, "w" )
            # wrie xmlSource
            file_object.write( xmlSource )
            # close file object
            file_object.close()
            # return successful
            return True
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return False

    def parse_xml_source( self ):
        # Parse xmlSource for videos
        base_path = ( self.BASE_CURRENT_SOURCE_PATH, )[ self.settings[ "source" ] ]
        parser = _Parser( base_path, self.settings[ "source" ], self.settings )
        return parser.success


if ( __name__ == "__main__" ):
    Main()