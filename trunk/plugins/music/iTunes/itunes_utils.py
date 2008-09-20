# tell application "iTunes"
#	play (first track of library playlist 1 whose database ID is 17685)
# end tell

import commands

def play_track(playlistid, dbid):
    print commands.getoutput('osascript -e \'tell application "iTunes"\' -e \'play (first track of library playlist %s whose database ID is %s)\' -e \'end tell\'' % (playlistid, dbid))
