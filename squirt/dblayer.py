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

db_path = '~/.squirt.db'

def db_delete_script(script):
    """ Delete an existng script
        Parameter script is the script name (character) """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('delete from squirt_ftp where script_id in (select script_id from squirt_scripts where script = ? )', parameters)
    cursor.execute('delete from squirt_smtp where script_id in (select script_id from squirt_scripts where script = ? )', parameters)
    cursor.execute('delete from squirt_scripts where script = ?', parameters)

    connection.commit()
    connection.close()

    return True

def db_script_exists(script):
    """ Returns True if the named script exists, else False """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select count(*) from squirt_scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        if row[0] == 0:
            return False
        else:
            return True

def db_list_scripts():
    """ Lists all of the currently defined scripts """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    cursor.execute('select script from squirt_scripts order by script')

    rows = cursor.fetchall()
    for row in rows:
        yield row[0]

def db_retrieve_script_protocol(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select protocol from squirt_scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]


def db_retrieve_script_host(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select host from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_user(script):
    """ Retrieves a script value """

    # First check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select user from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)
    elif protocol == 'SMTP':
        cursor.execute('select user from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)
    else:
        return 'Error: Unknown protocol'

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_password(script):
    """ Retrieves a script value """

    # First check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select pass from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)
    if protocol == 'SMTP':
        cursor.execute('select pass from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_local(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select local from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_remote(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select remote from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_do(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select do from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_files(script):
    """ Retrieves a script value """

    # First check the protocol
    protocol = db_retrieve_script_protocol(script)

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    if protocol == 'FTP':
        cursor.execute('select files from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)
    elif protocol == 'SMTP':
        cursor.execute('select files from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)
    else:
        return 'Error: Unknown protocol'

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_mode(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mode from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_namefmt(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select namefmt from squirt_ftp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_server(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select server from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_port(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select port from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_mailfrom(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mailfrom from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_mailto(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select mailto from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_subject(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select subject from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_body(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select body from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_folder(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select folder from squirt_smtp f join squirt_scripts s on f.script_id = s.script_id where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_write_script(options):
    """ Write a new script definition to database """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    protocol = options.get('protocol')
    parameters = (options.get('script'), protocol)
    cursor.execute('insert into squirt_scripts (script, protocol) \
                    values(?, ?)', parameters)
    script_id = cursor.lastrowid

    if protocol == 'FTP':
        parameters = (script_id, options.get('host'), options.get('user'), \
                      options.get('password'), options.get('local'), \
                      options.get('remote'), options.get('do'), \
                      options.get('files'), options.get('mode'), \
                      options.get('namefmt'))
        cursor.execute('insert into squirt_ftp \
                        (script_id, host, user, pass, local, remote, do, files, mode, namefmt) \
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', parameters)
    elif protocol == 'SMTP':
        parameters = (script_id, options.get('server'), options.get('port'), \
                      options.get('user'), options.get('password'), \
                      options.get('mailfrom'), options.get('mailto'), \
                      options.get('subject'), options.get('body'), \
                      options.get('files'), options.get('folder'))
        cursor.execute('insert into squirt_smtp \
                        (script_id, server, port, user, pass, mailfrom, mailto, subject, body, files, folder) \
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', parameters)
    else:
        return False

    connection.commit()
    connection.close()

    return True

def db_update_script(options):
    """ Update an existing script definition """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
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

    if protocol == 'FTP':

        if options.get('host') != None:
            parameters = (options.get('host'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set host = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('user') != None:
            parameters = (options.get('user'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set user = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('password') != None:
            parameters = (options.get('password'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set pass = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('local') != None:
            parameters = (options.get('local'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set local = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('remote') != None:
            parameters = (options.get('remote'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set remote = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('do') != None:
            parameters = (options.get('do'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set do = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('files') != None:
            parameters = (options.get('files'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set files = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('mode') != None:
            parameters = (options.get('mode'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set mode = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

        if options.get('namefmt') != None:
            parameters = (options.get('namefmt'), options.get('script'))
            cursor.execute('update squirt_ftp \
                            set namefmt = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
    elif protocol == 'SMTP':
        if options.get('server') != None:
            parameters = (options.get('server'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set server = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('port') != None:
            parameters = (options.get('port'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set port = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('user') != None:
            parameters = (options.get('user'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set user = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('password') != None:
            parameters = (options.get('password'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set pass = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('mailfrom') != None:
            parameters = (options.get('mailfrom'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set mailfrom = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('mailto') != None:
            parameters = (options.get('mailto'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set mailto = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('subject') != None:
            parameters = (options.get('subject'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set subject = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('body') != None:
            parameters = (options.get('body'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set body = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('files') != None:
            parameters = (options.get('files'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set files = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)
        if options.get('folder') != None:
            parameters = (options.get('folder'), options.get('script'))
            cursor.execute('update squirt_smtp \
                            set folder = ? \
                            where script_id in \
                                (select script_id \
                                 from squirt_scripts where script = ?)' \
                            , parameters)

    connection.commit()
    connection.close()

    return True

def db_init():
    """ Checks if the database exists and returns the current level
        If the database is not found, create it """

    # Connect
    connection = sqlite3.connect(os.path.expanduser(db_path))

    # First check whether the database exists and find its version
    database_version = 0
    cursor = connection.cursor()
    cursor.execute('select name from sqlite_master where name = \'squirt_config\' and type = \'table\' ')
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
        cursor.execute('create table squirt_config(ID integer primary key, current_version integer)')
        cursor.execute('insert into squirt_config(current_version) values(1)')

        # Create the squirt scripts table
        cursor.execute('create table squirt_scripts(ID integer primary key, script TEXT, host TEXT, user TEXT, pass TEXT, local TEXT, remote TEXT, do TEXT, files TEXT)')

        database_version = 1

    # A small update to version 1
    if database_version == 1:

        cursor.execute('alter table squirt_scripts add column protocol TEXT default \'FTP\' ')
        cursor.execute('update squirt_config set current_version = 2')

        database_version = 2

    # A major update to version 2
    if database_version == 2:

        # First, the FTP detail
        cursor.execute('create table squirt_ftp (ftp_ID integer primary key, script_id integer, host text, user text, pass text, local text, remote text, do text, files text)')

        cursor.execute('insert into squirt_ftp (script_id, host, user, pass, local, remote, do, files) select id, host, user, pass, local, remote, do, files from squirt_scripts where protocol = \'FTP\' ')

        # Then drop the crap out of the script header
        # Slightly clunky approach due to the lack of ALTER TABLE support in SQLite
        cursor.execute('create table squirt_scripts_new (script_id integer primary key, script text, protocol text)')

        cursor.execute('insert into squirt_scripts_new select ID, script, protocol from squirt_scripts')

        cursor.execute('drop table squirt_scripts')

        cursor.execute('create table squirt_scripts (script_id integer primary key, script text, protocol text)')

        cursor.execute('insert into squirt_scripts select * from squirt_scripts_new')

        cursor.execute('drop table squirt_scripts_new')

        # And then we need an SMTP detail table
        cursor.execute('create table squirt_smtp (smtp_id integer primary key, script_id integer, server text, port integer, user text, pass text, mailfrom text, mailto text, subject text, body text)')

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

    connection.commit()
    connection.close()

    return True
