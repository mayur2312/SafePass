#!/usr/bin/env python3
import argparse
import sqlite3
import os
import base64
import getpass
import hashlib
from cryptography.fernet import Fernet

# File paths
DB_NAME = "password_manager.db"
KEY_FILE = "key.key"
MASTER_HASH_FILE = "master.hash"

# Generate or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
fernet = Fernet(key)

# Set master password (hashed)
def set_master(master):
    if os.path.exists(MASTER_HASH_FILE):
        print("Master password already set.")
        return
    hashed = hashlib.sha256(master.encode()).hexdigest()
    with open(MASTER_HASH_FILE, "w") as f:
        f.write(hashed)
    print("Master password set successfully.")

# Verify master password
def verify_master():
    if not os.path.exists(MASTER_HASH_FILE):
        print("Master password not set. Please set it first using: set-master --master <password>")
        return False
    master = getpass.getpass("Enter master password: ")
    with open(MASTER_HASH_FILE, "r") as f:
        stored_hash = f.read()
    if hashlib.sha256(master.encode()).hexdigest() == stored_hash:
        return True
    else:
        print("Access denied.")
        return False

# Create DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add password
def add_password(name, username, password):
    if not verify_master():
        return
    encrypted = fernet.encrypt(password.encode()).decode()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (name, username, password) VALUES (?, ?, ?)", (name, username, encrypted))
    conn.commit()
    conn.close()
    print("Password added successfully!")

# List all passwords (masked)
def list_passwords():
    if not verify_master():
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, username FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        print("\nStored Passwords:")
        for row in rows:
            print(f"Name: {row[0]}, Username: {row[1]}, Password: ********")
    else:
        print("No passwords found.")

# Reveal one password
def reveal_password(name):
    if not verify_master():
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        username, encrypted = row
        decrypted = fernet.decrypt(encrypted).decode()
        print(f"\nUsername: {username}\nPassword: {decrypted}")
    else:
        print("No entry found with that name.")

# List all passwords (unmasked) with private access key
def list_passwords_unmasked():
    secret_unmask_key = "Pirated123"  
    input_key = getpass.getpass("Enter unmask access key: ")

    if input_key != secret_unmask_key:
        print("❌ Invalid unmask access key.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print(f"\nStored Passwords (Unmasked):")
        for row in rows:
            name, username, encrypted = row
            decrypted = fernet.decrypt(encrypted).decode()
            print(f"Name: {name}, Username: {username}, Password: {decrypted}")
    else:
        print("No passwords found.")

# CLI setup
def main():
    parser = argparse.ArgumentParser(description="Simple Password Manager with Master Password")
    subparsers = parser.add_subparsers(dest="command")

    set_master_parser = subparsers.add_parser("set-master", help="Set the master password")
    set_master_parser.add_argument("--master", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new password")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--username", required=True)
    add_parser.add_argument("--password", required=True)

    list_parser = subparsers.add_parser("list", help="List all stored passwords (masked)")

    list_unmasked_parser = subparsers.add_parser("list-unmasked", help="List all stored passwords (unmasked)")
    
    reveal_parser = subparsers.add_parser("reveal", help="Reveal the password for a given name")
    reveal_parser.add_argument("--name", required=True)

    update_parser = subparsers.add_parser("update", help="Update a password")
    update_parser.add_argument("--name", required=True)
    update_parser.add_argument("--password", required=True)

    delete_parser = subparsers.add_parser("delete", help="Delete a password entry")
    delete_parser.add_argument("--name", required=True)

    args = parser.parse_args()

    init_db()

    if args.command == "set-master":
        set_master(args.master)
    elif args.command == "add":
        add_password(args.name, args.username, args.password)
    elif args.command == "list":
        list_passwords()
    elif args.command == "list-unmasked":
        list_passwords_unmasked()
    elif args.command == "reveal":
        reveal_password(args.name)
    elif args.command == "update":
        update_password(args.name, args.password)
    elif args.command == "delete":
        delete_password(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
