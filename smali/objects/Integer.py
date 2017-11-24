# -*- coding: utf-8 -*-
# This file is contribution to the Smali Emulator.
#
# by @hugo_glez
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

class Integer:
    @staticmethod
    def name():
        return 'java.lang.Integer'

    @staticmethod
    def methods():
        return {
            'new-instance': Integer.new_instance,
            'parseInt(Ljava/lang/String;I)I' : Integer.parseInt,
        }

    
    @staticmethod
    def new_instance():
        return ""

    @staticmethod
    def parseInt(vm,this,args):
        vm.return_v = int(vm[this])

