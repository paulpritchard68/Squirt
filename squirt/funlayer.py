#! /usr/bin/python
""" Squirt functional layer

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

from dblayer import *
from ftplayer import *

def fn_build_script(script):
    """ Build a new script or update an existing script """
    if db_script_exists(script.get('script')) == True:
        if db_update_script(script) == True:
            return 'updated'
        else:
            return 'Fail'
    else:
        if db_write_script(script) == True:
            return 'built'
        else:
            return 'Fail'

def fn_copy_script(settings):
    """ Copy a script definition
        Any optional settings are applied to the new script """
    if db_script_exists(settings.get('cf')) == True:
        settings.update(script = settings.get('ct'))

        if settings.get('host') == None:
            settings.update(host = db_retrieve_script_host(settings.get('cf')))
    
        if settings.get('user') == None:
            settings.update(user = db_retrieve_script_user(settings.get('cf')))

        if settings.get('password') == None:
            settings.update(password = db_retrieve_script_pass(settings.get('cf')))

        if settings.get('local') == None:
            settings.update(local = db_retrieve_script_local(settings.get('cf')))

        if settings.get('remote') == None:
            settings.update(remote = db_retrieve_script_remote(settings.get('cf')))

        if settings.get('do') == None:
            settings.update(do = db_retrieve_script_do(settings.get('cf')))

        if settings.get('files') == None:
            settings.update(files = db_retrieve_script_files(settings.get('cf')))

        return db_write_script(settings)
    else:
        return False

def fn_delete_script(script):
    """ Deletes an existing script
        script is the script name (character) """
    if db_script_exists(script) == True:
        if db_delete_script(script) == True:
            return True
        else:
            return False
    else:
        return False

def fn_execute_script(script):
    """ Retrieve script defaults and overrides and execute """
    if script.get('host') == None:
        script.update(host=db_retrieve_script_host(script.get('script')))
    if script.get('user') == None:
        script.update(user=db_retrieve_script_user(script.get('script')))
    if script.get('password') == None:
        script.update(password=db_retrieve_script_pass(script.get('script')))
    if script.get('local') == None:
        script.update(local=db_retrieve_script_local(script.get('script')))
    if script.get('remote') == None:
        script.update(remote=db_retrieve_script_remote(script.get('script')))
    if script.get('do') == None:
        script.update(do=db_retrieve_script_do(script.get('script')))
    if script.get('files') == None:
        script.update(files=db_retrieve_script_files(script.get('script')))

    result = dict(script=script.get('script'))
    file_list = []
    if script.get('do') == 'del':
        result.update(action='Files deleted')
        for found_file in ftp_del(script):
            file_list.append(found_file)
        result.update(files=file_list)
        result.update(status=True)
    if script.get('do') == 'get':
        result.update(action='Files retrieved')
        for found_file in ftp_get(script):
            file_list.append(found_file)
        result.update(files=file_list)
        result.update(status=True)
    if script.get('do') == 'ls':
        result.update(action='Files found')
        for found_file in ftp_ls(script):
            file_list.append(found_file)
        result.update(files=file_list)
        result.update(status=True)
    
    return result


def fn_retrieve_script(script_name):
    """ Retrieves the settings for an existing script """
    script = dict(script=script_name)
    if db_script_exists(script_name) == False:
        script.update(exists=False)
    else:
        script.update(exists=True)
        script.update(host=db_retrieve_script_host(script_name))
        script.update(user=db_retrieve_script_user(script_name))
        script.update(password=db_retrieve_script_pass(script_name))
        script.update(local=db_retrieve_script_local(script_name))
        script.update(remote=db_retrieve_script_remote(script_name))
        script.update(do=db_retrieve_script_do(script_name))
        script.update(files=db_retrieve_script_files(script_name))
    return script

def fn_list_scripts():
    """ Returns a list of currently defined scripts """
    script_list = []
    for script in db_list_scripts():
        script_list.append(script)
    return script_list

def fn_initialise():
    """ Initialise the database """
    return db_init()
