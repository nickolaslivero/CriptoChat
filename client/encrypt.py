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
    symmetric_key = b"\xa7\xdb\xdfH~\x87\xf0\xfb\x88\x81\xb2\xb4\xb1\x1c\xde\xaa\xfd\xfa\rUN{v\x88" # generate_3des_key()
    print(symmetric_key)

    # Mensagem para criptografar
    original_message = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC98ShQMsgZZip+\nS2C4Xm4q+GKSBHp9Kcbz3tLOP43vIBwCqFP1DPDyhBeDKf2sEu8j5KpO+E6hD6VA\n7zwhdnzVRatgkOmlEY2l2ADrVkUf49PcnKMwubX9yXUwSf2i69bs2sGhAqKJYIQK\nUcQozBDQfhXXbUjHweQZncB55eDDO9LomQnDlNvRDP2R6C+/qlG0fYZdgmEYxOh3\ncPRY4NjObwQH9VbdDQE5QVcPuOFn+FCMozmfCA8EPnaWFcyiLY2Z+g4BCAvDAUy2\n9iBbR/3zDA8Tsu5SjFoXNVeSPbg0Y/HNz1irEMuaRTCM5MOydngQGUBAfiqZeXiN\ne/sbLcRXAgMBAAECggEAQvWiiA824llVbptlF+nWPZi9qwsgIUKai/tH5oSaJSv1\nI+yyWEd9I4l0fn1Nm507J7SjY15+3aGV2Lvdv1A1drvuTAcaDuKOxGHPBSevC6x1\n0iZ4EyPM6BBemyziWM56QJpnuzqiEPrw4XBszhMOdGmWipDQoPcV0f/+TBrBbyFq\n1cuazL46YQsGPkOunpAjowx6NDaIku1MBUegWOQzPDNtbITN8tJ/rRQrECe1MuLx\nE91F9jI0Pzx8lgaMvzQQrZTZJ4hxopeJs9tAugfM/Suwm0yeoXpwYgYIBBJt+wQb\nstpLDDyA9N6+jAk28+xkW1TiM6+eKg45DkmDoYWNDQKBgQDh/OAhQywB4yNLnBLH\nwAL6b20w3EaBKcJmzlRL7nOf6SmOaXboy651nIE7YXk4Y8iJ9xaHUQ+IL4Kc8Gor\nJ2l40OnkWbPEc3Iy8UY3ZlORMi8DOFB0Rydf8dGHyvCzTi5HXGqaeK96xmTU92EA\nq5kOsA9ZMDmuehv5N1QmsIz9ZQKBgQDXKsyTPms+S055rzT1+hJdrYTjQxMlGVg0\nR1As80QBtFDITCKORaonVnqqI9aXHsRxtB9fOQhAKlFKUHQrZB6Mwjh4obiqq3yu\ndq14qcdBML9gAMHGpiJEoUyhcad4IdxkjXudRq3eiG6d2SoK5NUnSy6wkYp/xYq0\ndOobOJHNCwKBgER36TAqudqYhskRsF70vfJCcEKtem8Hx+599OxMgpugeQa8zVoa\n2/CmSkFDdwautMOYKSs2VA5e1qPV81S/zCTepv6Ybu7GS4NDtpJyXj9PhQ7ksPuJ\n01QuX91UjzjEJyFXzrSefAwmr8YWbT1WwDjC/uN2yQMj2/XV3ZkbRJxBAoGBAL62\nCK1Z3eRRCzV/vglnpW+ypN5qTUXMuQldTAsLc3OvRwrBsL85sB8932t+aG15r9S4\nOjZEbrOwzmx38v+ithE89KC3dt6PMOvR9N/GW/3EH1wQT7CrACSkcy+FdVJdcOMP\nJEm6o9FiS+lM2p7dRLCXSsLlvUSS6uYX2ohWE6URAoGBAJjkssUhiUjqOPjZQvfs\nZRSzNK3vAkyUmY3tlpXSsdFvUTEGVTamyQur/wEWpehBzVcfniUVLIObQJnom0tx\nWRY/HahuexnWXKw1azVvPFvFJoacRz5gVAiQgCw9cBHfZbkTTbCN/uvQ/sUk4crw\nsUm0tXwXjaMzqIm8pXzY/0ss\n-----END PRIVATE KEY-----\n"
    
    # Criptografar a mensagem
    encrypted_message = encrypt_message(original_message, symmetric_key)
    print(f"Mensagem criptografada: {encrypted_message}")

    # Descriptografar a mensagem
    decrypted_message = decrypt_message(encrypted_message, symmetric_key)
    print(f"Mensagem descriptografada: {decrypted_message}")
