from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import requests
from bb84 import bb84_key_exchange

class QuantumAES:
    def __init__(self, key):
        self.key = key

    def encrypt_text(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
        
        # Concatenate nonce, tag, and ciphertext, then encode in base64 for transmission
        encrypted_data = base64.b64encode(nonce + tag + ciphertext).decode('utf-8')
        return encrypted_data

# Generate the shared key via BB84 protocol
shared_key = bb84_key_exchange()
print("Sender Shared Key:", shared_key.hex())  # Print the shared key in hex format

# Ensure key length is 16 bytes for AES
if len(shared_key) != 16:
    shared_key = shared_key[:16]

# Create the AES object with the shared key
aes = QuantumAES(shared_key)

# Encrypt the message
text_to_encrypt = "This is a test message with AES and BB84"
encrypted_text = aes.encrypt_text(text_to_encrypt)
print("Encrypted text:", encrypted_text)

# Send encrypted data to receiver
receiver_url = "NGROKURL/receive"  
response = requests.post(receiver_url, json={"ciphertext": encrypted_text})
print("Response from Receiver:", response.text)
