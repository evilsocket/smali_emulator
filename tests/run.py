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
import sys, os, fnmatch, time, traceback
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from smali.emulator import Emulator



def get_data_files(file_filter):
    files = []
    datapath = os.path.join( os.path.dirname(__file__), 'data' )

    for root, dirnames, filenames in os.walk(datapath):
        for filename in fnmatch.filter(filenames, '*.smali'):
            if file_filter is None or file_filter in filename:
                files.append( os.path.join( root, filename ) )

    return files

def run_data_file(datafile):
    emu = Emulator()
    ret = emu.run(datafile)
    out = emu.vm.variables.copy()
    out.update({'ret': ret})
    return str(out)

def get_desired_output(datafile):
    return open(datafile).read().split("\n")[0][1:].strip()

def ppassed():
    print "\x1b[32mPASSED\x1b[0m"

def pfail(test,out):
    print "\x1b[31mFAILED\x1b[0m\n"
    print "  Expected : %s" % test
    print "  Got      : %s" % out
    print

def pexception(e):
    print "\x1b[31mFAILED\x1b[0m\n"
    print traceback.format_exc()

file_filter = sys.argv[1] if len(sys.argv) == 2 else None
files = get_data_files(file_filter)
total = len(files)
passed = 0
failed = 0
exceptions = 0
start = time.time() * 1000
just = len(max(files, key=len))

for datafile in files:
    sys.stdout.write( "Testing %s : " % datafile.ljust(just) )

    try:
        out = run_data_file(datafile)
        test = get_desired_output(datafile)

        if out == test:
            ppassed()
            passed += 1
        else:
            pfail( test, out )
            failed += 1

    except Exception as e:
        pexception(e)
        exceptions += 1

elapsed = ( time.time() * 1000 ) - start

print
print "Total Tests : %d" % total
print "Passed      : %d" % passed
print "Failed      : %d ( %d exceptions )" % ( failed, exceptions )
print "Total Time  : %f ms" % elapsed
print "Average     : %f ms / test" % ( elapsed / float(total) )