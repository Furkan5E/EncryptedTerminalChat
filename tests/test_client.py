import pytest
from unittest.mock import patch
from src.client import parse_arguments, load_key

def test_parse_arguments():
    #simulate user typing
    test_args = ["client.py", "--host", "192.168.1.10", "--port", "9090"]
    
    with patch('sys.argv', test_args):
        args = parse_arguments()
        assert args.host == "192.168.1.10"
        assert args.port == 9090

def test_load_key_fails_without_env_var(monkeypatch):
    monkeypatch.delenv("SHARED_KEY", raising=False)
    
    #must crash with value error if no key
    with pytest.raises(ValueError, match="SHARED_KEY environment variable not set"):
        load_key()