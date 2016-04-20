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
from smali.opcodes import *
from smali.vm import VM
from smali.source import Source

import sys
import time

# Holds some statistics.
class Stats(object):
    def __init__(self, vm):
        self.opcodes = len(vm.opcodes)
        self.preproc = 0
        self.execution = 0
        self.steps = 0

    def __repr__(self):
        s  = "opcode handlers    : %d\n" % self.opcodes
        s += "preprocessing time : %d ms\n" % self.preproc
        s += "execution time     : %d ms\n" % self.execution
        s += "execution steps    : %d\n" % self.steps
        return s

# The main emulator class.
class Emulator(object):
    def __init__(self):
        # Instance of the virtual machine.
        self.vm      = None
        # Instance of the source file.
        self.source  = None
        # Instance of the statistics object.
        self.stats   = None
        # Opcodes handlers.
        self.opcodes = []

        # Dynamically load opcode handlers.
        # TODO: Implement missing opcodes.
        for entry in dir( sys.modules['smali.opcodes'] ):
            if entry.startswith('op_'):
                self.opcodes.append( globals()[entry]() )

    @staticmethod
    def __catch_expression(block_id):
        """
        Helper method to create a regular expression to parse a '.catch' directives for a given block.
        :param block_id: The block number found in the :try_start_BLOCK_ID label.
        :return: A regular expression.
        """
        return '^\.catch [^\s]+ \{:try_start_%s[ \.]+:try_end_%s\}\s*(\:.+)' % (block_id,block_id )

    def __preprocess_trycatch_block(self, index, line):
        """
        Will search the '.catch' directive and update the VM accordingly.
        :param index: The index of the line to start the research from.
        :param line: The line where the :try_start_BLOCK_ID label was found.
        """
        # get block identifier
        block_id = line.split('_')[2]
        # search for next pattern:
        #
        #   .catch Ljava/lang/Exception; {:try_start_BLOCK_ID .. :try_end_BLOCK_ID} :LABEL
        #
        for nindex, nline in enumerate(self.source.lines[index + 1:]):
            # TODO: Save exception type for specific catch.
            m = re.search( self.__catch_expression(block_id), nline )
            if m:
                label = m.group(1)
                eindex = nindex + index + 1
                self.vm.catch_blocks.append((index, eindex, label))
                break

    def __preprocess(self):
        """
        Start the preprocessing phase which will save all the labels and their line index
        for fast lookups while jumping and will pre parse all the try/catch directives.
        """
        self.source.lines = map( str.strip, self.source.lines )
        current_packed_switch = None
        for index, line in enumerate(self.source.lines):
            # label marker?
            if line != '' and line[0] == ':':
                # check for try/catch blocks
                if line.startswith( ':try_start_' ):
                    self.__preprocess_trycatch_block(index,line)

                # we already considered this ... hopefully :P
                elif line.startswith( ':try_end_' ):
                    pass

                elif line.startswith( ':pswitch_data' ):
                    self.vm.packed_switches[line] = {"first_value": 0, "cases": []}
                    current_packed_switch = line
                elif line.startswith( ':pswitch_' ) and current_packed_switch is not None:
                    self.vm.packed_switches[current_packed_switch]["cases"].append(line)

                else:
                    self.vm.labels[line] = index

            if line != '' and line[0] == '.':
                if line.startswith(".packed-switch "):
                    first_value = int(line.split(' ')[1], 16)
                    switch = self.vm.packed_switches[current_packed_switch]
                    switch["first_value"] = first_value
                elif line == '.end packed-switch':
                    current_packed_switch = None

    def __parse_line(self, line):
        # Search for appropriate parser.
        for parser in self.opcodes:
            if parser.parse(line, self.vm):
                return True

        return False

    @staticmethod
    def __should_skip_line(line):
        """
        Helper method used to determine if a line must be skipped/ignored.
        :param line: The line to check.
        :return: True if the line can be ignored, otherwise False.
        """
        return line == "" or line[0] == '#' or line[0] == ':' or line[0] == '.'

    def fatal(self, message):
        """
        Display an error message, the current line being executed and quit.
        :param message: The error message to display.
        """
        print
        print "-------------------------"
        print "Fatal error on line %03d:\n" % self.vm.pc

        print "  %03d %s" % (self.vm.pc, self.source[self.vm.pc - 1])

        print "\n%s" % message
        quit()

    def run(self, filename, args = {}):
        """
        Load a smali file and start emulating it.
        :param filename: The path of the file to load and emulate.
        :param args: A dictionary of optional initialization variables for the VM, mostly used for arguments.
        :return: The return value of the emulated method or None if no return-* opcode was executed.
        """
        self.source = Source(filename)
        self.vm     = VM(self)
        self.stats  = Stats(self)

        self.vm.variables.update(args)

        s = time.time() * 1000
        # Preprocess labels and try/catch blocks for fast lookup.
        self.__preprocess()
        e = time.time() * 1000
        self.stats.preproc = e - s

        s = time.time() * 1000
        # Loop each line and emulate.
        while self.vm.stop is False and self.source.has_line(self.vm.pc):
            self.stats.steps += 1
            line = self.source[self.vm.pc]
            self.vm.pc += 1

            if self.__should_skip_line(line):
                continue

            elif self.__parse_line(line) is False:
                self.fatal( "Unsupported opcode." )

        e = time.time() * 1000
        self.stats.execution = e - s

        return self.vm.return_v

