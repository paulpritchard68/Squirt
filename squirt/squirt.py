#! /usr/bin/python
""" An FTP automation utility

squirt.py

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

import sys
import argparse
from funlayer import fn_build_script, fn_copy_script, fn_delete_script, \
                     fn_retrieve_script, fn_list_scripts, fn_execute_script, \
                     fn_export_script

def build_script(options):
    """ Build a reusable FTP script
        options is the dictionary of options that define the script """
    script = dict(script=options.script)
    script.update(protocol=options.protocol.upper())
    script.update(host=options.host)
    script.update(user=options.user)
    script.update(password=options.password)
    script.update(local=options.local)
    script.update(remote=options.remote)
    script.update(do=options.do)
    script.update(files=options.files)
    script.update(mode=options.mode)
    script.update(namefmt=options.namefmt)
    script.update(server=options.server)
    script.update(port=options.port)
    script.update(mailfrom=options.mailfrom)
    script.update(mailto=options.mailto)
    script.update(folder=options.folder)
    if options.delete != None:
        script.update(delete=options.delete=='yes')
    else:
        script.update(delete='0')
    if options.description != None:
        script.update(description=" ".join(options.description))
    if options.subject != None:
        script.update(subject=" ".join(options.subject))
    if options.body != None:
        script.update(body=" ".join(options.body))

    can_we_build_it = fn_build_script(script)
    print("%s: Script %s" % (can_we_build_it[1], script.get('script')))

def copy_script(settings):
    """ Copy an existing script
        options is the dictionary of options that define the script """
    script = dict(cf=settings.cf)
    script.update(ct=settings.ct)
    script.update(host=settings.host)
    script.update(user=settings.user)
    script.update(password=settings.password)
    script.update(local=settings.local)
    script.update(remote=settings.remote)
    script.update(do=settings.do)
    script.update(files=settings.files)
    script.update(mode=settings.mode)
    script.update(namefmt=settings.namefmt)
    script.update(server=settings.server)
    script.update(port=settings.port)
    script.update(mailfrom=settings.mailfrom)
    script.update(mailto=settings.mailto)
    script.update(folder=settings.folder)
    if script.options != None:
        script.update(delete=settings.delete=='yes')
    if settings.description != None:
        script.update(description=" ".join(settings.description))
    if settings.subject != None:
        script.update(subject=" ".join(settings.subject))
    if settings.body != None:
        script.update(body=" ".join(settings.body))

    if fn_copy_script(script) == True:
        print("Script %s successfully copied to %s" \
            % (script.get('cf'), script.get('ct')))
    else:
        print("Copy of script %s to %s failed. Check your settings" \
            % (script.get('cf'), script.get('ct')))

def delete_script(options):
    """ Delete an existing script """
    if fn_delete_script(options.script) == True:
        print("Script %s deleted" % options.script)
    else:
        print("Error: Script %s not deleted" % options.script)

def display_script(options):
    """ Displays a script
        options is a dictionay that contains one value - the script name """
    script = fn_retrieve_script(options.script)
    if script.get('exists') == False:
        print("Script %s not defined" % script.get('script'))
    else:
        print("Script:        %s " % script.get('script'))
        print("Description:   %s " % script.get('description'))
        print("Protocol:      %s " % script.get('protocol'))
        if script.get('protocol') == 'FTP':
            print("Host:          %s " % script.get('host'))
            print("Port:          %s " % script.get('port'))
            print("User:          %s " % script.get('user'))
            if options.showpass == 'yes':
                print("Password:      %s " % script.get('password'))
            if  script.get('namefmt') != None:
                print("Naming format: %s " % script.get('namefmt'))
            print("Local folder:  %s " % script.get('local'))
            print("Remote folder: %s " % script.get('remote'))
            print("Action:        %s " % script.get('do'))
            print("Files:         %s " % script.get('files'))
            if script.get('mode') != None:
                print("Mode:          %s " % script.get('mode'))
            if script.get('delete') is True:
                delete_files = 'Yes'
            else:
                delete_files = 'No'
            print("Delete files:  %s " % delete_files)
        elif script.get('protocol') == 'SMTP':
            print("Server:        %s " % script.get('server'))
            print("Port:          %s " % script.get('port'))
            print("User:          %s " % script.get('user'))
            if options.showpass == 'yes':
                print("Password:      %s " % script.get('password'))
            print("Mail from:     %s " % script.get('mailfrom'))
            print("Mail to:       %s " % script.get('mailto'))
            print("Subject:       %s " % script.get('subject'))
            print("Body:          %s " % script.get('body'))
            print("Files:         %s " % script.get('files'))
            print("Folder:        %s " % script.get('folder'))
            if script.get('delete') is True:
                delete_files = 'Yes'
            else:
                delete_files = 'No'
            print("Delete files:  %s " % delete_files)

def list_scripts():
    """ Lists the currently defined set of scripts
        No paramerters this time """
    for script in  fn_list_scripts():
        if script[1] != None:
            print(script[0], '/', script[1])
        else:
            print(script[0])

def execute_script(options):
    """ Execute a built script
        options provides a dictionary of optional overrides that
        can be applied to the script """
    script = dict(script=options.script)
    script.update(host=options.host)
    script.update(user=options.user)
    script.update(password=options.password)
    script.update(local=options.local)
    script.update(remote=options.remote)
    script.update(do=options.do)
    script.update(files=options.files)
    script.update(mode=options.mode)
    script.update(namefmt=options.namefmt)
    script.update(server=options.server)
    script.update(port=options.port)
    script.update(mailfrom=options.mailfrom)
    script.update(mailto=options.mailto)
    script.update(folder=options.folder)
    script.update(test=options.test)
    if options.delete != None:
        script.update(delete=options.delete=='yes')
    if options.subject != None:
        script.update(subject=" ".join(options.subject))
    if options.body != None:
        script.update(body=" ".join(options.body))

    for filename in fn_execute_script(script):
        print(filename)

def export_script(options):
    """ Export a script """
    if fn_export_script(options.script) == True:
        print("Script %s exported" % options.script)
    else:
        print("Error: Script %s not exported" % options.script)

def main():
    """ The main event
        Parses the entered arguments and figures out what to do with them """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Commands')

    # The build command
    build_parser = subparsers.add_parser('build', help='Build script')
    build_parser.add_argument('protocol', action='store', \
                                choices=['FTP', 'SMTP'], \
                                help='Protocol')
    build_parser.add_argument('script', action='store', help='Script name')
    build_parser.add_argument('--description', nargs='*', action='store', \
                                help='Description')
    build_parser.add_argument('--host', action='store', help='FTP Host name')
    build_parser.add_argument('--user', action='store', help='User ID')
    build_parser.add_argument('--password', action='store', help='Password')
    build_parser.add_argument('--local', action='store', help='FTP local path')
    build_parser.add_argument('--remote', action='store', \
                                help='FTP remote path')
    build_parser.add_argument('--do', action='store', help='FTP Do action')
    build_parser.add_argument('--files', action='store', \
                                help='The files to be acted on')
    build_parser.add_argument('--mode', action='store', \
                                help='Transfer mode (ascii or binary). \
                                      This option is not currently supported')
    build_parser.add_argument('--namefmt', action='store', \
                                help='File naming format (0 or 1). \
                                You will need this when accessing an IBM i \
                                on Power.')
    build_parser.add_argument('--server', action='store', \
                                help='SMTP mail server')
    build_parser.add_argument('--port', action='store', help='FTP/SMTP server port.')
    build_parser.add_argument('--mailfrom', action='store', \
                                help='SMTP from email address')
    build_parser.add_argument('--mailto', action='store', \
                                help='SMTP to email address')
    build_parser.add_argument('--subject', nargs='*', action='store', \
                                help='SMTP email subject')
    build_parser.add_argument('--body', nargs='*', action='store', \
                                help='SMTP email message body')
    build_parser.add_argument('--folder', action='store', \
                                help='SMTP: local folder for attachments')
    build_parser.add_argument('--delete', action='store', \
                                choices=['yes', 'no'], \
                                help='Delete files after sending (not yet implemented')
    build_parser.set_defaults(command='build')

    # The copy command
    copy_parser = subparsers.add_parser('copy', help='Copy script')
    copy_parser.add_argument('cf', action='store', help='Copy from script')
    copy_parser.add_argument('ct', action='store', help='Copy to script')
    copy_parser.add_argument('--description', nargs='*', action='store', help='Description')
    copy_parser.add_argument('--host', action='store', help='FTP Host name')
    copy_parser.add_argument('--user', action='store', help='User ID')
    copy_parser.add_argument('--password', action='store', help='Password')
    copy_parser.add_argument('--local', action='store', help='FTP local path')
    copy_parser.add_argument('--remote', action='store', help='FTP remote path')
    copy_parser.add_argument('--do', action='store', help='FTP action')
    copy_parser.add_argument('--files', action='store', \
                                help='The files to be acted on')
    copy_parser.add_argument('--mode', action='store', \
                                help='Transfer mode (ascii or binary). \
                                This option is not currently supported')
    copy_parser.add_argument('--namefmt', action='store', \
                                help='File naming format (0 or 1). \
                                You will need this when accessing an IBM i \
                                on Power.')
    copy_parser.add_argument('--server', action='store', \
                                help='SMTP mail server')
    copy_parser.add_argument('--port', action='store', help='SMTP server port')
    copy_parser.add_argument('--mailfrom', action='store', \
                                help='SMTP from email address')
    copy_parser.add_argument('--mailto', action='store', \
                                help='SMTP to email address')
    copy_parser.add_argument('--subject', nargs='*', action='store', \
                                help='SMTP email subject')
    copy_parser.add_argument('--body', nargs='*', action='store', \
                                help='SMTP email message body')
    copy_parser.add_argument('--folder', action='store', \
                                help='SMTP: local folder for attachments')
    copy_parser.add_argument('--delete', action='store', \
                                choices=['yes', 'no'], \
                                help='Delete files after sending (partially implemented')
    copy_parser.set_defaults(command='copy')

    # The delete command
    delete_parser = subparsers.add_parser('delete', help='Delete script')
    delete_parser.add_argument('script', action='store', help='Script name')
    delete_parser.set_defaults(command='delete')

    # The display command
    display_parser = subparsers.add_parser('display', help='Display script')
    display_parser.add_argument('script', action='store', help='Script name')
    display_parser.add_argument('--showpass', action='store', \
                                help='Show password (yes/no)')
    display_parser.set_defaults(command='display')

    # The list command
    list_parser = subparsers.add_parser('list', \
                                        help='List currently defined scripts')
    list_parser.set_defaults(command='list')

    # The exec command
    exec_parser = subparsers.add_parser('exec', help='Execute script')
    exec_parser.add_argument('script', action='store', help='Script name')
    exec_parser.add_argument('--host', action='store', help='Host name')
    exec_parser.add_argument('--user', action='store', help='User ID')
    exec_parser.add_argument('--password', action='store', help='Password')
    exec_parser.add_argument('--local', action='store', help='Set local path')
    exec_parser.add_argument('--remote', action='store', help='Set remote path')
    exec_parser.add_argument('--do', action='store', help='Do action')
    exec_parser.add_argument('--files', action='store', \
                                help='The files to be acted on')
    exec_parser.add_argument('--mode', action='store', \
                                choices=['ascii', 'binary'], \
                                help='Transfer mode (ascii or binary). \
                                This option is not currently supported')
    exec_parser.add_argument('--namefmt', action='store', \
                                help='File naming format (0 or 1). \
                                You will need this when accessing an IBM i \
                                on Power.')
    exec_parser.add_argument('--server', action='store', \
                                help='SMTP mail server')
    exec_parser.add_argument('--port', action='store', help='SMTP server port')
    exec_parser.add_argument('--mailfrom', action='store', \
                                help='SMTP from email address')
    exec_parser.add_argument('--mailto', action='store', \
                                help='SMTP to email address')
    exec_parser.add_argument('--subject', nargs='*', action='store', \
                                help='SMTP email subject')
    exec_parser.add_argument('--body', nargs='*', action='store', \
                                help='SMTP email message body')
    exec_parser.add_argument('--folder', action='store', \
                                help='SMTP: local folder for attachments')
    exec_parser.add_argument('--test', action='store_const', const=True, \
                                default=False, help='Run in test mode')
    exec_parser.add_argument('--delete', action='store', \
                                choices=['yes', 'no'], \
                                help='Delete files after sending (partially implemented')
    exec_parser.set_defaults(command='exec')

    # The export command
    export_parser = subparsers.add_parser('export', help='Export script')
    export_parser.add_argument('script', action='store', help='Script name')
    export_parser.set_defaults(command='export')

    try:
        command_line = parser.parse_args()
    except:
        sys.exit(2)

    if command_line.command == 'build':
        build_script(command_line)
    elif command_line.command == 'copy':
        copy_script(command_line)
    elif command_line.command == 'delete':
        delete_script(command_line)
    elif command_line.command == 'display':
        display_script(command_line)
    elif command_line.command == 'list':
        list_scripts()
    elif command_line.command == 'exec':
        execute_script(command_line)
    elif command_line.command == 'export':
        export_script(command_line)
    else:
        print("Command not recognised. Try using --help")
        sys.exit(2)

if __name__ == "__main__":
    main()
