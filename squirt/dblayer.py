#! /usr/bin/python
""" Squirt database functions

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

import sqlite3
import os

DB_PATH = '~/.squirt.db'

def db_delete_script(script):
    """ Delete an existing script
        Parameter script is the script name (character) """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('delete from squirt_ftp \
                    where script_id in \
                        (select script_id from squirt_scripts \
                        where script = ? )', parameters)
    cursor.execute('delete from squirt_smtp \
                    where script_id in \
                        (select script_id from squirt_scripts \
                        where script = ? )', parameters)
    cursor.execute('delete from squirt_scripts where script = ?', parameters)

    connection.commit()
    connection.close()

    return (True, 'Script deleted')

def db_script_exists(script):
    """ Returns True if the named script exists, else False """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select count(*) from squirt_scripts \
                   where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        if row[0] == 0:
            return False
        else:
            return True

def db_list_scripts():
    """ Lists all of the currently defined scripts """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    cursor.execute('select script_id, script, description \
                    from squirt_scripts order by script')

    rows = cursor.fetchall()
    for row in rows:
        yield row[0], row[1], row[2]

def db_list_scripts_by_host(host):
    """ Lists all of the currently defined scripts for a selected host """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (str.upper(host), str.upper(host))
    cursor.execute('select a.script_id, a.script, a.protocol \
                    from squirt_scripts a \
                    left outer join squirt_ftp b on b.script_id = a.script_id and upper(b.host) = ? \
                    left outer join squirt_smtp c on c.script_id = a.script_id and upper(c.server) = ? \
                    where b.script_id is not null or c.script_id is not null', parameters)

    rows = cursor.fetchall()
    for row in rows:
        yield row[0], row[1], row[2]

def db_retrieve_script_protocol(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select protocol from squirt_scripts \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_host(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select host \
                    from squirt_ftp f \
                    join squirt_scripts s \
                        on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_user(script):
    """ Retrieves a script value """

    # First check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select user \
                        from squirt_ftp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)
    elif protocol == 'SMTP':
        cursor.execute('select user \
                        from squirt_smtp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)
    else:
        return 'Error: Unknown protocol'

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_password(script):
    """ Retrieves a script value """

    # Check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select pass \
                        from squirt_ftp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)
    if protocol == 'SMTP':
        cursor.execute('select pass \
                        from squirt_smtp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_local(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select local \
                    from squirt_ftp f \
                    join squirt_scripts s \
                        on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_remote(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select remote \
                    from squirt_ftp f \
                    join squirt_scripts s \
                        on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_do(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select do \
                    from squirt_ftp f \
                    join squirt_scripts s \
                        on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_files(script):
    """ Retrieves a script value """

    # First check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select files \
                        from squirt_ftp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)
    elif protocol == 'SMTP':
        cursor.execute('select files \
                        from squirt_smtp f \
                        join squirt_scripts s \
                            on f.script_id = s.script_id \
                        where script = ?', parameters)
    else:
        return 'Error: Unknown protocol'

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_mode(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mode \
                    from squirt_ftp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_namefmt(script):
    """ Retrieves a script value """

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select namefmt \
                    from squirt_ftp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_server(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select server \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_port(script):
    """ Retrieves a script value """

    # Check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select port \
                        from squirt_ftp f \
                        join squirt_scripts s on f.script_id = s.script_id \
                        where script = ?', parameters)
    if protocol == 'SMTP':
        cursor.execute('select port \
                        from squirt_smtp f \
                        join squirt_scripts s on f.script_id = s.script_id \
                        where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_delete(script):
    """ Retrieves a script value """

    # Check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select delete_files \
                        from squirt_ftp f \
                        join squirt_scripts s on f.script_id = s.script_id \
                        where script = ?', parameters)
    if protocol == 'SMTP':
        cursor.execute('select delete_files \
                        from squirt_smtp f \
                        join squirt_scripts s on f.script_id = s.script_id \
                        where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]==1

def db_retrieve_script_mailfrom(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mailfrom \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_mailto(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mailto \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_subject(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select subject \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_body(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select body \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_folder(script):
    """ Retrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select folder \
                    from squirt_smtp f \
                    join squirt_scripts s on f.script_id = s.script_id \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_description(script):
    """ Retrieves the description for a script """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select description \
                    from squirt_scripts \
                    where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_write_script(options):
    """ Write a new script definition to database """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    protocol = options.get('protocol')
    parameters = (options.get('script'), protocol, options.get('description'))
    cursor.execute('insert into squirt_scripts (script, protocol, description) \
                    values(?, ?, ?)', parameters)
    script_id = cursor.lastrowid

    if protocol == 'FTP':
        delete_flag = options.get('delete')
        parameters = (script_id, options.get('host'), options.get('user'), \
                      options.get('password'), options.get('local'), \
                      options.get('remote'), options.get('do'), \
                      options.get('files'), options.get('mode'), \
                      options.get('namefmt'), options.get('port'), \
                      delete_flag);
        cursor.execute('insert into squirt_ftp \
                        (script_id, host, user, pass, local, remote, do, files, mode, namefmt, port, delete_files) \
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', parameters)
    elif protocol == 'SMTP':
        delete_flag = options.get('delete')
        parameters = (script_id, options.get('server'), options.get('port'), \
                      options.get('user'), options.get('password'), \
                      options.get('mailfrom'), options.get('mailto'), \
                      options.get('subject'), options.get('body'), \
                      options.get('files'), options.get('folder'), \
                      delete_flag);
        cursor.execute('insert into squirt_smtp \
                        (script_id, server, port, user, pass, mailfrom, mailto, subject, body, files, folder, delete_files) \
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', parameters)
    else:
        return (False, 'Invalid protocol')

    connection.commit()
    connection.close()

    return (True, 'Script built')

def db_update_script_description(options, cursor):
    """ Update an existing script description """
    if options.get('description') != None:
        setnull = options.get('description') == '*Null'
        parameters = (setnull, options.get('description'), options.get('script'))
        cursor.execute('update squirt_scripts \
                        set description = \
                        case when ? = 1 then null else ? end \
                        where script = ?' \
                        , parameters)

def db_update_ftp_host(options, cursor):
    """ Update an existing script definition: FTP Host """
    if options.get('host') != None:
        setnull = options.get('host') == '*Null'
        parameters = (setnull, options.get('host'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set host = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_user(options, cursor):
    """ Update an existing script definition: FTP User """
    if options.get('user') != None:
        setnull = options.get('user') == '*Null'
        parameters = (setnull, options.get('user'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set user = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_password(options, cursor):
    """ Update an existing script definition: FTP Password """
    if options.get('password') != None:
        setnull = options.get('password') == '*Null'
        parameters = (setnull, options.get('password'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set pass = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_local(options, cursor):
    """ Update an existing script definition: FTP Local Path """
    if options.get('local') != None:
        setnull = options.get('local') == '*Null'
        parameters = (setnull, options.get('local'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set local = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_remote(options, cursor):
    """ Update an existing script definition: FTP Remote Path """
    if options.get('remote') != None:
        setnull = options.get('remote') == '*Null'
        parameters = (setnull, options.get('remote'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set remote = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_do(options, cursor):
    """ Update an existing script definition: FTP action """
    if options.get('do') != None:
        setnull = options.get('do') == '*Null'
        parameters = (setnull, options.get('do'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set do = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_files(options, cursor):
    """ Update an existing script definition: FTP files """
    if options.get('files') != None:
        setnull = options.get('files') == '*Null'
        parameters = (setnull, options.get('files'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set files = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_mode(options, cursor):
    """ Update an existing script definition: FTP mode """
    if options.get('mode') != None:
        setnull = options.get('mode') == '*Null'
        parameters = (setnull, options.get('mode'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set mode = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_namefmt(options, cursor):
    """ Update an existing script definition: FTP namefmt for i """
    if options.get('namefmt') != None:
        setnull = options.get('namefmt') == '*Null'
        parameters = (setnull, options.get('namefmt'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set namefmt = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_port(options, cursor):
    """ Update an existing script definition: FTP port """
    if options.get('port') != None:
        setnull = options.get('port') == '*Null'
        parameters = (setnull, options.get('port'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set port = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_ftp_delete(options, cursor):
    """ Update an existing script definition: FTP delete flag """
    if options.get('delete') != None:
        parameters = (options.get('delete'), options.get('script'))
        cursor.execute('update squirt_ftp \
                        set delete_files = ? \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_server(options, cursor):
    """ Update an existing script definition: SMTP Server """
    if options.get('server') != None:
        setnull = options.get('server') == '*Null'
        parameters = (setnull, options.get('server'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set server = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_port(options, cursor):
    """ Update an existing script definition: SMTP Port """
    if options.get('port') != None:
        setnull = options.get('port') == '*Null'
        parameters = (setnull, options.get('port'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set port = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_user(options, cursor):
    """ Update an existing script definition: SMTP User """
    if options.get('user') != None:
        setnull = options.get('user') == '*Null'
        parameters = (setnull, options.get('user'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set user = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_password(options, cursor):
    """ Update an existing script definition: SMTP Password """
    if options.get('password') != None:
        setnull = options.get('password') == '*Null'
        parameters = (setnull, options.get('password'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set pass = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_mailfrom(options, cursor):
    """ Update an existing script definition: SMTP From address """
    if options.get('mailfrom') != None:
        setnull = options.get('mailfrom') == '*Null'
        parameters = (setnull, options.get('mailfrom'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set mailfrom = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_mailto(options, cursor):
    """ Update an existing script definition: SMTP To address """
    if options.get('mailto') != None:
        setnull = options.get('mailto') == '*Null'
        parameters = (setnull, options.get('mailto'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set mailto = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_subject(options, cursor):
    """ Update an existing script definition: SMTP Subject """
    if options.get('subject') != None:
        setnull = options.get('subject') == '*Null'
        parameters = (setnull, options.get('subject'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set subject = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_body(options, cursor):
    """ Update an existing script definition: SMTP Body """
    if options.get('body') != None:
        setnull = options.get('body') == '*Null'
        parameters = (setnull, options.get('body'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set body = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_files(options, cursor):
    """ Update an existing script definition: SMTP Files to send """
    if options.get('files') != None:
        setnull = options.get('files') == '*Null'
        parameters = (setnull, options.get('files'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set files = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_folder(options, cursor):
    """ Update an existing script definition: SMTP Folder """
    if options.get('folder') != None:
        setnull = options.get('folder') == '*Null'
        parameters = (setnull, options.get('folder'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set folder = \
                        case when ? = 1 then null else ? end \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_smtp_delete(options, cursor):
    """ Update an existing script definition: SMTP delete flag """
    if options.get('delete') != None:
        parameters = (options.get('delete'), options.get('script'))
        cursor.execute('update squirt_smtp \
                        set delete_files = ? \
                        where script_id in \
                            (select script_id \
                             from squirt_scripts where script = ?)' \
                        , parameters)

def db_update_script(options):
    """ Update an existing script definition """
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = connection.cursor()

    # Establish the protocol
    parameters = (options.get('script'))
    cursor.execute('select protocol \
                    from squirt_scripts \
                    where script = ?', (parameters, ))
    rows = cursor.fetchall()
    for row in rows:
        protocol = row[0]
        break
    if options.get('protocol') != None and options.get('protocol') != protocol:
        return False  # Mismatched protocol

    # Update the description
    db_update_script_description(options, cursor)

    if protocol == 'FTP':
        db_update_ftp_host(options, cursor)
        db_update_ftp_user(options, cursor)
        db_update_ftp_password(options, cursor)
        db_update_ftp_local(options, cursor)
        db_update_ftp_remote(options, cursor)
        db_update_ftp_do(options, cursor)
        db_update_ftp_files(options, cursor)
        db_update_ftp_namefmt(options, cursor)
        db_update_ftp_port(options, cursor)
        db_update_ftp_delete(options, cursor)
    elif protocol == 'SMTP':
        db_update_smtp_server(options, cursor)
        db_update_smtp_port(options, cursor)
        db_update_smtp_user(options, cursor)
        db_update_smtp_password(options, cursor)
        db_update_smtp_mailfrom(options, cursor)
        db_update_smtp_mailto(options, cursor)
        db_update_smtp_subject(options, cursor)
        db_update_smtp_body(options, cursor)
        db_update_smtp_files(options, cursor)
        db_update_smtp_folder(options, cursor)
        db_update_smtp_delete(options, cursor)
    else:
        return (False, 'Invalid protocol')

    connection.commit()
    connection.close()

    return (True, 'Script updated')

def db_init():
    """ Checks if the database exists and returns the current level
        If the database is not found, create it """

    # Connect
    connection = sqlite3.connect(os.path.expanduser(DB_PATH))

    # First check whether the database exists and find its version
    database_version = 0
    cursor = connection.cursor()
    cursor.execute('select name \
                    from sqlite_master \
                    where name = \'squirt_config\' and type = \'table\' ')
    table_rows = cursor.fetchall()
    for table_rows in table_rows:
        cursor.execute('select current_version from squirt_config')
        rows = cursor.fetchall()
        for row in rows:
            database_version = row[0]
            break
        break

    # If no database exists, create it
    if database_version == 0:

        # Create the config table
        cursor.execute('create table squirt_config \
                        (ID integer primary key, current_version integer)')
        cursor.execute('insert into squirt_config(current_version) values(1)')

        # Create the squirt scripts table
        cursor.execute('create table squirt_scripts \
                       (ID integer primary key, script TEXT, host TEXT, \
                       user TEXT, pass TEXT, local TEXT, remote TEXT, \
                       do TEXT, files TEXT)')

        database_version = 1

    # A small update to version 1
    if database_version == 1:

        cursor.execute('alter table squirt_scripts \
                        add column protocol TEXT default \'FTP\' ')
        cursor.execute('update squirt_config set current_version = 2')

        database_version = 2

    # A major update to version 2
    if database_version == 2:

        # First, the FTP detail
        cursor.execute('create table squirt_ftp \
                       (ftp_ID integer primary key, script_id integer, \
                       host text, user text, pass text, local text, \
                       remote text, do text, files text)')

        cursor.execute('insert into squirt_ftp \
                       (script_id, host, user, pass, local, remote, do, files) \
                       select id, host, user, pass, local, remote, do, files \
                       from squirt_scripts where protocol = \'FTP\' ')

        # Then drop the crap out of the script header
        # Slightly clunky approach due to the lack of ALTER TABLE support
        # in SQLite
        cursor.execute('create table squirt_scripts_new \
                       (script_id integer primary key, script text, \
                       protocol text)')

        cursor.execute('insert into squirt_scripts_new select ID, script, \
                        protocol from squirt_scripts')

        cursor.execute('drop table squirt_scripts')

        cursor.execute('create table squirt_scripts \
                       (script_id integer primary key, script text, \
                       protocol text)')

        cursor.execute('insert into squirt_scripts \
                        select * from squirt_scripts_new')

        cursor.execute('drop table squirt_scripts_new')

        # And then we need an SMTP detail table
        cursor.execute('create table squirt_smtp \
                       (smtp_id integer primary key, script_id integer, \
                       server text, port integer, user text, pass text, \
                       mailfrom text, mailto text, subject text, body text)')

        # And finally, the version change
        cursor.execute('update squirt_config set current_version = 3')

        database_version = 3

    # Files! There's no point if the SMTP doesn't send any files.
    if database_version == 3:
        cursor.execute('alter table squirt_smtp add column files TEXT')
        cursor.execute('update squirt_config set current_version = 4')
        database_version = 4

    # And folders. You forgot to include the folders, Gromit!
    if database_version == 4:
        cursor.execute('alter table squirt_smtp add column folder TEXT')
        cursor.execute('update squirt_config set current_version = 5')
        database_version = 5

    # Two more FTP options
    if database_version == 5:
        cursor.execute('alter table squirt_ftp add column mode TEXT')
        cursor.execute('alter table squirt_ftp add column namefmt integer')
        cursor.execute('update squirt_config set current_version = 6')
        database_version = 6

    # Yet another FTP option: PORT
    if database_version == 6:
        cursor.execute('alter table squirt_ftp add column port INTEGER')
        cursor.execute('update squirt_config set current_version = 7')
        database_version = 7

    # More functionality: DELETE.
    # If this option is set to yes, files will be deleted once sent/received
    if database_version == 7:
        cursor.execute('alter table squirt_ftp \
                        add column delete_files integer not null default 0 check(delete_files in (0, 1))')
        cursor.execute('alter table squirt_smtp \
                        add column delete_files integer not null default 0 check(delete_files in (0, 1))')
        cursor.execute('update squirt_config set current_version = 8')
        database_version = 8

    # Add a description column to the database
    if database_version == 8:
        cursor.execute('alter table squirt_scripts \
                        add column description text')
        cursor.execute('update squirt_config set current_version = 9')
        database_version = 9

    connection.commit()
    connection.close()

    return True
