from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """Generates a secure 32-byte url-safe base64-encoded key."""
    return Fernet.generate_key()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a plaintext string and returns encrypted bytes."""
    cipher = Fernet(key)
    return cipher.encrypt(message.encode('utf-8'))

def decrypt_message(encrypted_bytes: bytes, key: bytes) -> str:
    """Decrypts bytes and returns the original plaintext string."""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_bytes).decode('utf-8')