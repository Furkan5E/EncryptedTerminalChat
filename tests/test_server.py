import pytest
from unittest.mock import MagicMock
from src.server import broadcast

def test_broadcast_sends_to_other_clients():
    #mock sockets
    sender = MagicMock()
    client2 = MagicMock()
    client3 = MagicMock()
    
    #simulate server's active connection pool
    active_clients = [sender, client2, client3]
    message = b"encrypted_network_payload"
    
    #execute broadcast function
    broadcast(message, sender, active_clients)
    
    #sender should not receive their own message back
    sender.send.assert_not_called()
    
    #other clients must receive the exact byte payload
    client2.send.assert_called_once_with(message)
    client3.send.assert_called_once_with(message)