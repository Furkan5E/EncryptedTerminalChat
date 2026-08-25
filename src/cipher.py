from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key() -> bytes:
    """Generates a secure 32-byte symmetric Fernet key."""
    return Fernet.generate_key()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a plaintext string into a secure byte payload."""
    f = Fernet(key)
    return f.encrypt(message.encode('utf-8'))

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decrypts a secure byte payload back into a plaintext string."""
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode('utf-8')

def generate_rsa_keypair():
    """Generates an ephemeral 2048-bit asymmetric RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialise_public_key(public_key) -> bytes:
    """Converts an RSA public key object into transmitable PEM bytes."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialise_public_key(pem_bytes: bytes):
    """Converts received PEM bytes back into an RSA public key object."""
    return serialization.load_pem_public_key(pem_bytes)