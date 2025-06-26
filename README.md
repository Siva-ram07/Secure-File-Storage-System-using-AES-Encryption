Secure File Storage System (AES-256)

## Objective
This project encrypts and decrypts files locally using AES-256 (CBC mode) and checks for tampering via file hash verification.

---

###  Step 1: Folder Setup
I created the following structure:

```

SecureFileStorage-AES/
*main.py
*README.md
*sample.txt

````

---

###  Step 2: Wrote main.py (AES Encryption Code)

I wrote a Python script that:
- Uses `cryptography` library
- Generates AES-256 key and IV
- Encrypts/Decrypts files
- Stores metadata and verifies file integrity

```python
# sample from main.py
def encrypt_file(filepath):
    ...
    with open(out_path, 'wb') as f: f.write(enc)
    ...
````

---

###  Step 3: Created README.md

Added this file to explain:

* Project objective
* Tools used
* How to run it
* Features like `.enc` file generation and hash check

---

###  Step 4: Made sample.txt

I created a test file:

```
This is a sample file to demonstrate encryption.
```

Encrypted and then decrypted it using my script.

---

###  Step 5: Tested and Verified

* Ran encryption
* Decrypted the file back
* Integrity was **verified successfully** using SHA-256 hash

```bash
File encrypted and saved as encrypted_files/sample.txt.enc
Decryption successful. Integrity verified.
```

---

##  How to Run

1. Install:

```bash
pip install cryptography
```

2. Run:

```bash
python main.py
```

3. Choose:

* `1` to encrypt any file
* `2` to decrypt and verify

---

##  Output

* Encrypted files → `encrypted_files/`
* Keys → `key.bin`, `iv.bin`
* Metadata → `metadata.json`

```

---
