# 🔐 SafeGuard Password Manager

A command-line **password manager** built in Python.  
It stores your credentials **encrypted** using strong, modern cryptography (Argon2id + Fernet/AES-128).  
The vault is protected by a single **master password** – only you can unlock it.


## ✨ Features

- 🔒 **Zero‑knowledge encryption** – your data is encrypted before it touches the disk
- 🧠 **Argon2id key derivation** – memory‑hard, brute‑force resistant
- 🔐 **Fernet (AES‑128‑CBC + HMAC)** for authenticated encryption
- 🎨 **Colored terminal interface** using `colorama`
- 👁️ **Hidden master password input** (like `sudo`)
- 📋 **Clipboard support** – generated passwords auto‑copied (optional)
- 🗂️ **Full CRUD** – view, add, update, delete entries
- 🔍 **Search** by website name
- 🧹 **Sort** vault alphabetically
- 🎲 **Password generator** – customizable length, character sets
- 💾 **Single encrypted file** – easy to back up or move

---

## 🧪 Tech Stack

| Component          | Technology               |
|--------------------|--------------------------|
| Encryption         | Fernet (AES‑128‑CBC + HMAC) |
| Key derivation     | Argon2id (via `argon2-cffi`) |
| Password input     | `getpass` (hidden typing) |
| Terminal styling   | `colorama`               |
| Randomness         | `secrets` module         |
| Clipboard (opt.)   | `pyperclip`              |
| Language           | Python 3.8+              |

---


🚀 Usage

Run the script from your terminal:
bash

python3 password_manager.py

The first time, you’ll be asked to create a master password.
A new encrypted vault (vault.enc) and a salt file (vault.salt) will be created in the same folder.

Always keep these two files together!
Main menu

1. View all              – list all stored credentials
2. Search by website     – find an entry by website name
3. Add new entry         – store a new credential
4. Update an entry       – change username or password
5. Delete an entry       – remove a credential
6. Sort vault by website – alphabetically reorder the vault
7. Generate a password   – create a strong random password
8. Quit                  – exit and save


🔑 Password generator

Option 7 (or during “Add new entry”) launches the generator:

    Choose length (default 16)

    Include uppercase letters, digits, symbols (each default = yes)

    At least one character from each selected set is guaranteed

    The password is printed and, if pyperclip is installed, automatically copied to the clipboard

⚠️ Security notes

This tool was built as an educational and personal project.
It implements strong cryptographic primitives, but it has limitations:

    Memory safety – Python cannot lock or securely wipe memory. The master password and decrypted vault remain in RAM while the program runs.

    No two‑factor authentication – Your master password is the sole secret.

    Clipboard – Copied passwords may linger in your system’s clipboard history (varies by OS).

    Offline only – No cloud sync, no browser integration.

For real‑world daily use, consider established password managers (Bitwarden, KeePassXC, etc.).
This tool is perfect for learning, offline backups, or as a minimal, trust‑yourself‑only vault.
📁 File structure
text


📋 Requirements

    Python 3.8+

    cryptography

    argon2-cffi

    colorama

    pyperclip (optional)

All can be installed via requirements.txt.
🧪 Running tests (if you add them later)
bash

pytest

📜 License

This project is open‑source under the MIT License. See LICENSE for details.
🙌 Acknowledgements

    Fernet

    Argon2

    Colorama

    pyperclip

🛠️ Author & Contributions

Made by sudo-scorpion
Feel free to open issues or pull requests!
