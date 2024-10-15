# DAO Deployment Automation Scripts

This repository includes two Python scripts designed to automate the deployment and reset of DAO contracts on the Aptos blockchain. These scripts facilitate bulk deployment and reset of DAO modules by renaming directories, updating contract files, and compiling/publishing them with updated parameters.

## Scripts Overview

### 1. `gen_automate_dao_deployment.py`

This script automates the creation and deployment of multiple DAOs on Aptos. It renames DAO directories, updates Move contract and configuration files, and compiles/publishes each DAO contract. 

#### Usage

1. **Set Up Base Parameters:**
   - Define the `base_dir`, `module_addr`, `start_index`, `num_daos`, and `dao_type` variables as needed.
2. **Run the Script:**
   - Execute the script: `python gen_automate_dao_deployment.py`
   - The script will:
     - Rename each DAO directory based on the specified `dao_type` and `num_daos`.
     - Update the module name and `APP_OBJECT_SEED` constant in the `.move` contract files.
     - Modify the `Move.toml` configuration files for each DAO.
     - Compile and publish each DAO contract separately.

#### Functions

- **`rename_directories_and_update_contracts()`**: Main function to handle the renaming, updating, and deploying process for DAOs.
- **`update_move_contract(move_file, dao_number, dao_type)`**: Updates the module name and `APP_OBJECT_SEED` constant within the `.move` file.
- **`update_move_toml(directory, dao_number)`**: Edits the `Move.toml` file to set the new DAO name.
- **`compile_and_publish_separately(directory)`**: Compiles and publishes the Move contract in the specified directory using the Aptos CLI.

### 2. `gen_reset.py`

This script resets the DAO directory structure and configuration for a specific DAO. It updates the module name and `APP_OBJECT_SEED` constant, resets the `Move.toml` file, and renames the DAO directory.

#### Usage

1. **Set Up Reset Parameters:**
   - Define the `base_dir`, `module_addr`, `current_index`, `reset_index`, and `dao_type` variables as needed.
2. **Run the Script:**
   - Execute the script: `python gen_reset.py`
   - The script will:
     - Reset the DAO directory name from `current_index` to `reset_index`.
     - Update the Move contract and `Move.toml` file to reflect the new DAO index.
     - Rename the DAO directory.

#### Functions

- **`reset_dao_number(current_index, reset_index)`**: Main function to reset DAO naming and configuration.
- **`update_move_contract(move_file, new_index, dao_type)`**: Resets the module name and `APP_OBJECT_SEED` in the `.move` file.
- **`update_move_toml(directory, new_index)`**: Resets the `Move.toml` file with the new DAO name.
- **`reset_dao_directory(current_dir, new_dir)`**: Renames the DAO directory from `current_index` to `reset_index`.

## Requirements

- Python 3.x
- Aptos CLI installed and configured
- Access to the DAO directories and corresponding `.move` and `Move.toml` files.

## Notes

- Ensure that the `base_dir` path is set to the directory containing the DAO folders.
- Adjust `module_addr` to reflect the correct base address for your DAOs.
- Run these scripts with appropriate permissions to modify file and directory names.
