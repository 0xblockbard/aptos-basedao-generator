import os
import fileinput
import subprocess

# Base directory where the DAOs are located
base_dir    = ""
module_addr = "basedao_addr"

# Init params
start_index = 0
num_daos    = 10
dao_type    = "standard_dao"

def rename_directories_and_update_contracts():
    for i in range(start_index, start_index + num_daos):
        dao_dir = os.path.join(base_dir, f"{dao_type}_{i}")
        new_dao_dir = os.path.join(base_dir, f"{dao_type}_{i+1}")

        # Rename the directory
        os.rename(dao_dir, new_dao_dir)

        # Path to the Move file
        move_file = os.path.join(new_dao_dir, "sources", f"{dao_type}.move")

        # Edit the Move contract to update module name and APP_OBJECT_SEED
        update_move_contract(move_file, i+1, dao_type)

        # Update Move.toml file
        update_move_toml(new_dao_dir, i+1)

        # Compile and publish the Move contract
        compile_and_publish_separately(new_dao_dir)


def update_move_contract(move_file, dao_number, dao_type):
    # Check if the Move file exists
    if not os.path.exists(move_file):
        print(f"Move file {move_file} not found. Skipping.")
        return

    # Convert the dao_type to uppercase for the APP_OBJECT_SEED
    dao_type_upper = dao_type.upper()

    # Edit the Move contract to update both the module name and the APP_OBJECT_SEED
    with fileinput.FileInput(move_file, inplace=True) as file:
        for line in file:
            if line.startswith("module"):
                # Update the module name
                updated_line = f"module basedao_addr::{dao_type}_{dao_number} {{\n"
                print(updated_line, end="")
            elif line.strip().startswith("const APP_OBJECT_SEED"):
                # Update the APP_OBJECT_SEED value
                updated_seed = f'const APP_OBJECT_SEED : vector<u8> = b"{dao_type_upper}_{dao_number}";\n'
                print(updated_seed, end="")
            else:
                print(line, end="")


def update_move_toml(directory, dao_number):
    move_toml_path = os.path.join(directory, "Move.toml")

    # Check if Move.toml file exists
    if not os.path.exists(move_toml_path):
        print(f"Move.toml file {move_toml_path} not found. Skipping.")
        return

    # Edit the [package] section to update the name
    with fileinput.FileInput(move_toml_path, inplace=True) as file:
        for line in file:
            if line.startswith("name"):
                # Update the name field
                updated_line = f'name = "{dao_type}_{dao_number}"\n'
                print(updated_line, end="")
            else:
                print(line, end="")

def compile_and_publish_separately(directory):
    try:
        process = subprocess.run(
            ["aptos", "move", "publish", "--profile", "default"],
            cwd=directory,
            input="yes\n",  # Automatically send "yes" input
            text=True,      # Treat input/output as text (string)
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during compile/publish: {e}")

if __name__ == "__main__":
    rename_directories_and_update_contracts()
