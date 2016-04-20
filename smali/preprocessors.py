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
import re
from smali.opcodes import OpCode

# Preprocess try/catch blocks.
class TryCatchPreprocessor:
    @staticmethod
    def check(line):
        return line.startswith( ':try_start_' )

    @staticmethod
    def process(vm, line, index, lines ):
        """
        Will search the '.catch' directive and update the VM accordingly.
        """
        # get block identifier
        block_id = line.split('_')[2]
        # search for next pattern:
        #
        #   .catch Ljava/lang/Exception; {:try_start_BLOCK_ID .. :try_end_BLOCK_ID} :LABEL
        #
        expression = '^\.catch [^\s]+ \{:try_start_%s[ \.]+:try_end_%s\}\s*(\:.+)' % (block_id,block_id )
        for nindex, nline in enumerate(lines[index + 1:]):
            # TODO: Save exception type for specific catch.
            m = re.search( expression, nline)
            if m:
                label = m.group(1)
                eindex = nindex + index + 1
                vm.catch_blocks.append((index, eindex, label))
                break

# Preprocess packed-switch blocks.
class PackedSwitchPreprocessor:
    @staticmethod
    def check(line):
        return line.startswith( ':pswitch_data' )

    @staticmethod
    def process(vm, name, index, lines):
        pswitch   = {"first_value": 0, "cases": []}
        next_line = index

        for nindex, nline in enumerate(lines[index + 1:]):
            if nline.startswith(".packed-switch "):
                pswitch["first_value"] = OpCode.get_int_value(nline.split(' ')[1])

            elif nline.startswith(':pswitch_'):
                pswitch["cases"].append(nline)

            elif nline == '.end packed-switch':
                next_line = index + nindex + 1
                break

            else:
                vm.fatal("Unexpected line '%s' while preprocessing packed-switch." % nline)

        vm.packed_switches[name] = pswitch

        # keep preprocessing from the end of this block
        return next_line