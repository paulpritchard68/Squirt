#! /usr/bin/python
""" Squirt FTP layer

Copyright (C) 2012 - 2014 Paul Pritchard

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
import ftplib
import re
from squtils import retrieve_local_path


def ftp_chmod(script):
    """ Chmods the remote files matching the file mask
        Parameter script is a dictionary object
        returns True if successful
        Failure is not an option """
    if script.get('port') is None:
        ftp = ftplib.FTP(script.get('host'), script.get('user'), script.get('password'))
    else:
        ftp = ftplib.FTP()
        ftp.connect(script.get('host'), script.get('port'))
        ftp.login(script.get('user'), script.get('password'))

    if script.get('namefmt') != None:
        sndcmd = 'site namefmt ' + str(script.get('namefmt'))
        ftp.sendcmd(sndcmd)

    if script.get('remote') != None:
        try:
            ftp.cwd(script.get('remote'))
        except ftplib.all_errors as err:
            yield 'FTP error: %s' % err
            return

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') is None:
            if script.get('test') is False:
                ftp.sendcmd('site chmod %s %s' % \
                (script.get('do').split('-')[-1], entry.split(' ')[-1]))
            yield entry

    ftp.quit()


def ftp_del(script):
    """ Deletes remote files matching file mask
        Parameter script is a dictionary object
        Returns file names as they are deleted """
    if script.get('port') is None:
        ftp = ftplib.FTP(script.get('host'), script.get('user'), script.get('password'))
    else:
        ftp = ftplib.FTP()
        ftp.connect(script.get('host'), script.get('port'))
        ftp.login(script.get('user'), script.get('password'))

    if script.get('namefmt') != None:
        sndcmd = 'site namefmt ' + str(script.get('namefmt'))
        ftp.sendcmd(sndcmd)

    if script.get('remote') != None:
        try:
            ftp.cwd(script.get('remote'))
        except ftplib.all_errors as err:
            yield 'FTP error: %s' % err
            return

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') is None:
            if script.get('test') is False:
                ftp.delete(entry.split(' ')[-1])
            yield entry

    ftp.quit()

def ftp_get(ftp, local_path, remote_path, script):
    """ Recursively retrieve files, starting at path """
    if not hasattr(ftp, 'attr_name'):
        if script.get('files') != None:
            pattern = re.compile(script.get('files'))
        else:
            pattern = re.compile('')

        local_path = retrieve_local_path(local_path)

        if script.get('port') is None:
            ftp = ftplib.FTP(script.get('host'), \
                      script.get('user'), script.get('password'))
        else:
            ftp = ftplib.FTP()
            ftp.connect(script.get('host'), script.get('port'))
            ftp.login(script.get('user'), script.get('password'))

        if script.get('namefmt') != None:
            sndcmd = 'site namefmt ' + str(script.get('namefmt'))
            ftp.sendcmd(sndcmd)

    try:
        for entry in ftp.mlsd(remote_path, facts=["type"]):
            if entry[1].get('type') == 'dir':
                new_remote_path = remote_path + '/' + entry[0]
                new_local_path = local_path + '/' + entry[0]
                if not os.path.exists(new_local_path) \
                and script.get('test') is False:
                    os.makedirs(new_local_path)
                for new_entry in ftp_get(ftp, new_local_path, \
                                         new_remote_path, script):
                    yield new_entry

            if entry[1].get('type') == 'file' \
            and (pattern.search(entry[0]) != None \
                 or script.get('files') is None):
                local_file = os.path.join(local_path, entry[0])
                remote_file = remote_path + '/' + entry[0]
                yield remote_file
                if script.get('test') is False:
                    with open(local_file, 'wb') as file_get:
                        ftp.retrbinary('RETR %s' % \
                                       remote_file, \
                                       lambda data: file_get.write(data))
                    if script.get('delete') is True:
                        ftp.delete(remote_file)

    except:
        yield 'Error: MLSD command not supported by this server'

    ftp.quit()

def ftp_ls(script):
    """ Lists remote files matching file mask
        Parameter script is a dictionary object
        Yields each of the found files """

    if script.get('port') is None:
        ftp = ftplib.FTP(script.get('host'), script.get('user'), script.get('password'))
    else:
        ftp = ftplib.FTP()
        ftp.connect(script.get('host'), script.get('port'))
        ftp.login(script.get('user'), script.get('password'))


    if script.get('namefmt') != None:
        sndcmd = 'site namefmt ' + str(script.get('namefmt'))
        ftp.sendcmd(sndcmd)

    if script.get('remote') != None:
        try:
            ftp.cwd(script.get('remote'))
        except ftplib.all_errors as err:
            yield 'FTP error: %s' % err
            return

    entries = []
    ftp.retrlines('LIST', lambda data: entries.append(data))

    if script.get('files') != None:
        pattern = re.compile(script.get('files'))
    else:
        pattern = re.compile('')

    for entry in entries:
        if pattern.search(entry) != None or script.get('files') is None:
            yield entry

    ftp.quit()

def ftp_put(script):
    """ Sends local files matching file mask to remote server
        Parameter script is a dictionary object
        Yields each of the found files """

    # Position to the local folder
    if script.get('local') != None:
        local = retrieve_local_path(script.get('local'))
        os.chdir(local)
    else:
        local = os.getcwd()
    local_root = len(local)

    # Remote positioning
    remote = script.get('remote') or ''

    # Build the list of files to send
    entries = os.listdir(local)
    pattern = re.compile(script.get('files') or '')

    # And start sending
    for dirname, dirnames, filenames in os.walk(local):

        remote_dir = dirname[local_root: len(dirname)]
        remote_full_path = remote + remote_dir
        os.chdir(dirname)
        if remote_dir != '':
            if script.get('port') is None:
                ftp = ftplib.FTP(script.get('host'), \
                          script.get('user'), script.get('password'))
            else:
                ftp = ftplib.FTP()
                ftp.connect(script.get('host'), script.get('port'))
                ftp.login(script.get('user'), script.get('password'))

            if script.get('namefmt') != None:
                sndcmd = 'site namefmt ' + str(script.get('namefmt'))
                ftp.sendcmd(sndcmd)

            try:
                ftp.cwd(remote_full_path)
            except:
                if script.get('test') is False:
                    ftp.mkd(remote_full_path)
                yield remote_full_path
            ftp.quit()

        for filename in filenames:
            if pattern.search(filename) != None \
            or script.get('files') is None:
                try:
                    if script.get('port') is None:
                        ftp = ftplib.FTP(script.get('host'), \
                                  script.get('user'), script.get('password'))
                    else:
                        ftp = ftplib.FTP()
                        ftp.connect(script.get('host'), script.get('port'))
                        ftp.login(script.get('user'), script.get('password'))
                    ftp.cwd(remote_full_path)
                    if script.get('test') is False:
                        ftp.storbinary('STOR %s' % \
                                       filename, open(filename, 'rb'), 1024)
                        if script.get('delete') is True:
                            os.remove(filename)
                    yield remote_full_path + '/' + filename
                    ftp.quit()
                except:
                    pass

def ftp_tree(ftp, path, script):
    """ Returns the directory tree starting at path """
    if not hasattr(ftp, 'attr_name'):
        if script.get('port') is None:
            ftp = ftplib.FTP(script.get('host'), \
                      script.get('user'), script.get('password'))
        else:
            ftp = ftplib.FTP()
            ftp.connect(script.get('host'), script.get('port'))
            ftp.login(script.get('user'), script.get('password'))

        if script.get('namefmt') != None:
            sndcmd = 'site namefmt ' + str(script.get('namefmt'))
            try:
                ftp.sendcmd(sndcmd)
            except:
                pass

    try:
        for entry in ftp.mlsd(path, facts=["type"]):
            if entry[1].get('type') == 'dir':
                dir_path = path + '/' + entry[0]
                yield dir_path
                for search_path in ftp_tree(ftp, dir_path, script):
                    yield search_path
    except:
        pass

    ftp.quit()
