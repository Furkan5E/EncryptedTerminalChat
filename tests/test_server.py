import pytest
from unittest.mock import MagicMock, patch
from src.server import handle_client, clients, ready_event

def test_handle_client_routes_messages():
    #reset global server state for test isolation
    clients.clear()
    ready_event.set()
    
    #mock sockets
    sender = MagicMock()
    client2 = MagicMock()
    client3 = MagicMock()
    
    #simulate server's active connection pool
    clients.extend([sender, client2, client3])
    message = b"encrypted_network_payload"
    
    #simulate sender sending a message then disconnecting
    sender.recv.side_effect = [message, b""]
    
    #execute network routing handler safely
    with patch("os._exit"):
        handle_client(sender, ("127.0.0.1", 9999))
    
    #sender should not receive their own message back
    sender.send.assert_not_called()
    
    #other clients must receive the exact byte payload
    client2.send.assert_called_once_with(message)
    client3.send.assert_called_once_with(message)