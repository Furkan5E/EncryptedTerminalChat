import socket
import threading
import argparse
import os
import sys
from dotenv import load_dotenv
from src.cipher import encrypt_message, decrypt_message

def parse_arguments():
    """Parses command line arguments for host and port configuration."""
    parser = argparse.ArgumentParser(description="Secure TCP Chat Client")
    parser.add_argument("--host", type=str, default="localhost", help="Server IP address")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    return parser.parse_args()

def load_key():
    """Loads the cryptographic key securely from the environment variables."""
    load_dotenv()
    key = os.getenv("SHARED_KEY")
    if not key:
        raise ValueError("SHARED_KEY environment variable not set")
    #fernet requires key as bytes
    return key.encode('utf-8')

def receive_messages(client_socket, key):
    """Listens for incoming network payloads and decrypts them."""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("\n[System] Server closed the connection.")
                os._exit(0)
            
            decrypted_message = decrypt_message(message, key)
            print(f"\r{decrypted_message}\nYou: ", end="")
        except Exception:
            print("\n[System] Connection to server lost.")
            os._exit(0)

def start_client():
    """Initializes the secure client connection and I/O threads."""
    try:
        args = parse_arguments()
        key = load_key()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((args.host, args.port))
        print(f"Connected to secure chat server at {args.host}:{args.port}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

    username = input("Enter your username: ").strip()
    if not username:
        username = "Anonymous"

    #start receiving process in background thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, key), daemon=True)
    receive_thread.start()
    print("Type your messages below. Type 'exit' to quit.")
    
    try:
        #main loop
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                break
            
            full_message = f"[{username}]: {message}"
            encrypted_msg = encrypt_message(full_message, key)
            client_socket.send(encrypted_msg)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n error: {e}")
    finally:
        client_socket.close()
        os._exit(0)

if __name__ == "__main__":
    start_client()