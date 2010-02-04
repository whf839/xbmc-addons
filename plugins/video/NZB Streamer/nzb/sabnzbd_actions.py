import urllib
import re
import rarfile
import xbmc
import xbmcgui
import xbmcplugin
import sys
import os
import simplejson
import nzb_stream
import time
from misc import _get_path
from settings import category_list
class SABnzbdActions:
    def __init__(self, title=None):

        self.RE_NEWZBIN_URL = re.compile(r'/browse/post/(\d+)')

    # TODO: maintain a queue of the currently downloading NZBs
    # (which should show up as a directory item in the list for managing downloads
    #  whose progress dialog has been closed without cancelling the download)

    # try to start a video in a RAR set;
    # if it fails it will inform user and ask to either cancel or continue downloading;
    # returns a pair of booleans, the first is True if playing was successfull and the
    # second is True if the client should continue downloading
    def play_rar(self, rar_filepath):

        try:
            rar_file = rarfile.RarFile(rar_filepath)
            print rar_filepath, rar_file.namelist()

            movie_name = None
            for filename in rar_file.namelist():
                if filename.endswith(".avi") or \
                   filename.endswith(".mkv") or \
                   filename.endswith(".mpg") or \
                   filename.endswith(".ts") or \
                   filename.endswith(".wmv"):
                    movie_name = filename
                    break

            if movie_name != None:
                video_url = urllib.quote(rar_filepath).replace("-", "%2d").replace(".", "%2e")
                video_url = "rar://" + video_url + "/" + movie_name
                print video_url
                #time.sleep(5) # give player time to start
                xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(video_url)
                time.sleep(3) # give player time to start
                #return True, False

            # the movie could not be found or the RAR is passworded
            if not xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).isPlaying():
                if xbmcgui.Dialog().yesno("Unable to find MKV/AVI/MPG file in RAR...cancel download?",
                                          "NZB Streamer requires one of these files with the",
                                          "same filename as the RAR archive to be inside.",
                                          "Passworded RAR files could also cause this.",
                                          "Cancel", # nolabel
                                          "Continue" # yeslabel
                                          ):
                    # if yes, continue downloading in background
                    return False, True
                else:
                    # if no, cancel download
                    return False, False


            # playing worked, continue downloading
            return True, True

        except Exception:
            import traceback
            traceback.print_exc()
            return False, False


    def nzb_stream_update(self,
                          current_task,       # string
                          current_status,     # STATUS_*
                          current_file,       # string or None
                          num_files_finished, # int
                          num_files_total,    # int
                          num_bytes_finished, # int
                          num_bytes_total     # int
                         ):
        cancel = False

        print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_file, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)

        if current_status != self.progress_status:
            print "Status changed from %s to %s (%s)" % (nzb_stream.status_to_string(self.progress_status), \
                                                         nzb_stream.status_to_string(current_status), \
                                                         current_task)

        current_filename = ""
        if current_file: current_filename = os.path.basename(current_file)

        try:
            if self.progress_dialog and self.progress_dialog.iscanceled():
                self.progress_dialog.close()
                self.progress_dialog = None
                self.progress_dialog_closed_by_user = True
                if current_status == nzb_stream.STATUS_INITIALIZING or \
                   current_status == nzb_stream.STATUS_FINISHED or \
                   current_status == nzb_stream.STATUS_READY:
                    cancel = True
                elif xbmcgui.Dialog().yesno("Download in background?", "", "", "", "Cancel", "Continue"):
                    # if yes, continue downloading in background
                    pass
                else:
                    # if no, cancel download
                    cancel = True

            if not self.progress_dialog:
                print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_filename, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)
                sys.stdout.flush()

                if current_status == nzb_stream.STATUS_FAILED:
                    self.notify("An error occurred, see log for details.")
                    cancel = True

                elif current_status == nzb_stream.STATUS_READY and \
                     self.progress_status != nzb_stream.STATUS_READY:
                    # if status is newly READY, start playing
                    playing, continue_downloading = self.play_rar(current_file)
                    cancel = not continue_downloading

                elif current_status == nzb_stream.STATUS_BROKEN and \
                     self.progress_status != nzb_stream.STATUS_BROKEN:
                    # TODO: stop playing current movie if previous status is READY

                    # if status is newly BROKEN, ask user if they want to cancel or continue with a simple download
                    if xbmcgui.Dialog().yesno("Some files are missing or corrupted...",
                                              "NZB Streamer only works on completely intact NZBs.",
                                              "You can cancel now or continue downloading",
                                              "and hope the PAR2 files can repair the damage.",
                                              "Cancel", # nolabel
                                              "Continue" # yeslabel
                                              ):
                        # if yes, continue downloading
                        pass
                    else:
                        # if no, cancel download
                        cancel = True

                elif current_status == nzb_stream.STATUS_FINISHED:
                    self.notify("Finished downloading " + current_file)

                # re-open closed progress dialog if it was automatically closed (and no media is playing)
                elif not self.progress_dialog_closed_by_user and \
                     not xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).isPlaying():
                    self.progress_dialog = xbmcgui.DialogProgress()
                    self.progress_dialog.create("NZB Streamer")

            else:

                percent = 0
                if num_bytes_total > 0:
                    percent = int((num_bytes_finished * float(100)) / num_bytes_total)

                if current_status == nzb_stream.STATUS_FAILED:
                    self.progress_dialog.close()
                    self.progress_dialog = None
                    self.dialog("An error occurred, see log for details.")
                    print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_filename, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)
                    sys.stdout.flush()
                    cancel = True

                elif current_status == nzb_stream.STATUS_INITIALIZING:
                    self.progress_dialog.update(percent,
                                                "Initializing...",
                                                current_task)

                elif current_status == nzb_stream.STATUS_READY and \
                     self.progress_status != nzb_stream.STATUS_READY:
                    self.progress_dialog.update(percent,
                                                "Ready...",
                                                current_filename + " (" + `num_files_finished+1` + "/" + `num_files_total` + ")",
                                                `num_bytes_finished` + " of " + `num_bytes_total` + " bytes")
                    # if status is newly READY, close progress dialog and start playing
                    self.progress_dialog.close()
                    self.progress_dialog = None
                    time.sleep(1) # give dialog time to close
                    playing, continue_downloading = self.play_rar(current_file)
                    cancel = not continue_downloading
                    if not playing and continue_downloading:
                        self.progress_dialog = xbmcgui.DialogProgress()
                        self.progress_dialog.create("NZB Streamer")

                elif current_status == nzb_stream.STATUS_BROKEN and \
                     self.progress_status != nzb_stream.STATUS_BROKEN:
                    # TODO: stop playing current movie if previous status is READY

                    print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_filename, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)
                    sys.stdout.flush()

                    self.progress_dialog.close()
                    self.progress_dialog = None

                    # if status is newly BROKEN, ask user if they want to cancel or continue with a simple download
                    if xbmcgui.Dialog().yesno("Some files are missing or corrupted...",
                                              "NZB Streamer only works on completely intact NZBs.",
                                              "You can cancel now or continue downloading",
                                              "and hope the PAR2 files can repair the damage.",
                                              "Cancel", # nolabel
                                              "Continue" # yeslabel
                                              ):
                        # if yes, continue downloading
                        self.progress_dialog = xbmcgui.DialogProgress()
                        self.progress_dialog.create("NZB Streamer")
                    else:
                        # if no, cancel download
                        self.progress_dialog_closed_by_user = True
                        cancel = True

                elif current_status == nzb_stream.STATUS_DOWNLOADING or \
                     current_status == nzb_stream.STATUS_BROKEN or \
                     current_status == nzb_stream.STATUS_READY:
                    self.progress_dialog.update(percent,
                                                "Downloading...",
                                                current_filename + " (" + `num_files_finished+1` + "/" + `num_files_total` + ")",
                                                `num_bytes_finished` + " of " + `num_bytes_total` + " bytes")

                elif current_status == nzb_stream.STATUS_FINISHED:
                    self.progress_dialog.update(100, "Finished downloading.", current_file)

        except:
            print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_filename, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)
            import traceback
            traceback.print_exc()
            sys.stdout.flush()
            cancel = True

        self.progress_status = current_status
        return cancel


    def _download_nzb(self, url, title='', category='default'):
        try:
            url = url.strip()

            # decide whether to add it as a url, or a newzbin messageid
            newzbin_url = self.RE_NEWZBIN_URL.search(urllib.unquote(url).lower())
            if url and (url.isdigit() or len(url)==5):
                type = 'nzb_msgid'
                nzb_source = url
            elif newzbin_url:
                type = 'nzb_msgid'
                nzb_source = newzbin_url.group(1)
            else:
                type = 'nzb_url'
                nzb_source = urllib.unquote(url)

            self.progress_dialog = xbmcgui.DialogProgress()
            self.progress_dialog.create("NZB Streamer")
            self.progress_dialog_closed_by_user = False
            self.progress_status = nzb_stream.STATUS_INITIALIZING

            if type == "nzb_msgid":
                import newzbin
                username_newzbin = xbmcplugin.getSetting("username_newzbin")
                password_newzbin = xbmcplugin.getSetting("password_newzbin")

                if self.nzb_stream_update("Downloading " + title, self.progress_status, title, 0, 0, 0, 0): return
                newname, nzb_data, nzb_category, more_info = newzbin._grabnzb(nzb_source, username_newzbin, password_newzbin)
                if self.nzb_stream_update("Downloading " + title, self.progress_status, title, 0, 0, 0, 0): return

                if newname and not newname.isdigit():
                    nzb_source = nzb_data
                else:
                    raise Exception("error downloading NZB from Newzbin")

            # Grab the newsgroup server settings
            server = xbmcplugin.getSetting("server")
            port = int(xbmcplugin.getSetting("port"))
            username = xbmcplugin.getSetting("username")
            password = xbmcplugin.getSetting("password")
            num_threads = range(1, 21)[int(xbmcplugin.getSetting("num_threads"))]

            title = title.replace("%20"," ")
            title = title.replace('\'S','\'s').replace('Iii','III').replace('Ii','II')
            title_quoted_match = re.search("\"(.+?)\"", title)
            if title_quoted_match:
                title = title_quoted_match.group(1)

            print server, port, username, num_threads
            #print nzb_url
            #nzb_url = 'file:///C|/Users/Matt%20Chambers/AppData/Roaming/XBMC/userdata/script_data/NZB/exp-fringex264-s01e10.nzb'
            #nzb_url = 'file:///D|/Personal/Downloads/exp-fringex264-s01e10.nzb'
            nzb_directory = os.path.join(xbmc.translatePath("special://profile/"), "plugin_data", "Video", os.path.basename(os.getcwd()))
            par2_directory = os.path.join(xbmc.translatePath("special://home/"), "plugins", "Video", os.path.basename(os.getcwd()), "par2")
            nzb_stream.nzb_stream(server, port, username, password, num_threads, nzb_source, nzb_directory, par2_directory, title, self.nzb_stream_update)

        except:
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

    def notify(self, message, title="NZB Streamer"):
        xbmc.Notification(title, message)

    def dialog(self, message, title="NZB Streamer"):
        xbmcgui.Dialog().ok(title, message)

    def _sabnzbd_action(self, nzo_id):
        ''' Queue actions such as delete and move to top '''
        dl_type = xbmcgui.Dialog().select('Select an action', ['Delete', 'Move to top'])
        print 'dl_type:%s' % dl_type
        if dl_type == 0:
            action = 'queue/delete?uid=%s' % (nzo_id)
        elif dl_type == 1:
            action = 'queue/switch?uid1=%s&uid2=%s' % (nzo_id, '0')
        else: action = ''

        sab_url = self.sabnzbd_url.replace('ACTION_HERE', action)
        print 'sab debug url: %s' % sab_url

        resp = self._connection(sab_url, read=False)
        if resp:
            # reload the queue
            xbmc.executebuiltin('Container.Refresh')
        else:
            self.dialog('Failed to contact SABnzbd')

    def _sabnzbd_queue(self):
        ''' Load sabnzbd's queue using the API and return it as a dictionary '''
        try:
            dict = { "status": "fail", 'folder':'false'}
            sab_url = self.sabnzbd_url.replace('ACTION_HERE', 'api?mode=qstatus&output=json')
            print 'sab_url: %s' % sab_url

            resp = self._connection(sab_url)
            print 'resp:%s' % resp
            if not resp:
                msg = 'Failed to load the SABnzbd queue - Check your settings'
                xbmcgui.Dialog().ok('SABnzbd', msg)
                print 'failed to load sabnzbd queue'
                return {}
            elif '<html>' in resp:
                msg = 'Please add your sabnzbd user/pass in the settings.'
                xbmcgui.Dialog().ok('SABnzbd', msg)
                return {}
            elif 'error: API Key Required' in resp:
                self.dialog('Please enter the API key from SABnzbd into the plugin settings')
            elif 'error: API Key Incorrect' in resp:
                self.dialog('The API key in the plugin settings is incorrect, please change')
            else:
                #proccess the json from sabnzbd into a dictionary
                json = simplejson.loads(resp)

                #extract some info from the json that sabnzbd outputs
                items = []
                for job in json['jobs']:
                    extra = ''
                    item = {}
                    mb = float(job['mb'])
                    mbleft = float(job['mbleft'])
                    if mbleft or mb:
                        perc = (1.0 - mbleft/mb) * 100.00
                    else:
                        perc = 0
                    extra = ' (%d%%)' % perc
                    item['name'] = job['filename'] + extra
                    item['url'] = ''
                    item['id'] = job['id']
                    item['type'] = 'sab_item'
                    items.append(item)

                if not items:
                    item = {}
                    item['name'] = 'The queue is empty'
                    item['url'] = ''
                    item['type'] = 'sab_item'
                    item['id'] = 'empty'
                    items.append(item)

                dict[ "items" ] = {"assets": items, 'folder':False }
                dict[ "status" ] = "ok"

                return dict
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return {}

    def _connection(self, sab_url, read=True):
        ''' General wrapper for sending actions or retrieving a response from the SABnzbd api  '''
        try:
            print 'url:%s' % sab_url
            print 'read:%s' % read
            req = urllib.urlopen(sab_url)
            # return the server responce if requested
            if read:
                print 'getting response'
                resp = req.read()
                req.close()
                return resp
            else:
                req.close()
                return True
        except:
            print 'sab connection failed'
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            if read:
                return 'failed'
            else:
                return False