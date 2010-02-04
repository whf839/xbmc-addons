#!/usr/bin/python -OO
# Copyright 2008-2009 The SABnzbd-Team <team@sabnzbd.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
sabnzbd.newzbin - newzbin.com support functions
"""

import httplib
import urllib
import time
import logging
import re
import Queue
import socket
try:
    socket.ssl
    _HAVE_SSL = True
except:
    _HAVE_SSL = False

from threading import *
import traceback

"""
import sabnzbd
from sabnzbd.constants import *
from sabnzbd.decorators import synchronized
from sabnzbd.misc import cat_to_opts, sanitize_foldername, bad_fetch
from sabnzbd.nzbstuff import CatConvert
from sabnzbd.codecs import name_fixer
import sabnzbd.newswrapper
import sabnzbd.nzbqueue
import sabnzbd.cfg as cfg
from sabnzbd.lang import T, Ta
from sabnzbd.utils import osx
"""

def _grabnzb(msgid, username, password):
    """ Grab one msgid from newzbin """

    nothing  = (None, None, None, None)
    retry = (60, None, None, None)
    nzo_info = {'msgid': msgid}

    print 'Fetching NZB for Newzbin report #%s' % msgid

    headers = {'User-agent' : 'newzbin.py/1.0'}

    # Connect to Newzbin
    try:
        if _HAVE_SSL:
            conn = httplib.HTTPSConnection('www.newzbin.com')
        else:
            conn = httplib.HTTPConnection('www.newzbin.com')

        postdata = { 'username': username, 'password': password, 'reportid': msgid }
        postdata = urllib.urlencode(postdata)

        headers['Content-type'] = 'application/x-www-form-urlencoded'

        fetchurl = '/api/dnzb/'
        conn.request('POST', fetchurl, postdata, headers)
        response = conn.getresponse()

        # Save debug info if we have to
        data = response.read()

    except:
        print 'Problem accessing Newzbin server, wait 1 min.'
        traceback.print_exc()
        return retry

    # Get the filename
    rcode = response.getheader('X-DNZB-RCode')
    rtext = response.getheader('X-DNZB-RText')
    try:
        nzo_info['more_info'] = response.getheader('X-DNZB-MoreInfo')
    except:
        # Only some reports will generate a moreinfo header
        pass
    if not (rcode or rtext):
        print 'error-nbProtocol'
        return nothing

    # Official return codes:
    # 200 = OK, NZB content follows
    # 400 = Bad Request, please supply all parameters
    #       (this generally means reportid or fileid is missing; missing user/pass gets you a 401)
    # 401 = Unauthorised, check username/password?
    # 402 = Payment Required, not Premium
    # 404 = Not Found, data doesn't exist?
    #       (only working for reportids, see Technical Limitations)
    # 450 = Try Later, wait <x> seconds for counter to reset
    #       (for an explanation of this, see DNZB Rate Limiting)
    # 500 = Internal Server Error, please report to Administrator
    # 503 = Service Unavailable, site is currently down

    if rcode in ('500', '503'):
        print 'Newzbin has a server problem (%s, %s), wait 5 min.' % (rcode, rtext)
        return retry

    if rcode == '450':
        wait_re = re.compile('wait (\d+) seconds')
        try:
            wait = int(wait_re.findall(rtext)[0])
        except:
            wait = 60
        if wait > 60:
            wait = 60
        print "Newzbin says we should wait for %s sec" % wait
        return int(wait+1), None, None, None

    if rcode in ('402'):
        print 'warn-nbCredit'
        return nothing

    if rcode in ('401'):
        print 'warn-nbNoAuth'
        return nothing

    if rcode in ('400', '404'):
        print 'error-nbReport@1', msgid
        return nothing

    if rcode != '200':
        print 'error-nbUnknownError@2', rcode, rtext
        return nothing

    # Process data
    report_name = response.getheader('X-DNZB-Name')
    report_cat  = response.getheader('X-DNZB-Category')
    if not (report_name and report_cat):
        print 'error-nbInfo@1', msgid
        return nothing

    # sanitize report_name
    newname = sanitize_foldername(report_name)
    if len(newname) > 80:
        newname = newname[0:79].strip('. ')
    newname += ".nzb"

    print 'Successfully fetched report %s - %s (cat=%s) (%s)' % (msgid, report_name, report_cat, newname)

    return (newname, data, report_cat, nzo_info)


################################################################################
# sanitize_filename                                                            #
################################################################################
CH_ILLEGAL = r'\/<>?*:|"'
CH_LEGAL   = r'++{}!@-#`'

def sanitize_filename(name):
    """ Return filename with illegal chars converted to legal ones
        and with the par2 extension always in lowercase
    """
    illegal = CH_ILLEGAL
    legal   = CH_LEGAL

    lst = []
    for ch in name.strip():
        if ch in illegal:
            ch = legal[illegal.find(ch)]
        lst.append(ch)
    name = ''.join(lst)

    if not name:
        name = 'unknown'

    name, ext = os.path.splitext(name)
    lowext = ext.lower()
    if lowext == '.par2' and lowext != ext:
        ext = lowext
    return name + ext


def sanitize_foldername(name):
    """ Return foldername with dodgy chars converted to safe ones
        Remove any leading and trailing dot and space characters
    """
    illegal = r'\/<>?*:|"'
    legal   = r'++{}!@-#`'

    lst = []
    for ch in name.strip():
        if ch in illegal:
            ch = legal[illegal.find(ch)]
            lst.append(ch)
        else:
            lst.append(ch)
    name = ''.join(lst)

    name = name.strip('. ')
    if not name:
        name = 'unknown'

    return name