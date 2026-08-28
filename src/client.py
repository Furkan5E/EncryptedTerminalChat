import socket
import threading
import argparse
import os
import sys
import re
from src.cipher import (
    encrypt_message, decrypt_message, generate_key,
    generate_rsa_keypair, serialise_public_key,
    deserialise_public_key, wrap_symmetric_key, unwrap_symmetric_key
)
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def parse_arguments():
    """Parses command line arguments for host, port, and handshake mode."""
    parser = argparse.ArgumentParser(description="Secure TCP Chat Client")
    parser.add_argument("--host", type=str, default="localhost", help="Server IP address")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--mode", type=str, choices=["host", "join"], required=True, help="Set to 'host' for the first user, 'join' for the second.")
    return parser.parse_args()

def perform_handshake(client_socket, mode):
    """Executes the RSA key exchange to securely negotiate a symmetric key."""
    print("\n[System] Initiating cryptographic handshake...")
    
    if mode == "host":
        private_key, public_key = generate_rsa_keypair()
        pem_bytes = serialise_public_key(public_key)
        
        client_socket.send(pem_bytes)
        print("[System] Public key broadcasted. Waiting for symmetric key...")
        
        wrapped_key = client_socket.recv(1024)
        if not wrapped_key:
            raise ConnectionError("Server closed connection during handshake.")
            
        fernet_key = unwrap_symmetric_key(wrapped_key, private_key)
        print("[System] Symmetric key received and unwrapped securely.\n")
        return fernet_key
        
    elif mode == "join":
        print("[System] Waiting for host public key...")
        pem_bytes = client_socket.recv(1024)
        if not pem_bytes:
            raise ConnectionError("Server closed connection during handshake.")
            
        public_key = deserialise_public_key(pem_bytes)
        print("[System] Public key received.")
        
        fernet_key = generate_key()
        wrapped_key = wrap_symmetric_key(fernet_key, public_key)
        
        client_socket.send(wrapped_key)
        print("[System] Symmetric key generated, wrapped, and sent.\n")
        return fernet_key

def receive_messages(client_socket, key):
    """Listens for incoming network payloads, buffers them, and decrypts them."""
    buffer = b""
    while True:
        try:
            chunk = client_socket.recv(1024)
            if not chunk:
                print("\n[System] Server closed the connection.")
                os._exit(0)
            
            buffer += chunk
            
            #process messages in buffer
            while b"<END>" in buffer:
                message_bytes, buffer = buffer.split(b"<END>", 1)
                decrypted_message = decrypt_message(message_bytes, key)
                decrypted_message = ANSI_ESCAPE.sub('', decrypted_message) #sanitise string
                print(f"\r\033[2K{decrypted_message}\nYou: ", end="", flush=True)
                
        except Exception as e:
            print(f"\n[System] Client error: {e}")
            os._exit(0)

def start_client():
    """Initialises the secure client connection and I/O threads."""
    args = parse_arguments()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((args.host, args.port))
        print(f"Connected to secure chat server at {args.host}:{args.port}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

    try:
        shared_key = perform_handshake(client_socket, args.mode)
    except Exception as e:
        print(f"Handshake failed: {e}")
        client_socket.close()
        sys.exit(1)

    username = input("Enter your username: ").strip()
    if not username:
        username = "Anonymous"

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, shared_key), daemon=True)
    receive_thread.start()
    print("Type your messages below. Type 'exit' to quit.")
    
    try:
        #main loop
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                break
            
            full_message = f"{username}: {message}"
            encrypted_msg = encrypt_message(full_message, shared_key)

            #append framing delimiter before sending tcp stream
            client_socket.send(encrypted_msg + b"<END>")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n error: {e}")
    finally:
        client_socket.close()
        os._exit(0)

if __name__ == "__main__":
    start_client()