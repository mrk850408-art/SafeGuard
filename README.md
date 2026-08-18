# SafeGuard

SafeGuard is a local password manager that encrypts all credentials using Argon2id-derived keys and Fernet encryption. It offers credential storage, search, update, deletion, sorting, and a built-in strong password generator.

## Features

- Strong encryption: Argon2id key derivation + Fernet (AES-128-CBC)
- Master password protection (never stored)
- Encrypted vault file (`vault.enc`) with salt (`vault.salt`)
- Store, view, search, update, delete, and sort credentials
- Built-in random password generator
- Optional clipboard copy (via `pyperclip`)
- Color-coded terminal output

## Installation

```bash
pip install colorama cryptography argon2-cffi pyperclip
