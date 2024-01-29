from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode

import os


def generate_3des_key():
    password = b"senha_segura"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=24,
        salt=os.urandom(16),
        iterations=100000,
        backend=default_backend(),
    )

    key = kdf.derive(password)
    return key


# Função para criptografar uma mensagem
def encrypt_message(message, key):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    message_bytes = message.encode("utf-8")
    padded_message = message_bytes + b" " * (
        8 - len(message_bytes) % 8
    )  # Preenche a mensagem para ser múltiplo de 8 bytes
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return b64encode(ciphertext).decode("utf-8")


# Função para descriptografar uma mensagem
def decrypt_message(ciphertext, key):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    ciphertext_bytes = b64decode(ciphertext)
    decrypted_message = decryptor.update(ciphertext_bytes) + decryptor.finalize()
    return decrypted_message.rstrip(b" ").decode("utf-8")


# Exemplo de uso
if __name__ == "__main__":
    # Gerar chave
    symmetric_key = generate_3des_key()
    print(symmetric_key)

    # Mensagem para criptografar
    original_message = "Olá, mundo!"

    # Criptografar a mensagem
    encrypted_message = encrypt_message(original_message, symmetric_key)
    print(f"Mensagem criptografada: {encrypted_message}")

    # Descriptografar a mensagem
    decrypted_message = decrypt_message(encrypted_message, symmetric_key)
    print(f"Mensagem descriptografada: {decrypted_message}")
