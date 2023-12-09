# call this script like:
#   python -m tests.mock_board boards/nullbitsco/tidbit

import sys

from .mocks import init_board_module_mocks


init_board_module_mocks()

board_dir = sys.argv[1]
sys.path.insert(0, board_dir)

# TODO pass tests for dactyl keebs which seem to map a mystery pin B7
if 'dactyl' in board_dir:
    from kmk.quickpin.pro_micro.avr_promicro import translate as avr

    avr['B7'] = -1

if __name__ == '__main__':
    import main

    assert main
