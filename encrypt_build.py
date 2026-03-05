#!/usr/bin/env python3
import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureBuildSystem:
    def __init__(self):
        self.master_key = self._get_master_key()
        self.cipher = Fernet(self.master_key)
        self.src_dir = Path("src")
        self.enc_dir = Path("encrypted")
        
    def _get_master_key(self):
        password = os.getenv("BUILD_PASSWORD")
        if not password:
            print("BUILD_PASSWORD gerekli!")
            sys.exit(1)
        salt = b"unlearning_salt_v1_2024"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_file(self, src_path):
        with open(src_path, "rb") as f:
            content = f.read()
        relative_path = src_path.relative_to(self.src_dir)
        metadata = f"PATH:{relative_path}\nSIZE:{len(content)}\n".encode()
        payload = metadata + b"---CONTENT---\n" + content
        return self.cipher.encrypt(payload)
    
    def process_directory(self):
        import shutil
        if self.enc_dir.exists():
            shutil.rmtree(self.enc_dir)
        self.enc_dir.mkdir(parents=True)
        count = 0
        for py_file in self.src_dir.rglob("*.py"):
            enc_path = self.enc_dir / f"{py_file.relative_to(self.src_dir)}.enc"
            enc_path.parent.mkdir(parents=True, exist_ok=True)
            with open(enc_path, "wb") as f:
                f.write(self.encrypt_file(py_file))
            print(f"Encrypted: {py_file.name}")
            count += 1
        print(f"\n{count} files encrypted")

if __name__ == "__main__":
    SecureBuildSystem().process_directory()
