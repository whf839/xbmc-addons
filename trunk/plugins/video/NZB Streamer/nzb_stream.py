import nntplib
import sys
import sre
import string
import threading
import Queue
import rarfile
import os
import time
import traceback
import urllib
import shutil
from pynzb import nzb_parser
from yenc import yenc_decode

#__scriptname__ = sys.modules[ "__main__" ].__scriptname__
#__version__ = sys.modules[ "__main__" ].__version__
#__svn_revision__ = sys.modules[ "__main__" ].__svn_revision__

def get_rar_file_index(subject, last_index):

    # place *.vol###+##.par2 at the end
    rar_match = sre.search("\".+?\.vol\d+\+\d+\.par2\"", subject)
    if rar_match != None:
        last_index -= 1
        return last_index

    # place par2 header first
    rar_match = sre.search("\".+?\.par2\"", subject)
    if rar_match != None:
        return 0

    # place *.part##.rar files simply in order of the ##
    rar_match = sre.search("\".+?\.part(\d+).rar\"", subject)
    if rar_match != None:
        return int(rar_match.group(1))+1

    # place *.rar files before *.r##
    rar_match = sre.search("\".+?\.rar\"", subject)
    if rar_match != None:
        return 1

    # place *.r## files simply in order of the ##
    rar_match = sre.search("\".+?\.r(\d+)\"", subject)
    if rar_match != None:
        return int(rar_match.group(1))+2

    # place anything else at the end
    last_index -= 1
    return last_index

def sort_nzb_rar_files(nzb_files):
    last_index = sys.maxint
    nzb_file_index = dict()
    for nzb_file in nzb_files:
        nzb_file_index[nzb_file.subject] = get_rar_file_index(nzb_file.subject, last_index)
    nzb_files.sort(key=lambda obj: nzb_file_index[obj.subject])


class multipart_file:
    def __init__(self, filename, filepath, nzb_file):
        self.name = filename
        self.path = filepath
        self.stream = None
        self.total_parts = len(nzb_file.segments)
        self.total_bytes = 0 # read from first part
        self.finished = False
        self.finished_parts = 0
        self.finished_bytes = 0
        self.finished_event = threading.Event()


STATUS_INITIALIZING = 0  # downloading/parsing NZB or getting other metadata
STATUS_DOWNLOADING = 1   # downloading multipart binary files
STATUS_READY = 2         # download is ready to be played
STATUS_BROKEN = 3        # some file parts are missing or corrupt
STATUS_FAILED = 4        # a nasty error occurred
STATUS_FINISHED = 5      # download complete

def status_to_string(status):
    return ("initializing", "downloading", "ready", "broken", "failed", "finished")[status]


'''
# progress_update must be a method with a compatible signature:
def nzb_stream_update(current_task,       # string
                      current_status,     # STATUS_*
                      current_file,       # string or None
                      num_files_finished, # int
                      num_files_total,    # int
                      num_bytes_finished, # int
                      num_bytes_total     # int
                     ):
# If a progress_update call returns something other than None, the stream will abort
'''
class nzb_stream:
    def __init__(self, server, port, username, password, num_threads, nzb_url, nzb_directory, par2exe_directory, progress_update = None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.num_threads = num_threads

        self.par2exe_directory = par2exe_directory
        self.progress_update = progress_update

        self.common_prefix = ""
        self.rar_filepath = None
        self.sorted_filenames = list()
        self.downloaded_files = dict()
        self.download_queue = Queue.Queue(0)
        self.decode_queue = Queue.Queue(0)
        self.cancelled = False
        self.finished_files = 0

        self.threads = list()

        # note on calls to _update_progress: a call is made before the task begins and after the task completes;
        # this allows the consumer to cancel during the task

        nzb_string = ""
        try:
            if self._update_progress("Downloading NZB", STATUS_INITIALIZING, os.path.basename(nzb_url)): return
            urllib.urlopen(nzb_url)
            nzb_string = string.join(urllib.urlopen(nzb_url).readlines(), "")
            if self._update_progress("Downloading NZB", STATUS_INITIALIZING, os.path.basename(nzb_url)): return

            if self._update_progress("Parsing NZB", STATUS_INITIALIZING, os.path.basename(nzb_url)): return
            nzb_files = nzb_parser.parse(nzb_string)
            sort_nzb_rar_files(nzb_files)

            for nzb_file in nzb_files:
                filename = sre.search("\"(.*?)\"", nzb_file.subject).group(1)
                filename = filename.encode('utf8').lower()
                self.sorted_filenames.append(filename)

            self.common_prefix = os.path.commonprefix(self.sorted_filenames).rstrip(". ")
            if self.common_prefix == "":
                self.common_prefix = self.sorted_filenames[0]
            elif os.path.splitext(self.common_prefix)[1] == ".nzb":
                self.common_prefix = os.path.splitext(self.common_prefix)[0]
            print self.common_prefix

            self.download_directory = os.path.join(nzb_directory, self.common_prefix)
            self.status_filepath = os.path.join(self.download_directory, self.common_prefix + ".status")

            if self._update_progress("Parsing NZB", STATUS_INITIALIZING, os.path.basename(nzb_url)): return

            # make sure the download directory exists
            try: os.makedirs(self.download_directory)
            except: pass

            nzb_filepath = os.path.join(nzb_directory, self.common_prefix + ".nzb" )
            nzb_filepath = nzb_filepath.encode('utf8')
            print nzb_filepath
            #if os.path.exists(nzb_filepath) and os.path.isdir(nzb_filepath):
            #    shutil.rmtree(nzb_filepath) # remove the directory containing the nzb; it is rewritten below
            nzb = open(nzb_filepath, "w+b")
            nzb.write(nzb_string)
            nzb.close()

            # run par2 if we already have the .par2 file
            par2_file = os.path.join(self.download_directory, self.common_prefix + ".par2")
            par2_targets = None
            if os.path.exists(par2_file):
                if self._update_progress("Verifying with PAR2", STATUS_INITIALIZING, os.path.basename(par2_file)): return
                par2_targets = self._verify_with_par2(par2_file)
                if self._update_progress("Verifying with PAR2", STATUS_INITIALIZING, os.path.basename(par2_file)): return

                #for target in par2_targets:
                #    print "\t" + target + ": " + par2_targets[target]

            nested_nzbs = list()

            for nzb_file in nzb_files:
                filename = sre.search("\"(.*?)\"", nzb_file.subject.lower()).group(1)
                filename = filename.encode('utf8')
                filepath = os.path.join(self.download_directory, filename)
                filepath = filepath.encode('utf8')

                if self._update_progress("Queueing file", STATUS_INITIALIZING, filename): return

                print filepath
                # create an empty file if it doesn't exist
                if not os.path.exists(filepath):
                    open(filepath, "w+b").close()

                if not self.rar_filepath:
                    rar_match = sre.search("(.+?)\.part(\d+).rar", filename)
                    if rar_match and int(rar_match.group(2)) == 1:
                        self.rar_filepath = filepath
                        self.rar_filename = os.path.basename(filepath)
                    else:
                        rar_match = sre.search("(.+?)\.rar", filename)
                        if rar_match:
                            self.rar_filepath = filepath
                            self.rar_filename = os.path.basename(filepath)
                    if self.rar_filepath:
                        print "First RAR file is " + self.rar_filename

                if os.path.splitext(filepath)[1] == ".nzb":
                    nested_nzbs.append(filepath)

                self.downloaded_files[filename] = multipart_file(filename, filepath, nzb_file)

                # skip non-PAR2 files if par2 validated it
                if par2_targets and par2_targets.has_key(filename) and par2_targets[filename] == "found":
                    print "PAR2 verified " + filename + ": skipping"
                    self.finished_files += 1
                    self.downloaded_files[filename].finished = True
                    continue
                print "PAR2 didn't verify " + filename + ": queueing for download"

                # sort segments in ascending order by article number
                nzb_file.segments.sort(key=lambda obj: obj.number)
                for nzb_segment in nzb_file.segments:
                    self.download_queue.put([filename, nzb_file, nzb_segment], timeout=1)

            # if no RAR file and no nested NZBs, abort
            if not self.rar_filepath:
                if len(nested_nzbs) == 0:
                    raise Exception("nothing to do: NZB did not have a RAR file or any nested NZBs")
                self.rar_filepath = self.rar_filename = ""

            if par2_targets and par2_targets.has_key(self.rar_filename) and par2_targets[self.rar_filename] == "found":
                if self._update_progress("First RAR is ready.", STATUS_READY, self.rar_filepath): return

            if self._update_progress("Starting " + `self.num_threads` + " download threads", STATUS_INITIALIZING): return

            # start download threads
            for i in range(self.num_threads):
                thread = threading.Thread(name=`i`, target=self._download_thread)
                thread.start()
                self.threads.append(thread)

            if self._update_progress("Starting " + `self.num_threads` + " download threads", STATUS_INITIALIZING): return

            # decode parts as they are downloaded
            # begins streaming when the first RAR is finished
            self._decode_loop()

            # if no RAR file was found, try the nested NZBs that were downloaded
            if self.rar_filepath == "":
                if self._update_progress("No RAR files found.", STATUS_INITIALIZING): return
                for nested_nzb_filepath in nested_nzbs:
                    if self._update_progress("Trying nested NZB: " + os.path.basename(nested_nzb_filepath), STATUS_INITIALIZING): return
                    nzb_stream(self.server, self.port, self.username, self.password,
                               self.num_threads,
                               urllib.pathname2url(nested_nzb_filepath),
                               nzb_directory,
                               par2exe_directory,
                               self.progress_update)

        except:
            traceback.print_exc()
            self._update_progress("Error parsing NZB", STATUS_FAILED, self.common_prefix)

        # cancel all threads before returning
        self.cancelled = True
        for thread in self.threads:
            if thread.isAlive():
                print "Cancelled thread " + thread.getName()
                thread.join()


    def _update_progress(self, current_task, current_status, current_file = None,
                         num_files_finished = 0, num_files_total = 0,
                         num_bytes_finished = 0, num_bytes_total = 0):
        if self.progress_update:
            return self.progress_update(current_task, current_status, current_file, num_files_finished, num_files_total, num_bytes_finished, num_bytes_total)


    def _verify_with_par2(self, par2_file):
        try:
            if not os.path.exists(self.status_filepath):
                cmd = '"' + os.path.join(self.par2exe_directory, 'par2.exe') + '"'
                args = ' v -q "' + par2_file + '"'
                print cmd, args, self.status_filepath
                cmd = '"' + cmd + args + ' > "' + self.status_filepath + '""'
                cmd.encode('utf8')
                os.system(cmd)
            #print par2exe.readlines()
            #from subprocess import *
            #par2exe = Popen(["c:/temp/par2.exe"], stdout=PIPE, stderr=STDOUT, stdin=PIPE)
            #par2exe.wait()
            lines =  open(self.status_filepath).readlines()
            par2_targets = dict()
            for line in lines:
                # Target: "foo.rar" - found.
                # Target: "bar.rar" - missing.
                # Target: "baz.rar" - damaged.
                par2_target_match = sre.search("Target: \"(.+?)\" - (\S+)\.", line)
                if par2_target_match:
                    par2_targets[par2_target_match.group(1).lower()] = par2_target_match.group(2)
            return par2_targets

        except:
            traceback.print_exc()


    # peek at a part of a multipart file to get its expected size after decoding
    def _get_nzb_file_size(self, nzb_file):
        try:
            if not self.aux_connection:
                self.aux_connection = nntplib.NNTP(self.server, self.port, self.username, self.password)
                self.aux_group = ""

            # switch groups if necessary
            if self.aux_group != nzb_file.groups[0]:
                self.aux_group = nzb_file.groups[0]
                response, count, first, last, name = connection.group(self.aux_group)

            # download the segment
            response, number, id, encoded_lines = connection.body('<' + nzb_file.segments[0].message_id + '>')

            decode_result = yenc_decode(encoded_lines)
            if not decode_result:
                raise Exception("malformed yEnc file: " + encoded_lines)
            decoded_segment, part_number, part_begin, part_end, file_size = decode_result

            return file_size

        except (nntplib.NNTPTemporaryError, nntplib.NNTPPermanentError), ex:
            code = ex.response[:3]
            # authorization rejected
            if code == "452" or code == "502" or code == "480":
                raise Exception("Sending newsgroup command", "NNTP authorization failed! Check username and password.")

            # invalid article or article not found
            elif code == "423" or code == "430":
                raise Exception("Article " + nzb_file.segments[0].message_id + " not found.")


    def _download_thread(self):
        try:
            current_thread = threading.currentThread();

            connection = nntplib.NNTP(self.server, self.port, self.username, self.password)
            current_group = ""

            while 1:
                try:
                    if self.cancelled:
                        break

                    filename, nzb_file, nzb_segment = self.download_queue.get(True, 1)
                    #print "Thread " + `current_thread` + " downloading " + filename + " : " + `nzb_segment.number`

                # if the Queue.get() times out, close the thread due to lack of work
                except Queue.Empty:
                    #connection.quit()
                    print "Thread finished."
                    break

                # record current time
                start = time.time()

                try:
                    # switch groups if necessary
                    if current_group != nzb_file.groups[0]:
                        current_group = nzb_file.groups[0]
                        response, count, first, last, name = connection.group(current_group)

                    # download the segment
                    response, number, id, encoded_lines = connection.body('<' + nzb_segment.message_id + '>')

                except nntplib.NNTPTemporaryError, ex:
                    code = ex.response[:3]
                    # invalid article or article not found
                    if code == "423" or code == "430":
                        print "Article " + nzb_segment.message_id + " not found."
                        encoded_lines = [""] # decode will fail, status will be set to BROKEN
                    else:
                        raise ex

                duration = time.time() - start

                # put the buffer on the queue to be decoded and written to disk
                self.decode_queue.put([filename, nzb_segment, encoded_lines, duration], 1)

        except (nntplib.NNTPTemporaryError, nntplib.NNTPPermanentError), ex:
            code = ex.response[:3]
            # authorization rejected
            if code == "452" or code == "502" or code == "480":
                self._update_progress("Sending newsgroup command", STATUS_FAILED, "NNTP authorization failed! Check username and password.")
            else:
                raise ex

        except Exception:
            print `current_thread` + " caught exception: ",
            traceback.print_exc()
            sys.stdout.flush()
            sys.stderr.flush()


    def _decode_loop(self):
        try:
            current_status = STATUS_DOWNLOADING

            while 1:
                try:
                    filename, nzb_segment, encoded_lines, duration = self.decode_queue.get(True, 5)
                except Queue.Empty:
                    # if all download threads are dead, abort
                    all_threads_dead = True
                    for thread in self.threads:
                        if thread.isAlive():
                            all_threads_dead = False

                    if all_threads_dead:
                        return

                    # check for user cancellation
                    if self._update_progress("Waiting to decode a segment", current_status):
                        return

                    # continue to wait for a segment to decode
                    continue

                downloaded_file = self.downloaded_files[filename]

                try:
                    # decode the segment and capture part metadata
                    #print "Decoding " + filename + " : " + encoded_lines[0]
                    #print encoded_lines[1]
                    decode_result = yenc_decode(encoded_lines)
                    if not decode_result:
                        raise Exception("malformed yEnc file: " + encoded_lines[0])
                    decoded_segment, part_number, part_begin, part_end, file_size = decode_result
                except Exception, ex:
                    current_status = STATUS_BROKEN
                    if self._update_progress("Part " + `nzb_segment.number` + " is missing or corrupt.", current_status, filename,
                                             self.finished_files, len(self.sorted_filenames),
                                             downloaded_file.finished_bytes, downloaded_file.total_bytes):
                        return
                    continue

                if part_number != nzb_segment.number:
                    print "Warning: decoded part number " + `part_number` + " does not match requested segment number " + `nzb_segment.number`

                # first part decoded for a file sets the total file size;
                # each part is tested to make sure the file size is equal
                if downloaded_file.total_bytes == 0:
                    downloaded_file.total_bytes = file_size
                elif downloaded_file.total_bytes != file_size:
                    print "Warning: decoded part number " + `part_number` + " reports file size different from first part."

                current_file = filename
                if current_status == STATUS_READY:
                    current_file = self.rar_filepath

                if self._update_progress(downloaded_file.name + ":" + `nzb_segment.number`, current_status, current_file,
                                         self.finished_files, len(self.sorted_filenames),
                                         downloaded_file.finished_bytes, downloaded_file.total_bytes):
                     return

                # open the file's stream if it's not yet open
                if downloaded_file.stream == None:
                    print "Opening stream for " + filename
                    downloaded_file.stream = open(downloaded_file.path, "w+b")

                    # allocate entire file size at once
                    downloaded_file.stream.seek(downloaded_file.total_bytes-1)
                    downloaded_file.stream.write('\0')

                # write decoded bytes to the open stream
                downloaded_file.stream.seek(part_begin-1) # part_begin is 1-based, seek offsets are 0-based
                downloaded_file.stream.write(decoded_segment)
                #print "Decoded " + filename + " : " + `part_number`

                # if file has all parts, close its stream and trigger the finished event
                downloaded_file.finished_parts += 1
                downloaded_file.finished_bytes += len(decoded_segment)

                if downloaded_file.finished_parts == downloaded_file.total_parts:
                    print "File " + downloaded_file.name + " is finished."
                    downloaded_file.stream.close()

                    self.finished_files += 1
                    downloaded_file.finished = True
                    downloaded_file.finished_event.set()

                    # delete the par2 status file after a file finishes
                    try: os.remove(self.status_filepath)
                    except: pass

                    # check after finishing a file if rar_filepath is finished
                    # if so, change status to READY
                    if downloaded_file.name == self.rar_filename and current_status != STATUS_BROKEN:
                        current_status = STATUS_READY

                    if self.finished_files == len(self.sorted_filenames):
                        break

        except Exception, ex:
            traceback.print_exc()
            self._update_progress("Decode loop caused exception: " + str(ex), STATUS_FAILED)
