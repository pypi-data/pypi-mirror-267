########################################################################################################################
# Copyright 2023 the authors (see AUTHORS file for full list).                                                         #
#                                                                                                                      #
# This file is part of shapelets.                                                                                      #
#                                                                                                                      #
# Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General       #
# Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)  #
# any later version.                                                                                                   #
#                                                                                                                      #
# Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied      #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see           #
# <https://www.gnu.org/licenses/>.                                                                                     #
########################################################################################################################

import os
from pathlib import Path
import platform
import sys 
import time

from . import _run

def _run_shapelets():
    r"""
    Main function that runs shapelets. This is only invoked via the entry point "shapelets CONFIG" where CONFIG is the name of the configuration plaintext file that exists in the same directory level as the working directory.  

    """
    # if user did not provide any configuration filename (which is required)
    if len(sys.argv) == 1: 
        raise RuntimeError('Please provide name of config file, i.e. "shapelets config".')

     # if user did provide a configuration filename/path
    elif len(sys.argv) == 2:
        config_file = sys.argv[1]
        working_dir = os.getcwd() 
        _run._run(config_file, working_dir)

    # if the user provides more than 1 argument (in addition to shapelets). Print error messages and quit.
    else: 
        raise RuntimeError('Please provide one argument (configuration filename), i.e.: "shapelets config".')


def _run_tests():
    r"""
    Main function that runs all the unit tests via unittest from Python STL. This is only invoked via the entry point "shapelets-test".
    
    """
    # notify user tests may take more than a few seconds
    print("Initiating shapelets unit tests. This will likely take a few minutes.")
    time.sleep(10)
    
    # navigate to tests/ folder relative to this file
    tests_dir = os.path.join(Path(__file__).parents[0], 'tests')
    os.chdir(tests_dir)

    # command line arguments based on user OS
    # automatically find all tests using unittest built-in discovery component
    if str(platform.system()) == 'Windows':
        os.system('python -B -m unittest -v')
    else:
        os.system('python3 -B -m unittest -v')               