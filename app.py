#!/usr/bin/env python3
import streamlit as st
import sys
import types
import os
from pathlib import Path

ENCRYPTION_CONFIG = {"salt": b"unlearning_salt_v1_2024", "iterations": 600000}

class SecureModuleLoader:
    def __init__(self):
        self.decryption_key = None
        self.loaded_modules = {}
        
    def _derive_key(self, password: str):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=ENCRYPTION_CONFIG["salt"], iterations=ENCRYPTION_CONFIG["iterations"])
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def _decrypt_module(self, encrypted_data: bytes):
        from cryptography.fernet import Fernet
        if not self.decryption_key:
            raise RuntimeError("Decryption key not initialized")
        fernet = Fernet(self.decryption_key)
        decrypted = fernet.decrypt(encrypted_data)
        parts = decrypted.split(b"---CONTENT---\n")
        header = parts[0].decode("utf-8")
        code = parts[1].decode("utf-8") if len(parts) > 1 else ""
        return code
    
    def initialize(self, password: str):
        self.decryption_key = self._derive_key(password)
        
    def load_module_from_file(self, enc_path: str, module_name: str):
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        
        # Dogrudan dosyadan oku
        with open(enc_path, "rb") as f:
            encrypted_data = f.read()
        
        code = self._decrypt_module(encrypted_data)
        module = types.ModuleType(module_name)
        exec(code, module.__dict__)
        self.loaded_modules[module_name] = module
        return module

_module_loader = SecureModuleLoader()

def initialize_security():
    try:
        password = st.secrets["encryption"]["build_password"]
        _module_loader.initialize(password)
        return True
    except Exception as e:
        st.error(f"Security initialization failed: {e}")
        return False

@st.cache_resource
def load_core_modules():
    modules = {}
    files = [
        ("encrypted/core/engine.py.enc", "engine"),
        ("encrypted/core/therapy.py.enc", "therapy"),
        ("encrypted/ui/components.py.enc", "components")
    ]
    for file_path, name in files:
        with st.spinner(f"Loading {name}..."):
            module = _module_loader.load_module_from_file(file_path, name)
            modules[name] = module
    return modules

def main():
    st.set_page_config(page_title="Unlearning Machine", page_icon="🧠", layout="wide")
    if not initialize_security():
        st.stop()
    try:
        modules = load_core_modules()
    except Exception as e:
        st.error(f"Critical error loading modules: {e}")
        st.stop()
    
    engine = modules["engine"].get_engine()
    therapy = modules["therapy"]
    ui = modules["components"]
    ui.render_main_interface(engine, therapy)

if __name__ == "__main__":
    main()
