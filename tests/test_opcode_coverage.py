import pytest
import os

from smali.parser import get_op_code

def build_op_code_data():
    return {
        hexcode: definition for hexcode, definition in enumerate(
            open(os.path.join(
                os.path.dirname(__file__), 'data', 'opcode_list.dat'
            )).readlines()
        )
    }

@pytest.mark.parametrize(
    'opcode_value, opcode_source_line',
    build_op_code_data().items(),
)
def test_op_code_building(opcode_value, opcode_source_line):
    assert opcode_source_line.startswith(get_op_code(opcode_source_line))