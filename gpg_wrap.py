#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import shlex
import getpass
import shutil
from pathlib import Path
parser = argparse.ArgumentParser( prog='gpg_wrap', description='encrypt/decrypt files with gpg command')
parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt files')
parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt files')
parser.add_argument('-p', '--password', help='password to encrypt/decrypt files')
parser.add_argument('files', action="extend", nargs="+", type=str, help='files to encrypt/decrypt')
args = parser.parse_args()

if (args.encrypt and args.decrypt) or (not args.encrypt and not args.decrypt):
    print('ERROR: choose one, encrypt (-e) or decrypt (-d)')
    sys.exit(1)

for file_name in args.files:
    if not Path(file_name).is_file():
        print(f"ERROR: file [{file_name}] does not exists. Exiting...")
        sys.exit(1)

if args.encrypt:
    encrypt_password = args.password if args.password else getpass.getpass(prompt='Password to encrypt files: ')
    encrypted_file_names_list = []
    for file_name in args.files:
        full_path_name = str(Path(file_name).resolve())
        encrypted_file_name = full_path_name + ".asc"
        gpg_cmd = f"gpg --yes --batch --symmetric --cipher-algo AES256 --armor --passphrase {encrypt_password} -o '{encrypted_file_name}' '{full_path_name}'"
        _ = subprocess.run(shlex.split(gpg_cmd), check=True, encoding="utf-8", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        encrypted_file_names_list.append(encrypted_file_name)
    for encrypted_file in encrypted_file_names_list:
        sed_cmd = f"sed -i -e '/BEGIN PGP MESSAGE/d' -e '/END PGP MESSAGE/d' {encrypted_file}"
        _ = subprocess.run(shlex.split(sed_cmd), check=True, encoding="utf-8", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        print(encrypted_file)
    sys.exit(0)

if args.decrypt:
    decrypt_password = args.password if args.password else getpass.getpass(prompt='Password to decrypt files: ')
    for file_name in args.files:
        if Path(file_name).suffix != '.asc':
            print(f"ERROR: file [{file_name}] is not encrypted file. Exiting...")
            sys.exit(1)
    decrypted_file_names_list = []
    for file_name in args.files:
        full_path_name = str(Path(file_name).resolve())
        full_path_name_tmp = str(Path(file_name).resolve()) + "_tmp"
        decrypted_file_name = full_path_name.replace(".asc", "")
        shutil.copy(full_path_name, full_path_name_tmp)
        sed_cmd = f"sed -i -e '1 i-----BEGIN PGP MESSAGE-----' -e '$ a -----END PGP MESSAGE-----' {full_path_name_tmp}"
        _ = subprocess.run(shlex.split(sed_cmd), check=True, encoding="utf-8", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        gpg_cmd = f"gpg --yes --batch --decrypt --cipher-algo AES256 --passphrase {decrypt_password} -o '{decrypted_file_name}' '{full_path_name_tmp}'"
        _ = subprocess.run(shlex.split(gpg_cmd), check=True, encoding="utf-8", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        os.remove(full_path_name_tmp)
        decrypted_file_names_list.append(decrypted_file_name)
    for decrypted_file in decrypted_file_names_list:
        print(decrypted_file)
    sys.exit(0)
