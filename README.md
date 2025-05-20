# SafePass - CLI Password Manager

SafePass is a terminal-based password manager built in Python. It uses AES encryption and master password protection.

# 1. sudo apt update && sudo apt install git -y

# 2. Clone the SafePass repository
     git clone https://github.com/mayurbopche23/SafePass.git

# 3. Navigate to the project folder
    cd safepass

# 4. (Optional) Set executable permissions for the main script
    chmod +x password_manager.py

# 5. Create a symbolic link to run the tool globally
    sudo ln -s "$(pwd)/password_manager.py" /usr/local/bin/password_manager

# 6. Run the tool
    password_manager -h

## Features
- Master password protection
- Add, update, reveal, and delete passwords
- Encrypted local database (Fernet)
- CLI commands with `--help` support

## Usage

Run the script using:

1. Display Help Menu:
password_manager -h
Master Password Commands
2. Set Master Password:
password_manager set-master --master <your_master_password>
Password Entry Management
3. Add New Entry:
password_manager add --name <entry_name> --user <username> --password <password>
4. List All Entries (Masked):
password_manager list
5. List All Entries (Unmasked):
password_manager list-unmasked
6. Reveal Specific Password:
password_manager reveal --name <entry_name>
7. Update Password:
password_manager update --name <entry_name> --password <new_password>
8. Delete Password:
password_manager delete --name <entry_name>


Example Usage:
1. Python3 password_manager set-master --master "MySecretMaster123"
2. password_manager add --name "Gmail" --user "me@gmail.com" --password "StrongP@ss!"
3. SafePass Password Manager - Command Reference Sheet
4. password_manager list
5. password_manager list-unmasked
6. password_manager reveal --name "Gmail"
7. password_manager update --name "Gmail" --password "NewStrongP@ss!"
8. password_manager delete --name "Gmail"
