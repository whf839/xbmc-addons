Find, download, save and display song lyrics from the internet using xml based scrapers. Displays embedded lyrics if available. Abilty to play and tag LRC (simple format) lyrics. *see Tagging lyrics. Can save lyrics to a song's folder or a shared folder. *see settings.

Uses primary scraper first then searches using all other enabled scrapers. *see settings. Will list all available songs for an artist if no song match was found. Artist aliases allow you to input an alias if no artist match was found. Ability to prefetch the next songs lyrics (will not interrupt user if no match was found).

Can run as a stand alone script (gui mode) or in the background. *see Running addon.

[B]Running addon:[/B]
----------------------------------------------------------------------------------------------------------------------------------------------------------
[I]Gui mode[/I] - RunScript(script.xbmc.lyrics)
Allows tagging LRC (simple format) lyrics. Script exits when you close the dialog or music ends.

[I]Background mode[/I] - RunScript(script.xbmc.lyrics,[I]<windowId>[/I])
Allows navigating away while script continues to run. Script exits when music ends. *requires skin support. Use resources/skins/default as a base skin.
----------------------------------------------------------------------------------------------------------------------------------------------------------

[B]Tagging lyrics:[/B]
----------------------------------------------------------------------------------------------------------------------------------------------------------
Addon must be run in gui mode. You must enable Karaoke mode and lyrics tagging in settings (there is a tagging offset setting to aid you).

    1. Start music and launch XBMC Lyrics
    2. Move to the lyrics control
    3. As each lyric is sung, click the appropriate lyric
    4. When done click the save lyrics button
        [I](If the song changes, you will be prompted to save tagged lyrics)[/I]

*tips: Disable crossfading. Any blank line or line that starts with a [ will be considered a non lyric (eg. [Chorus]). These lines are only for formatting and will be skipped when in Karaoke mode. If you make a mistake, you may be able to click a line again, then manually edit the lyrics file later (be careful if a non lyric line was clicked, it must have the same time as the next lyric). 
----------------------------------------------------------------------------------------------------------------------------------------------------------
