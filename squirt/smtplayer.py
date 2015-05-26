#! /usr/bin/python
""" Squirt SMTP layer

Copyright (C) 2014 - Paul Pritchard

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
from os.path import isabs, expanduser
import re
import smtplib
import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ", "

def smtp_send(script):
    """ Sends an email with whatever attachment was requested """

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = script.get('subject')
    outer['To'] = COMMASPACE.join([script.get('mailto')])
    outer['From'] = script.get('mailfrom')
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Message Body
    msg = MIMEText(script.get('body'), _subtype='plain')
    outer.attach(msg)

    # The attachments folder
    folder = script.get('folder')
    if folder == None:
        folder = os.getcwd()
    else:
        if not isabs(folder):
            folder = expanduser(folder)

    # The attachments
    if script.get('files') != None:
        try:
            pattern = re.compile(script.get('files'))
        except:
            return(False, 'Invalid file pattern')
    else:
        pattern = re.compile('')

    for filename in os.listdir(folder):
        if pattern.search(filename) != None or script.get('files') == None:
            path = os.path.join(folder, filename)
            if not os.path.isfile(path):
                continue
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed)
                # Use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(path) as file_path:
                    # Note: we should handle calculating the charset
                    msg = MIMEText(file_path.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(path, 'rb') as file_path:
                    msg = MIMEImage(file_path.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(path, 'rb') as file_path:
                    msg = MIMEAudio(file_path.read(), _subtype=subtype)
            else:
                with open(path, 'rb') as file_path:
                    msg = MIMEBase(maintype, subtype)
                    msg.set_payload(file_path.read())
                # Encode the payload using Base64
                encoders.encode_base64(msg)
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', \
                           filename=filename)
            outer.attach(msg)

            if script.get('delete')==True:
                os.remove(path)

    # And then send the message
    smtp_message = outer.as_string()

    server = smtplib.SMTP(script.get('server'), script.get('port'))
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(script.get('user'), script.get('password'))

    smtp_from = script.get('mailfrom')
    smtp_to = script.get('mailto')

    if script.get('test') == False:
        server.sendmail(smtp_from, smtp_to, smtp_message)
    server.close()

    return(True, 'Mail sent successfully')

