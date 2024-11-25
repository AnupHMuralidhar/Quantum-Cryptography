import base64
import requests
from bb84 import bb84_key_exchange  # Ensure bb84.py is in the same directory or the correct import path is used
from custom_aes import encrypt, decrypt  # Import encrypt and decrypt functions from custom_aes.py


class QuantumAES:
    def __init__(self, key):
        """
        Initialize QuantumAES with a given shared key.
        :param key: A 16-byte shared key for AES encryption.
        """
        self.key = key

    def encrypt_text(self, plain_text):
        """
        Encrypt the plain text using custom AES and encode it in Base64.
        :param plain_text: The text to encrypt.
        :return: Base64 encoded ciphertext.
        """
        ciphertext = encrypt(plain_text, self.key)
        encrypted_data = base64.b64encode(ciphertext).decode('utf-8')
        return encrypted_data


def main():
    # Generate the shared key via BB84 protocol
    shared_key = bb84_key_exchange()
    print("Sender Shared Key:", shared_key.hex())  # Print the shared key in hex format

    # Ensure key length is 16 bytes for AES (truncate or pad if necessary)
    if len(shared_key) != 16:
        shared_key = shared_key[:16]

    # Create the AES object with the shared key
    aes = QuantumAES(shared_key)

    # Encrypt the message
    text_to_encrypt = "This is a test message with custom AES and BB84"
    encrypted_text = aes.encrypt_text(text_to_encrypt)
    print("Encrypted text (Base64):", encrypted_text)

    # Send encrypted data to receiver
    receiver_url = "https://4593-2401-4900-1cbc-5612-4181-42b5-46e0-d042.ngrok-free.app/receive"  # Replace with actual receiver endpoint
    try:
        response = requests.post(receiver_url, json={"ciphertext": encrypted_text})
        print("Response from Receiver:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data:", str(e))


if __name__ == "__main__":
    main()
