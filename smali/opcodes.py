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

# Base class for all Dalvik opcodes ( see http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html ).
class OpCode(object):
    def __init__(self, expression):
        self.expression = re.compile(expression)

    @staticmethod
    def get_int_value(val):
        if "0x" in val:
            return int( val, 16 )
        else:
            return int( val )

    def parse(self, line, vm):
        m = self.expression.search(line)
        if m is None:
            return False

        # print "%03d %s" % ( vm.pc, line )

        try:
            self.eval(vm, *m.groups())
        except Exception as e:
            vm.exception(e)

        return True

class op_Const(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^const/\d+ (.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, lit):
        vm[vx] = OpCode.get_int_value(lit)

class op_ConstString(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^const-string (.+),\s*"([^"]*)"')

    @staticmethod
    def eval(vm, vx, s):
        vm[vx] = s.decode('unicode_escape')

class op_Move(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^move(-object)? (.+),\s*(.+)')

    @staticmethod
    def eval(vm, _, vx, vy):
        vm[vx] = vm[vy]

class op_MoveResult(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^move-result(-object)? (.+)')

    @staticmethod
    def eval(vm, _, dest):
        vm[dest] = vm.return_v

class op_MoveException(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^move-exception (.+)')

    @staticmethod
    def eval(vm, vx):
        vm[vx] = vm.exceptions.pop()

class op_IfLe(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-le (.+),\s*(.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, vy, label):
        if vm[vx] <= vm[vy]:
            vm.goto(label)

class op_IfGe(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-ge (.+),\s*(.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, vy, label):
        if vm[vx] >= vm[vy]:
            vm.goto(label)

class op_IfGt(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-gt (.+),\s*(.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, vy, label):
        if vm[vx] > vm[vy]:
            vm.goto(label)

class op_IfLez(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-lez (.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, label):
        if vm[vx] <= 0:
            vm.goto(label)

class op_IfEqz(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-eqz (.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, label):
        if vm[vx] == 0:
            vm.goto(label)

class op_IfNez(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^if-nez (.+),\s*(\:.+)')

    @staticmethod
    def eval(vm, vx, label):
        if vm[vx] != 0:
            vm.goto(label)

class op_ArrayLength(OpCode):
    def __init__(self):
        OpCode.__init__(self, 'array-length (.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy):
        vm[vx] = len(vm[vy])

class op_Aget(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^aget[\-a-z]* (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, vz):
        arr     = vm[vy]
        idx     = vm[vz]
        vm[vx] = arr[idx]

class op_AddIntLit(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^add-int/lit\d+ (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, lit):
        vm[vx] = eval( "%s + %s" % ( vm[vy], lit ) )

class op_MulIntLit(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^mul-int/lit\d+ (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, lit):
        vm[vx] = eval("%s * %s" % (vm[vy], lit))

class op_XorInt2Addr(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^xor-int(/2addr)? (.+),\s*(.+)')

    @staticmethod
    def eval(vm, _, vx, vy):
        # test if vm[vy] is a char instead of an int
        if isinstance(vm[vy], int):
            vm[vx] ^= int(vm[vy])
        else:
            vm[vx] ^= ord(vm[vy])

class op_DivInt(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^div-int (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, vz):
        vm[vx] = vm[vy] / vm[vz]

class op_SubInt(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^sub-int (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, vz):
        vm[vx] = vm[vy] - vm[vz]

class op_GoTo(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^goto(/\d+)? (:.+)')

    @staticmethod
    def eval(vm, _, label):
        vm.goto(label)

class op_NewInstance(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^new-instance (.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, klass):
        vm[vx] = vm.new_instance(klass)

class op_NewArray(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^new-array (.+),\s*(.+),\s*\[(.+)')

    @staticmethod
    def eval(vm, vx, vy, klass):
        vm[vx] = []

class op_APut(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^aput-(?:object|char) (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, vz):
        idx = int(vm[vz])
        arr = vm[vy]
        val = vm[vx]
        if len(arr) > idx:
            arr[idx] = val
        elif idx == len(arr):
            arr.append(val)
        vm[vy] = arr

class op_Invoke(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^invoke-([a-z]+) \{(.+)\},\s*(.+)')

    @staticmethod
    def eval(vm, _, args, call):
        args = map(str.strip, args.split(','))
        this = args[0]
        args = args[1:]
        klass, method  = call.split(';->')

        vm.invoke(this, klass, method, args)

class op_IntToType(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^int-to-([a-z]+) (.+),\s*(.+)')

    @staticmethod
    def eval(vm, ctype, vx, vy):
        if ctype == 'char':
            vm[vx] = chr( vm[vy] & 0xFF )

        else:
            vm.emu.fatal( "Unsupported type '%s'." % ctype )

class op_Return(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^return(-[a-z]+)?\s*(.+)')

    @staticmethod
    def eval(vm, ctype, vx):
        if ctype in ( '', '-wide', '-object' ):
            vm.return_v = vm[vx]
            vm.stop = True

        elif ctype == '-void':
            vm.return_v = None
            vm.stop = True

        else:
            vm.fatal( "Unsupported return type." )

class op_RemInt(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^rem-int/lit\d+ (.+),\s*(.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, vy, lit):
        vm[vx] = int(vm[vy]) % OpCode.get_int_value(lit)

class op_PackedSwitch(OpCode):
    def __init__(self):
        OpCode.__init__(self, '^packed-switch (.+),\s*(.+)')

    @staticmethod
    def eval(vm, vx, table):
        val = vm[vx]
        cases = vm.packed_switches.get(table, [])
        if val >= len(cases):
            return

        case_label = cases[val]
        vm.goto(case_label)
