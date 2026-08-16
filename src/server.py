import socket
import threading

active_clients = [] #list of active client sockets

def broadcast(message, sender_socket, clients_list):
    """Sends a raw byte message to all connected clients except the sender."""
    for client in clients_list:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception:
                #if sending fails assume client disconnected
                pass

def handle_client(client_socket):
    """Listens for incoming messages from a specific client and broadcasts them."""
    while True:
        try:
            #receive encrypted bytes
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket, active_clients)
        except Exception:
            break
            
    #clean up on disconnect
    if client_socket in active_clients:
        active_clients.remove(client_socket)
    client_socket.close()

def start_server(host='localhost', port=8080):
    """Initialises the TCP server and accepts incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Secure Chat Server listening on {host}:{port}...")

    while True:
        try:
            client_socket, address = server.accept()
            print(f"Connected with {address}")
            
            active_clients.append(client_socket)
            
            #new thread for new client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")
            
    server.close()

if __name__ == "__main__":
    start_server()