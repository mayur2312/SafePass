# SafePass - CLI Password Manager

SafePass is a terminal-based password manager built in Python. It uses AES encryption and master password protection.

## Features
- Master password protection
- Add, update, reveal, and delete passwords
- Encrypted local database (Fernet)
- CLI commands with `--help` support

## Usage

Run the script using:
Master Password Commands
1. Set Master Password:
password_manager set-master --master <your_master_password>
Password Entry Management
2. Add New Entry:
password_manager add --name <entry_name> --user <username> --password <password>
3. List All Entries (Masked):
password_manager list
4. List All Entries (Unmasked):
password_manager list-unmasked
5. Reveal Specific Password:
password_manager reveal --name <entry_name>
6. Update Password:
password_manager update --name <entry_name> --password <new_password>
7. Delete Password:
password_manager delete --name <entry_name>
Help Command
8. Display Help Menu:
password_manager -h
Example Usage
password_manager set-master --master "MySecretMaster123"
password_manager add --name "Gmail" --user "me@gmail.com" --password "StrongP@ss!"
SafePass Password Manager - Command Reference Sheet
password_manager list
password_manager list-unmasked
password_manager reveal --name "Gmail"
password_manager update --name "Gmail" --password "NewStrongP@ss!"
password_manager delete --name "Gmail"
