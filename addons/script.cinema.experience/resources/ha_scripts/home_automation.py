import xbmc, xbmcaddon

_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString

def activate_on( trigger = "None" ) :
    if trigger == "None":
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - No Trigger Sent, Returning", xbmc.LOGNOTICE )
        return
    xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - Activate On %s Triggered" % trigger, xbmc.LOGNOTICE )
    if trigger == _L_( 32613 ): # Script Start
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32613 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger == _L_( 32609 ): # Trivia Intro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32609 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32615 ): # Trivia
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32615 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32610 ): # Trivia Outro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32610 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32600 ): # Coming Attractions Intro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32600 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32605 ): # Trailer
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32605 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32608 ): # Coming Attractions Outro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32608 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32601 ): # Feature Presentation Intro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32601 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32603 ): # MPAA Rating
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32603 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32611 ): # Countdown
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32611 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32606 ): # Audio Format
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32606 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32616 ): # Movie
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32616 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32602 ): # Feature Presentation Outro
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32602 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32612 ): # Intermission
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32612 ), xbmc.LOGNOTICE )
        # place code below this line
    elif trigger ==_L_( 32614 ): # Script End
        xbmc.log( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32614 ), xbmc.LOGNOTICE )
        # place code below this line
