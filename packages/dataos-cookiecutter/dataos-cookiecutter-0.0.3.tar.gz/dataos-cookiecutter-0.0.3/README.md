# dataos-cookiecutter

**dataos-cookiecutter** package provides commands to facilitate various tasks of Lens2, enabling users to efficiently generate templates, perform schema checks, generate data quality checks yaml, and create Rill YAML configurations.

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
    lens2 lens create -n <lens_name> -s <source_type>
    ```

2. **lens2 checks**: This command provides two subcommands:
   - **schema-check**: Validates that all dimensions used in Lens2 tables are fulfilled by the SQL provided for them.
   - **create**: Creates checks YAML files and stores them in the checks folder.

    ```bash
    # Validate dimensions in Lens2 tables
    lens2 checks schema-check
    
    # Create checks YAML files
    lens2 checks create
    ```

3. **lens2 rill**: This command provides two subcommands for Rill-related tasks:
   - **create**: Creates Rill dashboard YAML for views made public in Lens2 and stores files in the Rill folder.
   - **start**: Uses the generated Rill content and starts Rill to initiate the dashboard.

    ```bash
    # Create Rill dashboard YAML for Lens2 views
    lens2 rill create
    
    # Start Rill with generated content
    lens2 rill start
    ```