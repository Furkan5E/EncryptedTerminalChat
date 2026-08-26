import socket
import threading
import os

clients = [] #list of active client sockets
ready_event = threading.Event()

def handle_client(client_socket, address):
    """Blocks until both clients are present, then routes incoming traffic."""
    ready_event.wait()
    
    while True:
        try:
            #receive encrypted bytes
            message = client_socket.recv(1024)
            if not message:
                break
            
            for client in clients:
                if client != client_socket:
                    client.send(message)
        except Exception:
            break
    #clean up on disconnect  
    print(f"\nConnection lost with {address}. Shutting down session.")
    client_socket.close()
    os._exit(0)

def start_server(host="localhost", port=8080):
    """Initialises the server and waits for exactly two connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(2)
    
    print(f"Secure Chat Server listening on {host}:{port}...")
    print("Waiting for exactly two clients to connect before routing traffic...")
    
    try:
        while len(clients) < 2:
            client_socket, address = server.accept()
            print(f"Connected with {address}")
            clients.append(client_socket)
            #new thread for new client
            thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
            thread.start()
            
        print("Both clients connected. Unlocking network routing.")
        ready_event.set()
        
        while True:
            pass
            
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        os._exit(0)

if __name__ == "__main__":
    start_server()