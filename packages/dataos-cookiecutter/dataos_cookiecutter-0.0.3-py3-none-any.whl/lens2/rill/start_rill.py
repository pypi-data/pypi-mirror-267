import re
import subprocess
import os
from lens2.utils import get_env_or_throw
from lens2.constants import LENS2_RILL_PATH


def add_start_subparser(subparsers):
    subparsers.set_defaults(func=executes_start)


def executes_start():
    # Change directory to Rill directory
    os.chdir(get_env_or_throw(LENS2_RILL_PATH))  # Change this to the actual path where Rill is installed

    # Run 'rill start --readonly' command
    start_command = "rill start --readonly"
    subprocess.run(start_command, shell=True)
