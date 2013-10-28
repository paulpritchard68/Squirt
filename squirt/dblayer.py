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

def db_retrieve_script_host(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select host from squirt_scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_user(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select user from squirt_scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_pass(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select pass from squirt_scripts where script = ?', parameters)

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
    cursor.execute('select local from squirt_scripts where script = ?', parameters)

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
    cursor.execute('select remote from squirt_scripts where script = ?', parameters)

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
    cursor.execute('select do from squirt_scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_files(script):
    """ Retrieves a script value """

    # First check the database is current
    db_init()

    # Then the function
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select files from squirt_scripts where script = ?', parameters)

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
        
    parameters = (options.get('script'), options.get('host'), options.get('user'), options.get('password'), options.get('local'), options.get('remote'), options.get('do'), options.get('files'))
    cursor.execute('insert into squirt_scripts (script, host, user, pass, local, remote, do, files) \
                   values(?, ?, ?, ?, ?, ?, ?, ?)', parameters)

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

    if options.get('host') != None:
        parameters = (options.get('host'), options.get('script'))
        cursor.execute('update squirt_scripts set host = ? where script = ?', parameters)
    
    if options.get('user') != None:
        parameters = (options.get('user'), options.get('script'))
        cursor.execute('update squirt_scripts set user = ? where script = ?', parameters)

    if options.get('password') != None:
        parameters = (options.get('password'), options.get('script'))
        cursor.execute('update squirt_scripts set pass = ? where script = ?', parameters)
       
    if options.get('local') != None:
        parameters = (options.get('local'), options.get('script'))
        cursor.execute('update squirt_scripts set local = ? where script = ?', parameters)

    if options.get('remote') != None:
        parameters = (options.get('remote'), options.get('script'))
        cursor.execute('update squirt_scripts set remote = ? where script = ?', parameters)

    if options.get('do') != None:
        parameters = (options.get('do'), options.get('script'))
        cursor.execute('update squirt_scripts set do = ? where script = ?', parameters)

    if options.get('files') != None:
        parameters = (options.get('files'), options.get('script'))
        cursor.execute('update squirt_scripts set files = ? where script = ?', parameters)

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
    cursor.execute('select name from sqlite_master where name = \'squirt_config\' and type = \'table\' ');
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

    # Update as necessary
    if database_version == 1:

        cursor.execute('alter table squirt_scripts add column protocol TEXT default \'FTP\' ')
        cursor.execute('update squirt_config set current_version = 2')

        database_version = 2

    connection.commit()
    connection.close()

    return True
