import pytest
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives.asymmetric import rsa
from src.cipher import encrypt_message, decrypt_message, generate_key, generate_rsa_keypair

def test_encryption_decryption():
    key = generate_key()
    original_message = "Target secured."

    encrypted = encrypt_message(original_message, key)
    decrypted = decrypt_message(encrypted, key)

    assert encrypted != original_message.encode() #ensure its actually scrambled
    assert isinstance(encrypted, bytes)
    assert decrypted == original_message #ensure reconstruction

def test_tampered_payload_raises_exception():
    key = generate_key()
    encrypted = encrypt_message("Do not tamper", key)
    
    #tamper with the bytes by changing the last character
    tampered = encrypted[:-1] + b'a'
    
    #assert that fernet catches the tampering and raises error
    with pytest.raises(InvalidToken):
        decrypt_message(tampered, key)

def test_generate_rsa_keypair_creates_valid_keys():
    private_key, public_key = generate_rsa_keypair()
    
    #verify generated objects are RSA keys
    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert isinstance(public_key, rsa.RSAPublicKey)
    
    #ensure key size is 2048 bits
    assert private_key.key_size == 2048