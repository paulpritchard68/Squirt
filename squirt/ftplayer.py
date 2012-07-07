#! /usr/bin/python
""" Squirt FTP layer

Copyright (C) 2012 - Paul Pritchard

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>. """

import os
from ftplib import FTP
import re

def ftp_del(script):
    """ Deletes remote files matching file mask
        Parameter script is a dictionary object 
        Returns True if successful
        Failure is not an option """
    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') == None:
            count = 0
            for text in entry.split(' '):
                count += 1
                if count == 10:
                    ftp.delete(text)
            yield entry

    ftp.close

def ftp_get(script):
    """ Retrieves remote files matching file mask
        Parameter script is a dictionary object 
        Returns True if successful
        Failure is not an option """
    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    if script.get('local') != None:
        local = script.get('local')
    else:
        local = os.getcwd()

    entries = ftp.nlst()

    if script.get('files') != None:
        name_length = len(script.get('files'))
    else:
        name_length = 0

    for entry in entries:
        if script.get('files') == entry[0:name_length] or script.get('files') == None:
            local_file = os.path.join(local, entry)
            try:
                with open(local_file, 'wb') as f:
                    ftp.retrbinary('RETR %s' % entry, lambda data: f.write(data))
                yield entry
            except:
                yield '%s Found but not retrieved' % entry

    ftp.close

def ftp_ls(script):
    """ Lists remote files matching file mask
        Parameter script is a dictionary object 
        Yields each of the found files """

    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') == None:
            yield entry

    ftp.close
