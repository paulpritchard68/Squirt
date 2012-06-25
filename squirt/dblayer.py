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
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('delete from scripts where script = ?', parameters)

    connection.commit()
    connection.close()

    return True

def db_script_exists(script):
    """ Returns True if the named script exists, else False """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select count(*) from scripts where script = ?', parameters)
    
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == 0:
            return False
        else:
            return True

def db_list_scripts():
    """ Lists all of the currently defined scripts """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    cursor.execute('select script from scripts order by script')
    
    rows = cursor.fetchall()
    for row in rows:
        yield row[0]

def db_retrieve_script_host(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select host from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_user(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select user from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_pass(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select pass from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_local(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select local from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_remote(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select remote from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_do(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select do from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_retrieve_script_files(script):
    """ Rertrieves a script value """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    parameters = (script, )
    cursor.execute('select files from scripts where script = ?', parameters)

    rows = cursor.fetchall()
    for row in rows:
        return row[0]

def db_write_script(options):
    """ Write a new script definition to database """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()
        
    parameters = (options.get('script'), options.get('host'), options.get('user'), options.get('password'), options.get('local'), options.get('remote'), options.get('do'), options.get('files'))
    cursor.execute('insert into scripts (script, host, user, pass, local, remote, do, files) \
                   values(?, ?, ?, ?, ?, ?, ?, ?)', parameters)

    connection.commit()
    connection.close()

    return True

def db_update_script(options):
    """ Update an existing script definition """
    connection = sqlite3.connect(os.path.expanduser(db_path))
    cursor = connection.cursor()

    if options.get('host') != None:
        parameters = (options.get('host'), options.get('script'))
        cursor.execute('update scripts set host = ? where script = ?', parameters)
    
    if options.get('user') != None:
        parameters = (options.get('user'), options.get('script'))
        cursor.execute('update scripts set user = ? where script = ?', parameters)

    if options.get('password') != None:
        parameters = (options.get('password'), options.get('script'))
        cursor.execute('update scripts set pass = ? where script = ?', parameters)
       
    if options.get('local') != None:
        parameters = (options.get('local'), options.get('script'))
        cursor.execute('update scripts set local = ? where script = ?', parameters)

    if options.get('remote') != None:
        parameters = (options.get('remote'), options.get('script'))
        cursor.execute('update scripts set remote = ? where script = ?', parameters)

    if options.get('do') != None:
        parameters = (options.get('do'), options.get('script'))
        cursor.execute('update scripts set do = ? where script = ?', parameters)

    if options.get('files') != None:
        parameters = (options.get('files'), options.get('script'))
        cursor.execute('update scripts set files = ? where script = ?', parameters)

    connection.commit()
    connection.close()

    return True

def db_init():
    """ Checks if the database exists and returns the current level
        If the database is not found, create it """
    
    # Connect
    try:
        connection = sqlite3.connect(os.path.expanduser(db_path))
    except:
        return False

    # Check version or create database
    try:
        cursor = connection.cursor()
        cursor.execute('select current_version from config')
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == 1: #Cureenet DB level
                return True
    except:
        with connection:
            cursor = connection.cursor()

            # Create the config table
            cursor.execute('create table config(ID integer primary key, current_version integer)')
            cursor.execute('insert into config(current_version) values(1)')

            # Create the squirt scripts table
            cursor.execute('create table scripts(ID integer primary key, script TEXT, host TEXT, user TEXT, pass TEXT, local TEXT, remote TEXT, do TEXT, files TEXT)') 

        return True
