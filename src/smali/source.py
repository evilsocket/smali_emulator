# -*- coding: utf-8 -*-
# This file is part of the Smali Emulator.
#
# Copyright(c) 2016 Simone 'evilsocket' Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# Class to hold the source file data.


class MissingSource(Exception):
    pass

def get_source_from_file(filename):
    with open(filename, 'r') as fd:
        source_code = Source(lines=fd.readlines())
    return source_code


class Source(object):
    def __init__(self, lines=None):
        if not lines:
            raise MissingSource("Missing Source Code.")

        self.lines = lines[:]

    def has_line(self, index):
        return 0 <= index < len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, index, line):
        self.lines[index] = line
