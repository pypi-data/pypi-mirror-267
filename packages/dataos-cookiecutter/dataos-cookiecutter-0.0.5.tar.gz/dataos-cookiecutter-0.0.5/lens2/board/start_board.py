import subprocess
import os
from lens2.utils import get_env_or_throw
from lens2.constants import LENS2_BOARD_PATH


def add_start_subparser(subparsers):
    subparsers.set_defaults(func=executes_start)


def executes_start(views):
    # Change directory to Rill directory
    view_name = views[0]
    view_board_path = os.path.join(get_env_or_throw(LENS2_BOARD_PATH), view_name)

    os.chdir(view_board_path)

    # Run 'board start --readonly' command
    start_command = "rill start --readonly"
    subprocess.run(start_command, shell=True)
