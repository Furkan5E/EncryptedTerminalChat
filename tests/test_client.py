import pytest
from unittest.mock import patch
from src.client import parse_arguments

def test_parse_arguments():
    #simulate user typing
    test_args = ["client.py", "--host", "192.168.1.10", "--port", "9090", "--mode", "host"]
    
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.host == "192.168.1.10"
        assert args.port == 9090
        assert args.mode == "host"