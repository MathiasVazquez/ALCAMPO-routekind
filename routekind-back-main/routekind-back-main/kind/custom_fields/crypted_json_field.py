import json
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

# Usa la clave de cifrado de la configuración
secret_key = settings.FIELD_ENCRYPTION_KEY.encode()
cipher_suite = Fernet(secret_key)


class CryptedJSONField(models.JSONField):

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.encrypt_data(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            crypted_valud = json.loads(value).get("c")
            return self.decrypt_data(crypted_valud)
        except (InvalidToken, ValueError):
            return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, dict):
            return value  # Already a dict, no need to decrypt
        try:
            return self.decrypt_data(value)
        except (InvalidToken, ValueError):
            return value

    def encrypt_data(self, data):
        if data is None:
            return None
        json_data = json.dumps(data)
        encrypted_data = cipher_suite.encrypt(json_data.encode())
        return json.dumps({"c": encrypted_data.decode()})

    def decrypt_data(self, data):
        if not data:
            return None
        if isinstance(data, dict):
            return data  # Already a dict, no need to decrypt
        decrypted_data = cipher_suite.decrypt(data.encode())
        return json.loads(decrypted_data.decode())
