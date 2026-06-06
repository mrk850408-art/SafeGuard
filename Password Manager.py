import os
import base64
import json
import secrets
import string
from getpass import getpass
from cryptography.fernet import Fernet
from argon2.low_level import hash_secret_raw, Type

# ------------- Colorama setup -------------
from colorama import init, Fore, Style
init(autoreset=True)

# Optional clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# ASCII banner
BANNER = r"""
::::::::      :::     :::::::::: :::::::::: ::::::::  :::    :::     :::     :::::::::  :::::::::  
:+:    :+:   :+: :+:   :+:        :+:       :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:    :+: 
+:+         +:+   +:+  +:+        +:+       +:+        +:+    +:+  +:+   +:+  +:+    +:+ +:+    +:+ 
+#++:++#++ +#++:++#++: :#::+::#   +#++:++#  :#:        +#+    +:+ +#++:++#++: +#++:++#:  +#+    +:+ 
       +#+ +#+     +#+ +#+        +#+       +#+   +#+# +#+    +#+ +#+     +#+ +#+    +#+ +#+    +#+ 
#+#    #+# #+#     #+# #+#        #+#       #+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#    #+# 
 ########  ###     ### ###        ########## ########   ########  ###     ### ###    ### ######### 
"""

# -------------------- Key derivation using Argon2id --------------------
def derive_key(master_password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)

    raw_key = hash_secret_raw(
        secret=master_password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )
    key = base64.urlsafe_b64encode(raw_key)
    return key, salt

# -------------------- Vault load / save --------------------
def load_vault(filename: str, key: bytes) -> list:
    f = Fernet(key)
    try:
        with open(filename, "rb") as file:
            encrypted = file.read()
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted)
    except FileNotFoundError:
        return []
    except Exception:
        print(Fore.RED + "Wrong master password or corrupted vault.")
        exit()

def save_vault(vault: list, filename: str, key: bytes):
    f = Fernet(key)
    plaintext = json.dumps(vault).encode()
    encrypted = f.encrypt(plaintext)
    with open(filename, "wb") as file:
        file.write(encrypted)

# -------------------- Password generator --------------------
def generate_password():
    """Generate a random password with user‑defined criteria."""
    print(Fore.CYAN + Style.BRIGHT + "\n--- PASSWORD GENERATOR ---")
    try:
        length = int(input(Fore.WHITE + "Password length (default 16): ") or 16)
    except ValueError:
        length = 16
    use_upper = input("Include uppercase letters? (y/n, default y): ").lower() != 'n'
    use_digits = input("Include digits? (y/n, default y): ").lower() != 'n'
    use_symbols = input("Include symbols? (y/n, default y): ").lower() != 'n'

    # Build character pool
    char_pool = string.ascii_lowercase
    required = [secrets.choice(string.ascii_lowercase)]
    if use_upper:
        char_pool += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        char_pool += string.digits
        required.append(secrets.choice(string.digits))
    if use_symbols:
        char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        required.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))

    # Ensure minimum length to fit at least one of each required type
    min_len = len(required)
    if length < min_len:
        print(Fore.YELLOW + f"Length too short to include all selected types. Minimum set to {min_len}.")
        length = min_len

    # Fill the rest of the password
    remaining = [secrets.choice(char_pool) for _ in range(length - len(required))]
    password_list = required + remaining
    secrets.SystemRandom().shuffle(password_list)  # shuffle to randomize position of required chars
    password = ''.join(password_list)

    print(Fore.GREEN + Style.BRIGHT + f"\nGenerated password: {password}")

    # Copy to clipboard if available
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(password)
            print(Fore.GREEN + "Password copied to clipboard!")
        except Exception:
            pass

    return password

# -------------------- Menu actions --------------------
def view_all(vault):
    if not vault:
        print(Fore.YELLOW + "Vault is empty.\n")
        return
    print(Fore.CYAN + Style.BRIGHT + "\n--- All stored credentials ---")
    for idx, entry in enumerate(vault, start=1):
        print(Fore.GREEN + f"{idx}. Website: {entry['website']}")
        print(Fore.WHITE + f"   Username: {entry['username']}")
        print(Fore.WHITE + f"   Password: {entry['password']}\n")

def search(vault):
    if not vault:
        print(Fore.YELLOW + "Vault is empty.\n")
        return
    query = input("Enter website to search: ").strip().lower()
    matches = [e for e in vault if e['website'].lower() == query]
    if not matches:
        print(Fore.RED + "No entry found.\n")
    else:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Search results ---")
        for e in matches:
            print(Fore.GREEN + f"Website: {e['website']}, " +
                  Fore.WHITE + f"Username: {e['username']}, " +
                  Fore.WHITE + f"Password: {e['password']}")
        print()

def add_entry(vault):
    website = input("Enter website: ").strip()
    username = input("Enter username: ").strip()

    # Offer password generation
    use_gen = input("Use a generated password? (y/n): ").lower()
    if use_gen == 'y':
        password = generate_password()
    else:
        password = input("Enter password: ").strip()

    print(Fore.CYAN + f"\nYou entered:\nWebsite: {website}\nUsername: {username}\nPassword: {password}")
    confirm = input("Is this correct? (y/n): ").lower()
    if confirm == 'y':
        vault.append({
            "website": website,
            "username": username,
            "password": password
        })
        print(Fore.GREEN + "Stored successfully!\n")
    else:
        print(Fore.YELLOW + "Entry discarded.\n")

def update_entry(vault):
    if not vault:
        print(Fore.YELLOW + "Vault is empty.\n")
        return
    website = input("Enter the website to update: ").strip().lower()
    for entry in vault:
        if entry['website'].lower() == website:
            print(Fore.CYAN + f"Current: Username={entry['username']}, Password={entry['password']}")
            new_user = input("New username (press Enter to keep current): ").strip()
            new_pass = input("New password (press Enter to keep current): ").strip()
            if new_user:
                entry['username'] = new_user
            if new_pass:
                entry['password'] = new_pass
            print(Fore.GREEN + "Entry updated.\n")
            return
    print(Fore.RED + "Website not found.\n")

def delete_entry(vault):
    if not vault:
        print(Fore.YELLOW + "Vault is empty.\n")
        return
    website = input("Enter the website to delete: ").strip().lower()
    for i, entry in enumerate(vault):
        if entry['website'].lower() == website:
            print(Fore.CYAN + f"Found: {entry['website']} – {entry['username']}")
            confirm = input("Delete this entry? (y/n): ").lower()
            if confirm == 'y':
                vault.pop(i)
                print(Fore.GREEN + "Entry deleted.\n")
            else:
                print(Fore.YELLOW + "Deletion cancelled.\n")
            return
    print(Fore.RED + "Website not found.\n")

def sort_vault(vault):
    vault.sort(key=lambda e: e['website'].lower())
    print(Fore.GREEN + "Vault sorted by website.\n")

# -------------------- Main program --------------------
def main():
    VAULT_FILE = "vault.enc"
    SALT_FILE = "vault.salt"

    # 1. Master password
    master_pw = getpass(Fore.MAGENTA + "Enter your master password: ")

    # 2. Load or create salt
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as sf:
            salt = sf.read()
    else:
        salt = None

    # 3. Derive key
    key, salt = derive_key(master_pw, salt)

    # 4. Save salt if new
    if not os.path.exists(SALT_FILE):
        with open(SALT_FILE, "wb") as sf:
            sf.write(salt)
        print(Fore.GREEN + "New vault created.\n")

    # 5. Load vault
    vault = load_vault(VAULT_FILE, key)

    # 6. Show red ASCII banner
    print(Fore.RED + Style.BRIGHT + BANNER)

    # 7. Main menu loop
    while True:
        print(Fore.CYAN + Style.BRIGHT + "=" * 30)
        print(Fore.YELLOW + Style.BRIGHT + "PASSWORD MANAGER")
        print(Fore.WHITE + "1. View all")
        print("2. Search by website")
        print("3. Add new entry")
        print("4. Update an entry")
        print("5. Delete an entry")
        print("6. Sort vault by website")
        print("7. Generate a password")
        print(Fore.RED + "8. Quit")
        choice = input(Fore.WHITE + "Choose an option (1-8): ").strip()

        if choice == '1':
            view_all(vault)
        elif choice == '2':
            search(vault)
        elif choice == '3':
            add_entry(vault)
            save_vault(vault, VAULT_FILE, key)
        elif choice == '4':
            update_entry(vault)
            save_vault(vault, VAULT_FILE, key)
        elif choice == '5':
            delete_entry(vault)
            save_vault(vault, VAULT_FILE, key)
        elif choice == '6':
            sort_vault(vault)
            save_vault(vault, VAULT_FILE, key)
        elif choice == '7':
            # Generate a password without adding to vault
            generate_password()
            print()
        elif choice == '8':
            save_vault(vault, VAULT_FILE, key)
            print(Fore.GREEN + Style.BRIGHT + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()