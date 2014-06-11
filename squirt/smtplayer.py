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

def smtp_send(script):
    """ Sends an email with whatever attachment was requested """
    COMMASPACE = ", "

    server = smtplib.SMTP(script.get('server'), script.get('port'))
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(script.get('user'), script.get('password'))
    
    smtp_from = script.get('mailfrom')
    smtp_to = [script.get('mailto')]
    smtp_message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (smtp_from, COMMASPACE.join(smtp_to), script.get('subject'), script.get('body'))

    server.sendmail(smtp_from, smtp_to, smtp_message)
    server.close()
    return(True, 'Mail sent successfully')
    
