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
from smtplayer import *
from squtils import replace_special

def fn_build_script(script):
    """ Build a new script or update an existing script """
    if db_script_exists(script.get('script')) == True:
        if db_retrieve_script_protocol(script.get('script')) != script.get('protocol'):
            return(False, 'Changing protocol is not allowed')

        return db_update_script(script)
    else:
        return db_write_script(replace_special(script))

def fn_copy_script(settings):
    """ Copy a script definition
        Any optional settings are applied to the new script """
    if db_script_exists(settings.get('cf')) == True:
        settings.update(script=settings.get('ct'))

        if settings.get('protocol') == None:
            settings.update(protocol=db_retrieve_script_protocol(settings.get('cf')))

        if settings.get('description') == None:
            settings.update(description=db_retrieve_script_description(settings.get('cf')))

        if settings.get('host') == None:
            settings.update(host=db_retrieve_script_host(settings.get('cf')))

        if settings.get('user') == None:
            settings.update(user=db_retrieve_script_user(settings.get('cf')))

        if settings.get('password') == None:
            settings.update(password=db_retrieve_script_password(settings.get('cf')))

        if settings.get('local') == None:
            settings.update(local=db_retrieve_script_local(settings.get('cf')))

        if settings.get('remote') == None:
            settings.update(remote=db_retrieve_script_remote(settings.get('cf')))

        if settings.get('do') == None:
            settings.update(do=db_retrieve_script_do(settings.get('cf')))

        if settings.get('files') == None:
            settings.update(files=db_retrieve_script_files(settings.get('cf')))

        if settings.get('mode') == None:
            settings.update(mode=db_retrieve_script_mode(settings.get('cf')))

        if settings.get('namefmt') == None:
            settings.update(namefmt=db_retrieve_script_namefmt(settings.get('cf')))

        if settings.get('server') == None:
            settings.update(server=db_retrieve_script_server(settings.get('cf')))

        if settings.get('port') == None:
            settings.update(port=db_retrieve_script_port(settings.get('cf')))

        if settings.get('mailfrom') == None:
            settings.update(mailfrom=db_retrieve_script_mailfrom(settings.get('cf')))

        if settings.get('mailto') == None:
            settings.update(mailto=db_retrieve_script_mailto(settings.get('cf')))

        if settings.get('subject') == None:
            settings.update(subject=db_retrieve_script_subject(settings.get('cf')))

        if settings.get('body') == None:
            settings.update(body=db_retrieve_script_body(settings.get('cf')))

        if settings.get('folder') == None:
            settings.update(folder=db_retrieve_script_folder(settings.get('cf')))

        if settings.get('delete') == None:
            settings.update(folder=db_retrieve_script_delete(settings.get('cf')))

        return db_write_script(replace_special(settings))[0]
    else:
        return False

def fn_delete_script(script):
    """ Deletes an existing script
        script is the script name (character) """
    if db_script_exists(script) == True:
        if db_delete_script(script)[0] == True:
            return True
        else:
            return False
    else:
        return False

def fn_execute_script(script):
    """ Retrieve script defaults and overrides and execute """
    if script.get('description') == None:
        script.update(description=db_retrieve_script_description(script.get('script')))
    if script.get('host') == None:
        script.update(host=db_retrieve_script_host(script.get('script')))
    if script.get('user') == None:
        script.update(user=db_retrieve_script_user(script.get('script')))
    if script.get('password') == None:
        script.update(password=db_retrieve_script_password(script.get('script')))
    if script.get('local') == None:
        script.update(local=db_retrieve_script_local(script.get('script')))
    if script.get('remote') == None:
        script.update(remote=db_retrieve_script_remote(script.get('script')))
    if script.get('do') == None:
        script.update(do=db_retrieve_script_do(script.get('script')))
    if script.get('files') == None:
        script.update(files=db_retrieve_script_files(script.get('script')))
    if script.get('mode') == None:
        script.update(mode=db_retrieve_script_mode(script.get('script')))
    if script.get('namefmt') == None:
        script.update(namefmt=db_retrieve_script_namefmt(script.get('script')))
    if script.get('server') == None:
        script.update(server=db_retrieve_script_server(script.get('script')))
    if script.get('port') == None:
        script.update(port=db_retrieve_script_port(script.get('script')))
    if script.get('mailfrom') == None:
        script.update(mailfrom=db_retrieve_script_mailfrom(script.get('script')))
    if script.get('mailto') == None:
        script.update(mailto=db_retrieve_script_mailto(script.get('script')))
    if script.get('subject') == None:
        script.update(subject=db_retrieve_script_subject(script.get('script')))
    if script.get('body') == None:
        script.update(body=db_retrieve_script_body(script.get('script')))
    if script.get('folder') == None:
        script.update(folder=db_retrieve_script_folder(script.get('script')))
    if script.get('delete')==None:
        script.update(delete=db_retrieve_script_delete(script.get('script')))

    if db_retrieve_script_protocol(script.get('script')) == 'FTP':
        if script.get('do').split('-')[0] == 'chmod':
            for found_file in ftp_chmod(script):
                yield found_file
        elif script.get('do') == 'del':
            for found_file in ftp_del(script):
                yield found_file
        elif script.get('do') == 'get':
            for found_file in ftp_get(None, script.get('local'), script.get('remote'), script):
                yield found_file
        elif script.get('do') == 'ls':
            for found_file in ftp_ls(script):
                yield found_file
        elif script.get('do') == 'put':
            for found_file in ftp_put(script):
                yield found_file
        elif script.get('do') == 'tree':
            for directory in ftp_tree(None, script.get('remote'), script):
                yield directory
        else:
            yield "Error: Unrecognised FTP command"
    elif db_retrieve_script_protocol(script.get('script')) == 'SMTP':
        yield smtp_send(script)
    else:
        yield 'Error: Unrecognised Protocol'


def fn_retrieve_script(script_name):
    """ Retrieves the settings for an existing script """
    script = dict(script=script_name)
    if db_script_exists(script_name) == False:
        script.update(exists=False)
    else:
        script.update(exists=True)
        script.update(protocol=db_retrieve_script_protocol(script_name))
        script.update(description=db_retrieve_script_description(script_name))
        if script.get('protocol') == 'FTP':
            script.update(host=db_retrieve_script_host(script_name))
            script.update(user=db_retrieve_script_user(script_name))
            script.update(password=db_retrieve_script_password(script_name))
            script.update(local=db_retrieve_script_local(script_name))
            script.update(remote=db_retrieve_script_remote(script_name))
            script.update(do=db_retrieve_script_do(script_name))
            script.update(files=db_retrieve_script_files(script_name))
            script.update(mode=db_retrieve_script_mode(script_name))
            script.update(namefmt=db_retrieve_script_namefmt(script_name))
            script.update(port=db_retrieve_script_port(script_name))
            script.update(delete=db_retrieve_script_delete(script_name))
        elif script.get('protocol') == 'SMTP':
            script.update(server=db_retrieve_script_server(script_name))
            script.update(port=db_retrieve_script_port(script_name))
            script.update(user=db_retrieve_script_user(script_name))
            script.update(password=db_retrieve_script_password(script_name))
            script.update(mailfrom=db_retrieve_script_mailfrom(script_name))
            script.update(mailto=db_retrieve_script_mailto(script_name))
            script.update(subject=db_retrieve_script_subject(script_name))
            script.update(body=db_retrieve_script_body(script_name))
            script.update(files=db_retrieve_script_files(script_name))
            script.update(folder=db_retrieve_script_folder(script_name))
            script.update(port=db_retrieve_script_port(script_name))
            script.update(delete=db_retrieve_script_delete(script_name))
    return script

def fn_list_scripts():
    """ Returns a list of currently defined scripts """
    script_list = []
    for script in db_list_scripts():
        script_list.append(script)
    return script_list
