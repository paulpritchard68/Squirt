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


def ftp_chmod(script):
    """ Chmods the remote files matching the file mask
        Parameter script is a dictionary object
        returns True if successful
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
            ftp.sendcmd('site chmod %s %s' % (script.get('do').split('-')[-1] , entry.split(' ')[-1]))
            yield entry

    ftp.quit()


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

    ftp.quit()

def ftp_get(script):
    """ Retrieves remote files matching file mask
        Parameter script is a dictionary object 
        Yields each of the found files """

    # First build a list of files to retrieve
    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    ftp.quit()

    # Position to the local folder
    if script.get('local') != None:
        local = script.get('local')
    else:
        local = os.getcwd()

    # Then retrieve the files
    for entry in entries:
        if pattern.search(entry) != None or script.get('files') == None:
            file_name =  entry.split(' ')[-1]
            local_file = os.path.join(local, file_name)
            try:
                ftp = FTP(script.get('host'), script.get('user'), script.get('password'))
                if script.get('remote') != None:
                    ftp.cwd(script.get('remote'))
                with open(local_file, 'wb') as f:
                    ftp.retrbinary('RETR %s' % file_name, lambda data: f.write(data))
                yield entry
                try:
                    ftp.quit()
                except:
                    pass
            except:
                yield '%s Found but not retrieved' % entry

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

    ftp.quit()

def ftp_put(script):
    """ Sends local files matching file mask to remote server
        Parameter script is a dictionary object 
        Yields each of the found files """

    ftp = FTP(script.get('host'), script.get('user'), script.get('password'))

    if script.get('remote') != None:
        ftp.cwd(script.get('remote'))

    if script.get('local') != None:
        local = script.get('local')
        os.chdir(local)
    else:
        local = os.getcwd()

    entries = os.listdir(local) 

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') == None:
            print 'STOR %s/%s' % (local, entry)
            ftp.storbinary('STOR %s' % entry, open(entry, 'rb'), 1024)
            yield entry

    ftp.quit()
