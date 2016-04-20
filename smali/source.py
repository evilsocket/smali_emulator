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
class Source(object):
    def __init__(self, filename):
        self.filename = filename
        self.lines    = list(open(filename, 'r'))

    def has_line(self,index):
        return True if 0 <= index < len(self.lines) else False

    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, index, line):
        self.lines[index] = line