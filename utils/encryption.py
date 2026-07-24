from cryptography.fernet import Fernet
from pathlib import Path
import utils.files

def get_secret():
    conf_home = Path.home() / ".secret"
    if conf_home.exists():
        print("Using secret file")
        return utils.files.read_file(conf_home)
    else:
        print("create secret file")
        key = Fernet.generate_key()
        utils.files.write_file(conf_home, key.decode("utf-8"))
        return key
def encrypt_string(key,item):
    cipher_suite = Fernet(key)

    # 3. Encrypt the string
    # Strings must be converted to bytes using .encode() before encryption
    bytes_to_encrypt = item.encode("utf-8")
    encrypted_token = cipher_suite.encrypt(bytes_to_encrypt)
    return encrypted_token.decode("utf-8")
def decrypt_string(key,encrypted_token):
    cipher_suite = Fernet(key)
    bytes_to_decrypt = cipher_suite.decrypt(encrypted_token)
    return bytes_to_decrypt.decode("utf-8")
