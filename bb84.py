import random

def bb84_key_exchange():
    random.seed(42)  # Fixed seed for testing; replace for real deployment
    bits = [random.randint(0, 1) for _ in range(128)]
    key_bytes = bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, 128, 8))
    return key_bytes[:16]  # Ensure a 16-byte (128-bit) key for AES
