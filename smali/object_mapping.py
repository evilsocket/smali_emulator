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
from smali.objects.string import String
from smali.objects.string_builder import StringBuilder

# This class holds the mapping of Java objects and methods to their Python respective.
class ObjectMapping(object):
    def __init__(self):
        self.mapping = {
            String.name(): String.methods(),
            StringBuilder.name(): StringBuilder.methods()
        }

    @staticmethod
    def __demangle_class_name(vm, name):
        """
        Demangle a class name.
        :param vm: Instance of the VM.
        :param name: The name of the class to be demangled.
        :return: The demangled class name.
        """
        if name[0] != 'L':
            vm.emu.fatal("'%s' does not name a class." % name)
        return name[1:].replace('/', '.').replace(';', '')

    def new_instance(self, vm, klass):
        """
        Used by the new-instance opcode.
        :param vm: Instance of the VM.
        :param klass: Mangled class name to instanciate.
        :return: The new class instance.
        """
        class_name = self.__demangle_class_name( vm, klass )

        if class_name in self.mapping:
            if 'new-instance' in self.mapping[class_name]:
                return self.mapping[class_name]['new-instance']()

            else:
                vm.emu.fatal("Unsupported method 'new-instance' for class '%s'." % class_name)
        else:
            vm.emu.fatal("Unsupported class '%s'." % class_name)

    def invoke(self, vm, this, klass, method_name, args):
        """
        Invoke a method ( if mapped ).
        :param vm: Instance of the VM.
        :param this: Identifier of the class instance.
        :param klass: Mangled class name.
        :param method_name: Mangled method name to invoke.
        :param args: Arguments of the method.
        """
        class_name = self.__demangle_class_name( vm, klass )
        if class_name in self.mapping:
            if method_name in self.mapping[class_name]:
                invokeResult = self.mapping[class_name][method_name]( vm, this, args )
                if not invokeResult is None:
                    vm.return_v = invokeResult

            else:
                vm.emu.fatal("Unsupported method '%s' for class '%s'." % ( method_name, class_name ))
        else:
            vm.emu.fatal("Unsupported class '%s'." % class_name)
