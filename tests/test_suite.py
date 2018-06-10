# -*- coding: utf-8 -*-
# This file is part of the Smali Emulator.
#
# Copyright(c) 2016-2018 Simone 'evilsocket' Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# Copyright(c) 2018- David Kremer, courrier@david-kremer.fr
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

import os, fnmatch

import pytest

from smali.emulator import Emulator


def data_files():
    files = []
    datapath = os.path.join(os.path.dirname(__file__), 'data')
    for root, dirnames, filenames in os.walk(datapath):
        for filename in fnmatch.filter(filenames, '*.smali'):
            input_data = open(os.path.join(root, filename), 'r').readlines()
            expected_result = input_data[0].lstrip('#').strip()
            smali_source = input_data[1:]
            files.append((filename, expected_result, smali_source))

    return files


def run_source(source_code):
    emu = Emulator()
    ret = emu.run_source(source_code)
    out = emu.vm.variables.copy()
    out.update({'ret': ret})
    return str(out)


@pytest.mark.parametrize(
    'filename, expected_result, input_source',
    data_files()
)
def test_all_files(filename, expected_result, input_source):
    assert filename.endswith('.smali')
    assert expected_result == run_source(input_source)

