#! /usr/bin/python
""" Squirt XML layer

Copyright (C) 2017 - Paul Pritchard

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

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def xml_export(script):
    """ Export settings as XML """
    root = Element('data')

    script_name = script.get('script')
    script_element = SubElement(root, 'script', attrib={'Name': script_name})

    description = script.get('description')
    if description != None:
        description_element = SubElement(script_element, 'description')
        description_element.text = description

    protocol = script.get('protocol')
    protocol_element = SubElement(script_element, 'protocol')
    protocol_element.text = protocol

    host = script.get('host')
    if host != None:
        host_element = SubElement(script_element, 'host')
        host_element.text = host

    user = script.get('user')
    if user != None:
        user_element = SubElement(script_element, 'user')
        user_element.text = user

    password = script.get('password')
    if password != None:
        password_element = SubElement(script_element, 'password')
        password_element.text = password

    local = script.get('local')
    if local != None:
        local_element = SubElement(script_element, 'local')
        local_element.text = local

    remote = script.get('remote')
    if remote != None:
        remote_element = SubElement(script_element, 'remote')
        remote_element.text = remote

    action = script.get('do')
    if action != None:
        action_element = SubElement(script_element, 'action')
        action_element.text = action

    files = script.get('files')
    if files != None:
        files_element = SubElement(script_element, 'files')
        files_element.text = files

    mode = script.get('mode')
    if mode != None:
        mode_element = SubElement(script_element, 'mode')
        mode_element.text = mode

    namefmt = script.get('namefmt')
    if namefmt != None:
        namefmt_element = SubElement(script_element, 'namefmt')
        namefmt_element.text = str(namefmt)

    port = script.get('port')
    if port != None:
        port_element = SubElement(script_element, 'port')
        port_element.text = str(port)

    delete = script.get('delete')
    if delete != None:
        delete_element = SubElement(script_element, 'delete')
        if delete_element is True:
            delete_element.text = 'Yes'
        else:
            delete_element.text = 'No'

    server = script.get('server')
    if server != None:
        server_element = SubElement(script_element, 'server')
        server_element.text = server

    mailfrom = script.get('mailfrom')
    if mailfrom != None:
        mailfrom_element = SubElement(script_element, 'mailfrom')
        mailfrom_element.text = mailfrom

    mailto = script.get('mailto')
    if mailto != None:
        mailto_element = SubElement(script_element, 'mailto')
        mailto_element.text = mailto

    subject = script.get('subject')
    if subject != None:
        subject_element = SubElement(script_element, 'subject')
        subject_element.text = subject

    body = script.get('body')
    if body != None:
        body_element = SubElement(script_element, 'body')
        body_element.text = body

    folder = script.get('folder')
    if folder != None:
        folder_element = SubElement(script_element, 'folder')
        folder_element.text = folder

    file_name = "%s.xml" % script_name
    with open(file_name, 'w') as xml_file:
        xml_file.write(xml_prettify(root))

def xml_prettify(element):
    """ Prettfy the XML elements """
    raw_string = tostring(element, 'utf-8')
    pretty_string = minidom.parseString(raw_string)
    return pretty_string.toprettyxml(indent="    ")
