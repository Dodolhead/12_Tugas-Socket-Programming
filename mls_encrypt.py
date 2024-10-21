from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
public_key = private_key.public_key()

# Function to encrypt using AES
def aes_encrypt(plain_text, key):
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_text = iv + encryptor.update(plain_text.encode()) + encryptor.finalize()
    return encrypted_text

# Function to encrypt using RSA
def rsa_encrypt(encrypted_text):
    return public_key.encrypt(
        encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Function to decrypt using RSA
def rsa_decrypt(encrypted_text):
    return private_key.decrypt(
        encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Function to decrypt using AES
def aes_decrypt(encrypted_text, key):
    iv = encrypted_text[:16]  # Extract the IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(encrypted_text[16:]) + decryptor.finalize()
    return decrypted_text.decode()

# Example usage
message = "Hello, this is a secret message!"
aes_key = os.urandom(32)  # Generate a random 256-bit key for AES

# Multi-level encryption
encrypted_aes = aes_encrypt(message, aes_key)
encrypted_rsa = rsa_encrypt(encrypted_aes)

# Multi-level decryption
decrypted_aes = aes_decrypt(rsa_decrypt(encrypted_rsa), aes_key)
print(decrypted_aes)  # Output: Hello, this is a secret message!
