Quantum Cryptographic Encryption for Text Communication

Project Description
This project demonstrates the use of quantum cryptography for secure text encryption and transmission. The key exchange process is implemented using the BB84 protocol, while the encryption and decryption of text messages are performed using AES (Advanced Encryption Standard).

The project consists of two main components
Quantum Key Distribution (QKD) using the BB84 protocol for securely exchanging encryption keys.
AES encryption for encrypting and decrypting text messages using the agreed-upon key.
The communication between the sender and receiver is simulated using a Quantum Channel for key exchange and ngrok for secure transmission over the internet.

Project Components

BB84 Protocol (bb84.py):
Implements the quantum key distribution using the BB84 protocol.
Simulates the process of transmitting quantum bits (qubits) and securely exchanging keys over an insecure channel.

AES Encryption (custom_aes.py):
AES is used to encrypt and decrypt text messages.
The encryption key used for AES is securely derived from the quantum key exchange (BB84 protocol).

Sender and Receiver Files (sender.py & receiver.py):
sender.py: Encrypts the text message using AES and sends the encrypted message over the secure channel.
receiver.py: Receives the encrypted message, decrypts it using AES, and displays the original message.

Text Transmission using ngrok:
The communication between the sender and receiver is achieved over the internet using ngrok for secure tunneling.

Technologies Used
Python 3.x: Programming language.
Cryptography: Library for AES encryption and decryption.
BB84 Protocol: Quantum Key Distribution Protocol for secure key exchange.
ngrok: Service for creating secure tunnels to localhost, allowing internet-based communication between sender and receiver.

Installation

Clone the repository:
git clone https://github.com/AnupHMuralidhar/Quantum-Cryptography.git
cd QuantumCryptographyProject

Install the required dependencies:
pip install -r requirements.txt

Run the receiver on one machine (this should also expose a port using ngrok for remote access):
ngrok http 8080
python receiver.py

Run the sender on another machine, providing the encrypted message:
python sender.py


How It Works
1. BB84 Protocol for Key Exchange
The sender and receiver use the BB84 protocol for quantum key distribution. The sender generates quantum bits (qubits) in different states and sends them to the receiver. The receiver then measures these qubits and returns a classical bit string as the key. Both parties use this shared key to encrypt and decrypt messages using AES.

2. AES Encryption
Once the key is securely shared, the sender uses the AES algorithm to encrypt a plaintext message. The encrypted message is transmitted over the network to the receiver. The receiver, using the same key derived from the BB84 protocol, decrypts the message back into its original form.

3. Secure Transmission using ngrok
To facilitate secure communication over the internet, ngrok is used to create a secure tunnel for transmitting the encrypted messages between the sender and receiver. This allows for simulation of real-world communication in a secure manner.

Example
Sender terminal:
Sender Shared Key: 2080b392eac23da1d1cba7905e6d4933
Encrypted text (Base64): suLVyp4rxFk2H/CchvZm1U7cOTK3yr2svWYdZnlg7dSkAaSxk7vCx9k3eyrCOO2G
Response from Receiver: {
  "message": "This is a test message with custom AES and BB84"
}

Receiver terminal:
Receiver Shared Key: 2080b392eac23da1d1cba7905e6d4933
Decrypting...
Decryption successful! Message: This is a test message with custom AES and BB84


Contributors
Adrian Richard Benjamin
Aishwarya S Biradar  
Anup H Muralidhar
Anusha R
