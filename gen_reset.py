import os
import fileinput
import subprocess

# Base directory where the DAOs are located
base_dir    = ""
module_addr = "basedao_addr"

# Init params
current_index = 0
reset_index   = 10
dao_type      = "standard_dao"

def reset_dao_number(current_index, reset_index):
    dao_dir = os.path.join(base_dir, f"{dao_type}_{current_index}")
    new_dao_dir = os.path.join(base_dir, f"{dao_type}_{reset_index}")
    
    # Check if the directory exists
    if not os.path.exists(dao_dir):
        print(f"DAO directory {dao_dir} not found. Exiting.")
        return
    
    # Path to the Move file
    move_file = os.path.join(dao_dir, "sources", f"{dao_type}.move")

    # Edit the Move contract to reset the module name and APP_OBJECT_SEED
    update_move_contract(move_file, reset_index, dao_type)

    # Update Move.toml file
    update_move_toml(dao_dir, reset_index)

    # Rename the DAO directory to the new index
    reset_dao_directory(dao_dir, new_dao_dir)


def update_move_contract(move_file, new_index, dao_type):
    # Check if the Move file exists
    if not os.path.exists(move_file):
        print(f"Move file {move_file} not found. Skipping.")
        return

    # Convert the dao_type to uppercase for the APP_OBJECT_SEED
    dao_type_upper = dao_type.upper()

    # Edit the Move contract to reset both the module name and the APP_OBJECT_SEED
    with fileinput.FileInput(move_file, inplace=True) as file:
        for line in file:
            if line.startswith("module"):
                # Reset the module name
                updated_line = f"module basedao_addr::{dao_type}_{new_index} {{\n"
                print(updated_line, end="")
            elif line.strip().startswith("const APP_OBJECT_SEED"):
                # Reset the APP_OBJECT_SEED value
                updated_seed = f'const APP_OBJECT_SEED : vector<u8> = b"{dao_type_upper}_{new_index}";\n'
                print(updated_seed, end="")
            else:
                print(line, end="")


def update_move_toml(directory, new_index):
    move_toml_path = os.path.join(directory, "Move.toml")

    # Check if Move.toml file exists
    if not os.path.exists(move_toml_path):
        print(f"Move.toml file {move_toml_path} not found. Skipping.")
        return

    # Edit the [package] section to reset the name
    with fileinput.FileInput(move_toml_path, inplace=True) as file:
        for line in file:
            if line.startswith("name"):
                # Reset the name field
                updated_line = f'name = "{dao_type}_{new_index}"\n'
                print(updated_line, end="")
            else:
                print(line, end="")


def reset_dao_directory(current_dir, new_dir):
    # Check if the new directory already exists to avoid conflicts
    if os.path.exists(new_dir):
        print(f"New DAO directory {new_dir} already exists. Exiting.")
        return

    # Rename the current directory to the new one
    os.rename(current_dir, new_dir)
    print(f"Renamed {current_dir} to {new_dir}")


# Call the reset function with initialized params
reset_dao_number(current_index, reset_index)
