# Encrypted Terminal Chat

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Build](https://img.shields.io/badge/Build-uv-purple.svg)
![Licence](https://img.shields.io/badge/Licence-MIT-blue?style=flat-square)
[![Test Suite](https://github.com/Furkan5E/EncryptedTerminalChat/actions/workflows/test.yaml/badge.svg)](https://github.com/Furkan5E/EncryptedTerminalChat/actions/workflows/test.yaml)

A secure, end-to-end encrypted terminal chat network featuring ephemeral keys and robust message sanitisation. Built strictly with Python and managed via `uv` for seamless local execution.

## Architecture

![Demo](docs/demo.gif)
The application operates on a lightweight client-server model:

| Component | Purpose |
|---|---|
| **Relay Server** | A headless network relay requiring a single exposed port to manage routing without retaining message data. |
| **Terminal Client** | An interactive, native terminal application handling end-to-end encryption, ephemeral key generation, and raw ANSI rendering. |

## Key Features

* **Server Blind Encryption:** Messages are encrypted locally, ensuring the relay server cannot intercept or store communication.
* **Cryptographic Primitives:** Uses asymmetric key exchange for session negotiation and AES-GCM for secure message encryption.
* **Terminal Injection Protection:** Input sanitisation prevents malicious escape sequences or shell commands from being injected into the recipient's terminal.
* **Native Execution:** Runs directly on the host machine without Docker overhead to prevent TTY allocation friction and preserve raw terminal output.
* **Deterministic Dependencies:** Cryptography modules and environments are completely isolated and locked using `pyproject.toml` and `uv.lock`.

## Installation

Clone the repository and install the dependencies:
```bash
git clone https://github.com/Furkan5E/EncryptedTerminalChat.git
cd EncryptedTerminalChat
uv sync
```
Start the relay server: 
```bash
uv run python src/server.py --port 8080
```
Launch the host client to open a room:
```bash
uv run python src/client.py --mode host --port 8080
```
Launch the joining client in a separate terminal:
```bash
uv run python src/client.py --mode join --port 8080
```
## Testing

To run the automated test suite locally:
```bash
uv run pytest
```
