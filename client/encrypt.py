from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def pad(message):
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    return padded_data

def unpad(padded_data):
    unpadder = padding.PKCS7(64).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

def encrypt_3des(message, key):
    if len(key) < 24:
        key = key.ljust(24, b'0')
    elif len(key) > 24:
        key = key[:24]

    iv = os.urandom(8)

    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padded_message = pad(message)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return ciphertext, iv

def decrypt_3des(ciphertext, key, iv):
    if len(key) < 24:
        key = key.ljust(24, b'0')
    elif len(key) > 24:
        key = key[:24]

    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_message = unpad(decrypted_message)

    return unpadded_message

def encrypt_message(message):
    chave_3des = b'SuaChaveSecreta' 
    mensagem_criptografada, iv = encrypt_3des(message, chave_3des)
    return mensagem_criptografada, iv

def decrypt_message(ciphertext, iv):
    chave_3des = b'SuaChaveSecreta'
    mensagem_descriptografada = decrypt_3des(ciphertext, chave_3des, iv)
    return mensagem_descriptografada
