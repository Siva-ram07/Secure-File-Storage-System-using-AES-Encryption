import os, json, hashlib
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

KEY_FILE, IV_FILE = 'key.bin', 'iv.bin'
META_FILE, STORAGE = 'encrypted_files'
os.makedirs(STORAGE, exist_ok=True)

def generate_key_iv():
    open(KEY_FILE, 'wb').write(os.urandom(32))
    open(IV_FILE, 'wb').write(os.urandom(16))

def load_key_iv():
    return open(KEY_FILE, 'rb').read(), open(IV_FILE, 'rb').read()

def encrypt_file(filepath):
    key, iv = load_key_iv()
    with open(filepath, 'rb') as f: data = f.read()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
    out_path = os.path.join(STORAGE, os.path.basename(filepath) + '.enc')
    with open(out_path, 'wb') as f: f.write(enc)
    log_metadata(filepath, out_path, hashlib.sha256(data).hexdigest())
    print(f'Encrypted: {out_path}')

def decrypt_file(enc_path, out_path):
    key, iv = load_key_iv()
    with open(enc_path, 'rb') as f: enc = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    dec_padded = cipher.decryptor().update(enc) + cipher.decryptor().finalize()
    data = padding.PKCS7(128).unpadder().update(dec_padded) + padding.PKCS7(128).unpadder().finalize()
    with open(out_path, 'wb') as f: f.write(data)
    hash_check = hashlib.sha256(data).hexdigest()
    if verify(os.path.basename(out_path), hash_check): print("Verified.")
    else: print("Warning: Integrity check failed!")

def log_metadata(original, enc, file_hash):
    meta = json.load(open(META_FILE)) if os.path.exists(META_FILE) else {}
    meta[os.path.basename(original)] = {"path": enc, "time": str(datetime.now()), "hash": file_hash}
    json.dump(meta, open(META_FILE, 'w'), indent=2)

def verify(name, new_hash):
    meta = json.load(open(META_FILE))
    return meta.get(name, {}).get('hash') == new_hash

if __name__ == '__main__':
    if not os.path.exists(KEY_FILE): generate_key_iv()
    print("1. Encrypt 2. Decrypt"); c = input("Choice: ")
    if c == '1': encrypt_file(input("File to encrypt: "))
    elif c == '2': decrypt_file(input("Encrypted file: "), input("Save as: "))
