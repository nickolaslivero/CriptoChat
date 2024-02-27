import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_key_str, public_key_str


def rsa_encrypt(string_to_encrypt, public_key_str):
    public_key = serialization.load_pem_public_key(
        public_key_str.encode("utf-8"), backend=default_backend()
    )
    message = (
        string_to_encrypt
        if isinstance(string_to_encrypt, (bytes, bytearray))
        else string_to_encrypt.encode("utf-8")
    )
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted


def rsa_decrypt(encrypted_string, private_key_str):
    private_key = serialization.load_pem_private_key(
        private_key_str.encode("utf-8"), password=None, backend=default_backend()
    )
    decrypted = private_key.decrypt(
        encrypted_string,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return (
        decrypted
        if isinstance(decrypted, (bytes, bytearray))
        else decrypted.decode("utf-8")
    )


if __name__ == "__main__":
    private_key, public_key = generate_rsa_keys()
    with open("keys.json", "w") as file:
        json.dump({"private_key": private_key, "public_key": public_key}, file)
