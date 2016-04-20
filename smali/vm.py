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
from smali.object_mapping import ObjectMapping

# The virtual machine used by the emulator.
class VM(object):
    def __init__(self, emulator):
        # we need the emulator instance in order to call its 'fatal' method.
        self.emu = emulator
        # holds the java->python objects and methods mapping
        self.mapping = ObjectMapping()
        # map of jump labels to opcodes offsets
        self.labels = {}
        # variables container
        self.variables = {}
        # try/catch blocks container with opcodes offsets
        self.catch_blocks = []
        # packed switches containers
        self.packed_switches = {}
        # list of thrown exceptions
        self.exceptions = []
        # holds the result of the last method invocation
        self.result = None
        # holds the return value of the method ( used by return-* opcodes )
        self.return_v = None
        # set to true when a return-* opcode is executed
        self.stop = False
        # current opcode index
        self.pc = 0

    def __getitem__(self, name):
        return self.variables[name]

    def __setitem__(self, name, value):
        self.variables[name] = value

    def fatal(self, message):
        self.emu.fatal(message)

    def goto(self, label):
        self.pc = self.labels[label]

    def exception(self, e):
        self.exceptions.append(e)

        # check if this operation is surrounded by a try/catch block
        for block in self.catch_blocks:
            start, end, label = block
            if start <= self.pc <= end:
                self.goto(label)
                return

        # nope, report unhandled exception
        self.emu.fatal("Unhandled exception '%s'." % str(e) )

    def new_instance(self, klass):
        return self.mapping.new_instance(self, klass)

    def invoke(self, this, class_name, method_name, args):
        self.mapping.invoke( self, this, class_name, method_name, args )



