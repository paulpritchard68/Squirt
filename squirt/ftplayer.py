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
            ftp.delete(entry.split(' ')[-1])
            yield entry

    ftp.close

def ftp_get(script):
    """ Retrieves remote files matching file mask
        Parameter script is a dictionary object 
        Yields each of the found files """

    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    if script.get('local') != None:
        local = script.get('local')
    else:
        local = os.getcwd()

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') == None:
            file_name =  entry.split(' ')[-1]
            local_file = os.path.join(local, file_name)
            try:
                with open(local_file, 'wb') as f:
                    ftp.retrbinary('RETR %s' % file_name, lambda data: f.write(data))
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
