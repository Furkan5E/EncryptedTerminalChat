import pytest
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives.asymmetric import rsa
from src.cipher import encrypt_message, decrypt_message, generate_key, generate_rsa_keypair, serialise_public_key, deserialise_public_key, wrap_symmetric_key, unwrap_symmetric_key

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

def test_public_key_serialization():
    _, public_key = generate_rsa_keypair()
    
    #serialise to bytes
    pem_bytes = serialise_public_key(public_key)
    assert isinstance(pem_bytes, bytes)
    assert b"-----BEGIN PUBLIC KEY-----" in pem_bytes
    
    #seserialise back to an object
    reconstructed_key = deserialise_public_key(pem_bytes)
    assert isinstance(reconstructed_key, rsa.RSAPublicKey)

def test_rsa_key_wrapping():
    private_key, public_key = generate_rsa_keypair()
    fernet_key = generate_key()
    
    wrapped_key = wrap_symmetric_key(fernet_key, public_key)
    assert wrapped_key != fernet_key
    assert isinstance(wrapped_key, bytes)
    
    unwrapped_key = unwrap_symmetric_key(wrapped_key, private_key)
    assert unwrapped_key == fernet_key