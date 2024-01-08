from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_string(string_to_encrypt, public_key):
    message = string_to_encrypt.encode('utf-8')
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def decrypt_string(encrypted_string, private_key):
    decrypted = private_key.decrypt(
        encrypted_string,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')


if __name__ == "__main__":
    private_key, public_key = generate_key_pair()
    text_to_encrypt = "SEBA"

    encrypted_text = encrypt_string(text_to_encrypt, public_key)
    print("Texto criptografado:", encrypted_text)

    decrypted_text = decrypt_string(encrypted_text, private_key)
    print("Texto descriptografado:", decrypted_text)
