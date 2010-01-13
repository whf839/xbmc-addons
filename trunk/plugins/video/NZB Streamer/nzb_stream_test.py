from nzb_stream import *

def nzb_stream_update(current_task,       # string
                      current_status,     # status
                      current_file,       # string or None
                      num_files_finished, # int
                      num_files_total,    # int
                      num_bytes_finished, # int
                      num_bytes_total     # int
                     ):
    print "%s (%s) - %s - %d/%d - %d/%d" % (current_task, current_status, current_file, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)
    sys.stdout.flush()

assert(status_to_string(STATUS_INITIALIZING) == "initializing")
assert(status_to_string(STATUS_FINISHED) == "finished")

server = 'us.news.astraweb.com'
port = 119
username = "chambm"
password = "k6ebh9y4"
num_threads = 1

nzb_url = 'file:///C|/Users/Matt%20Chambers/AppData/Roaming/XBMC/userdata/script_data/NZB/firefly.nzb'
nzb_directory = 'c:/Users/Matt Chambers/AppData/Roaming/XBMC/userdata/script_data/NZB'
par2exe_directory = 'c:/Users/Matt Chambers/AppData/Roaming/XBMC/plugins/Video/NZB/par2'

nzb_stream(server, port, username, password, num_threads, nzb_url, nzb_directory, par2exe_directory, nzb_stream_update)
