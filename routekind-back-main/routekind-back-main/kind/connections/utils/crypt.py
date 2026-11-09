# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from base64 import urlsafe_b64encode, urlsafe_b64decode
# import os
import string


# def generate_key(salt: str, password: str) -> bytes:
#     """Genera una clave a partir de un salt y una contraseña (password)"""
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt.encode(),
#         iterations=1000,
#         backend=default_backend()
#     )
#     return kdf.derive(password.encode())


# def encrypt_id(id: str, salt: str) -> str:
#     """Cifra el id utilizando el salt como clave"""
#     key = generate_key(salt, salt)  # Usando el salt como 'password' para simplicidad
#     iv = os.urandom(16)  # Vector de inicialización
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     encrypted_id = encryptor.update(id.encode()) + encryptor.finalize()
#     return urlsafe_b64encode(iv + encrypted_id).decode()


# def decrypt_key(encrypted_key: str, salt: str) -> str:
#     """Descifra el encrypted_key utilizando el salt"""
#     key = generate_key(salt, salt)
#     data = urlsafe_b64decode(encrypted_key.encode())
#     iv, encrypted_id = data[:16], data[16:]
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     return (decryptor.update(encrypted_id) + decryptor.finalize()).decode()

def vigenere_encrypt(text: str, key: str):
    alphabet = string.ascii_letters + string.digits  # + '-'  # Alfabeto alfanumérico + '-'
    extended_key = (key * (len(text) // len(key) + 1))[:len(text)]
    crypt_text = ""

    for t, c in zip(text, extended_key):
        if t not in alphabet:
            crypt_text += t
        else:
            new_index = (alphabet.index(t) + alphabet.index(c)) % len(alphabet)
            crypt_text += alphabet[new_index]

    return crypt_text.replace('-', '')


def vigenere_decrypt(crypt_text: str, key: str):
    new_crypt_text = []
    for i, char in enumerate(crypt_text):
        if i in [8, 12, 16, 20]:
            new_crypt_text.append('-')
        new_crypt_text.append(char)

    alphabet = string.ascii_letters + string.digits  # + '-'
    extended_key = (key * (len(new_crypt_text) // len(key) + 1))[:len(new_crypt_text)]
    decrypt_text = ""

    for t, c in zip(new_crypt_text, extended_key):
        if t not in alphabet:
            decrypt_text += t
        else:
            new_index = (alphabet.index(t) - alphabet.index(c)) % len(alphabet)
            decrypt_text += alphabet[new_index]

    return decrypt_text
