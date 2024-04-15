import os
import shutil

import pkg_resources


def create_project_structure(args):
    # Extract folder names from command line arguments
    lens_name = args.name
    lens_dir = args.dir_name
    source_type = args.source_type
    parent_dir = args.parent_dir if args.parent_dir else os.getcwd()

    # Create main directory
    main_dir = os.path.join(parent_dir, lens_dir)

    # Check if the directory already exists
    if os.path.exists(main_dir):
        overwrite = input(
            f"The directory '{main_dir}' already exists. Do you want to overwrite it? (Y/n): ").strip().lower() or 'n'
        if overwrite != 'y':
            print("Aborted.")
            return

        # Remove the existing directory and its contents
        try:
            shutil.rmtree(main_dir)
        except OSError as e:
            print(f"Error removing existing directory '{main_dir}': {e}")
            return

    try:
        os.makedirs(main_dir)
    except OSError as e:
        print(f"Error creating main directory '{main_dir}': {e}")
        return

    # Create model directory
    model_dir = os.path.join(main_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    # Create subdirectories within model directory
    subdirectories = ['sqls', 'tables', 'views']
    for subdir in subdirectories:
        temp_path = os.path.join(model_dir, subdir)
        os.makedirs(temp_path, exist_ok=True)
        if subdir == 'sqls':
            shutil.copyfile(pkg_resources.resource_filename('lens2', f'lens/resources/sql_sample.sql'),
                            os.path.join(temp_path, "sql_sample.sql"))
        else:
            shutil.copyfile(pkg_resources.resource_filename('lens2', f"lens/resources/"
                                                                     f"{subdir.replace('s', '')}_sample.yaml"),
                            os.path.join(temp_path, f"{subdir}_sample.yaml"))

    # Copy docker-compose.yaml file, makefile and env.env
    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/docker-compose.yaml'),
                    os.path.join(main_dir, 'docker-compose.yaml'))

    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/Makefile'),
                    os.path.join(main_dir, 'Makefile'))

    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/env.env'), os.path.join(main_dir, '.env'))

    with open(os.path.join(main_dir, '.env'), "r") as env_file:
        lines = env_file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("LENS2_NAME"):
            lines[i] = f"{'LENS2_NAME'}={lens_name}\n"
        elif line.startswith("LENS2_SOURCE_TYPE"):
            lines[i] = f"{'LENS2_SOURCE_TYPE'}={source_type}\n"

    # Write the modified lines back to the .env file
    with open(os.path.join(main_dir, '.env'), "w") as env_file:
        env_file.writelines(lines)


def add_subparser(subparsers):
    parser = subparsers.add_parser("create", help="Create lens2 template")
    parser.set_defaults(func=execute_lens)
    parser.add_argument("-d", "--dir-name", required=True, help="Name of lens folder")
    parser.add_argument("-n", "--name", required=True, help="Name of the lens")
    parser.add_argument("-s", "--source-type", required=False,
                        help="Type of the source (e.g., depot, themis or minerva)")
    parser.add_argument("-p", "--parent-dir", required=False,
                        help="Parent directory where the lens directory will be created")


def execute_lens(args):
    create_project_structure(args)
