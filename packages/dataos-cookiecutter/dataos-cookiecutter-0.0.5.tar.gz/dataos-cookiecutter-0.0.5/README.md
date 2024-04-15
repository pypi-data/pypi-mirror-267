# dataos-cookiecutter

**dataos-cookiecutter** package provides commands to facilitate various tasks of Lens2, enabling users to efficiently generate templates, perform schema checks, generate data quality checks yaml, and create Board YAML configurations.

## Installation

You can install **dataos-cookiecutter** via pip:

```bash
pip install dataos-cookiecutter
```

## Usage

dataos-cookiecutter offers several commands to simplify Lens2-related tasks:

1. **lens2 lens**: This command allows users to get started by creating a sample template along with folder structure, which they can modify based on their needs. It includes two flags:
   - `-n lens_name`: Specifies the name of the Lens.
   - `-s source_type`: Specifies the type of data source.

    ```bash
    lens2 create -n <lens2_name> -d <lens2_dir_name> -s <source_type>
    ```

2. **lens2 checks**: This command provides two subcommands:
   - **schema-check**: Validates that all dimensions used in Lens2 tables are fulfilled by the SQL provided of table.
   - **create**: Creates checks YAML files and stores them in the checks folder.

    ```bash
    # Validate dimensions in Lens2 tables
    lens2 checks schema-check -n tables/views '(comma separated)'
    
    # Create checks YAML files
    lens2 checks create -n tables/views '(comma separated)'
    ```

3. **lens2 board**: This command provides two subcommands for Board related tasks:
   - **create**: Creates View Board YAML made public in Lens2 and stores files in the boards/view_name folder.
   - **start**: Uses the generated Board content and starts Board to explore. This command only requires a view name (not comma separated values).

    ```bash
    # Create Board dashboard YAML for Lens2 views
    lens2 board create -n views '(comma separated)'
    
    # Start Board with generated content of View
    lens2 board start -n view_name
    ```