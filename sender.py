from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests

class QuantumAES:
    def __init__(self, key):
        self.key = self.pad_key(key)

    def pad_key(self, key):
        """Pad or truncate the key to ensure it's 128 bits (16 bytes)"""
        key = key[:16]  # Truncate if longer than 16 bytes
        key = key.ljust(16, '0')  # Pad with zeros if shorter than 16 bytes
        return key.encode()  # Ensure the key is in bytes format

    def encrypt_text(self, plain_text):
        """Encrypt the plain text with AES using ECB mode"""
        cipher = AES.new(self.key, AES.MODE_ECB)  # Using ECB mode
        padded_text = pad(plain_text.encode(), AES.block_size)  # Pad text to block size
        ciphertext = cipher.encrypt(padded_text)
        return ciphertext

# Example to use the QuantumAES class
quantum_key = 'Sixteen byte key'  # Ensure this key matches on both ends
aes = QuantumAES(quantum_key)

# Sample text to encrypt
text_to_encrypt = "This is a Longer Message"
print(f"Encrypting the text message: {text_to_encrypt}")

# Encrypt the text message
ciphertext = aes.encrypt_text(text_to_encrypt)

# Show the ciphertext in hexadecimal format
print(f"Ciphertext (hex): {ciphertext.hex()}")

# Send encrypted data via POST
receiver_url = "https://URLFROMNGROK/receive"
message = {
    "ciphertext": ciphertext.hex(),  # Send as hex to avoid transmission issues
}

# Sending request to the receiver
response = requests.post(receiver_url, json=message)

# Output the response from the receiver
print("Response from Receiver:", response.text)
