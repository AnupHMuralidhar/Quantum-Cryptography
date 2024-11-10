from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad  # For secure padding
from qkd_simulation import simulate_BB84_key  # Import the simulate_BB84_key function

class QuantumAES:
    def __init__(self, key):
        # Ensure key is exactly 16 bytes long (128 bits) for AES encryption
        self.key = self.pad_key(key)

    def pad_key(self, key):
        """Pad or truncate the key to ensure it's 128 bits (16 bytes)"""
        print(f"Original Key: {key}")
        # Truncate or pad to 16 bytes
        key = key[:16]  # Truncate if the key is longer than 16 bytes
        key = key.ljust(16, '0')  # Pad with zeros if the key is shorter than 16 bytes
        return key.encode()  # Ensure the key is in bytes format

    def encrypt_text(self, plain_text):
        """Encrypt the plain text with AES using EAX mode"""
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
        print(f"Ciphertext: {ciphertext}")
        return cipher.nonce, ciphertext, tag

    def decrypt_text(self, nonce, ciphertext, tag):
        """Decrypt the ciphertext with AES using EAX mode"""
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
        print(f"Decrypted Text: {decrypted_text}")
        return decrypted_text.decode()

# Step 1: Generate Quantum Key using BB84
quantum_key = simulate_BB84_key()
if quantum_key:
    print("Quantum-secured AES encryption in progress...")

    # Step 2: Encrypt Text
    text_to_encrypt = "HALO AICHWARREYYEAAA"
    aes = QuantumAES(quantum_key)
    nonce, ciphertext, tag = aes.encrypt_text(text_to_encrypt)
    print("Encrypted Text:", ciphertext)

    # Step 3: Decrypt Text
    decrypted_text = aes.decrypt_text(nonce, ciphertext, tag)
    print("Decrypted Text:", decrypted_text)

else:
    print("Eavesdropping detected; transmission terminated.")
