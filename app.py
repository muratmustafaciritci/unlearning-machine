#!/usr/bin/env python3
import streamlit as st
import sys, types, os

ENCRYPTION_CONFIG = {"salt": b"unlearning_salt_v1_2024", "iterations": 600000}
GITHUB_REPO = {"owner": None, "name": None, "token": None}

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
        path_line = [l for l in header.split("\n") if l.startswith("PATH:")][0]
        module_path = path_line.replace("PATH:", "").strip()
        return module_path, code
    
    def _fetch_from_github(self, file_path: str):
        import requests
        import base64
        if not all(GITHUB_REPO.values()):
            raise RuntimeError("GitHub configuration missing")
        url = f"https://api.github.com/repos/{GITHUB_REPO['owner']}/{GITHUB_REPO['name']}/contents/{file_path}"
        headers = {"Authorization": f"token {GITHUB_REPO['token']}", "Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise RuntimeError(f"GitHub API error: {response.status_code}")
        return base64.b64decode(response.json().get("content", ""))
    
    def initialize(self, password: str):
        self.decryption_key = self._derive_key(password)
        
    def load_module(self, enc_path: str, module_name: str = None):
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        encrypted_data = self._fetch_from_github(enc_path)
        original_path, code = self._decrypt_module(encrypted_data)
        if not module_name:
            module_name = original_path.replace("/", ".").replace(".py", "")
        module = types.ModuleType(module_name)
        module.__file__ = original_path
        exec(code, module.__dict__)
        self.loaded_modules[module_name] = module
        return module

_module_loader = SecureModuleLoader()

def initialize_security():
    try:
        GITHUB_REPO["owner"] = st.secrets["github"]["owner"]
        GITHUB_REPO["name"] = st.secrets["github"]["name"]
        GITHUB_REPO["token"] = st.secrets["github"]["token"]
        password = st.secrets["encryption"]["build_password"]
        _module_loader.initialize(password)
        return True
    except Exception as e:
        st.error(f"Security initialization failed: {e}")
        return False

@st.cache_resource
def load_core_modules():
    modules = {}
    files = [("encrypted/core/engine.py.enc", "engine"), ("encrypted/core/therapy.py.enc", "therapy"), ("encrypted/ui/components.py.enc", "components")]
    for file_path, name in files:
        with st.spinner(f"Loading {name}..."):
            module = _module_loader.load_module(file_path, name)
            modules[name] = module
    return modules

def main():
    st.set_page_config(page_title="Unlearning Machine", page_icon="🧠", layout="wide")
    if not initialize_security():
        st.stop()
    try:
        modules = load_core_modules()
    except Exception as e:
        st.error("Critical error loading modules")
        st.stop()
    engine = modules["engine"].get_engine()
    therapy = modules["therapy"]
    ui = modules["components"]
    ui.render_main_interface(engine, therapy)

if __name__ == "__main__":
    main()
