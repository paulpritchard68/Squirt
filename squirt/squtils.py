#! /usr/bin/python
""" Generic utilities

Copyright (C) 2014 Paul Pritchard

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

def retrieve_local_path(relative_path):
    """ Finds the absolute local path for relative path names """
    if relative_path == None:
        return os.getcwd('')
    elif not isabs(relative_path):
        return expanduser(relative_path)
    else:
        return relative_path

def replace_special(script):
    """ Scans script dictionary for special options and replace accoringly """
    for skey in script:
        if script.get(skey)  == '*Null':
            script[skey] = None
    return script        
