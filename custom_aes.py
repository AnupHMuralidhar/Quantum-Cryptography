import os
from typing import List

# Block size for AES encryption
BLOCK_SIZE = 16

# S-Box for AES Substitution
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]


def pad(plaintext: bytes) -> bytes:
    """
    Add padding to the plaintext to make its length a multiple of the block size.
    """
    padding_length = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    padding = bytes([padding_length] * padding_length)
    return plaintext + padding

def unpad(plaintext: bytes) -> bytes:
    """
    Remove padding from the plaintext.
    """
    padding_length = plaintext[-1]
    return plaintext[:-padding_length]

def add_round_key(state: List[int], key: List[int]) -> List[int]:
    """
    Perform the AddRoundKey step: XOR the state with the round key.
    """
    return [state[i] ^ key[i] for i in range(len(state))]

def sub_bytes(state: List[int]) -> List[int]:
    """
    Perform the SubBytes step using the AES S-Box.
    """
    return [S_BOX[b] for b in state]

def shift_rows(state: List[int]) -> List[int]:
    """
    Perform the ShiftRows step to permute the rows of the state.
    """
    return [
        state[0], state[5], state[10], state[15],  # Row 0
        state[4], state[9], state[14], state[3],  # Row 1
        state[8], state[13], state[2], state[7],  # Row 2
        state[12], state[1], state[6], state[11],  # Row 3
    ]

def encrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Encrypt a single 16-byte block using AES-like steps.
    """
    state = list(block)
    key_schedule = list(key)  # Simplified: static key as the round key

    # Initial round: AddRoundKey
    state = add_round_key(state, key_schedule)

    # Main rounds (simplified to 1 round for this example)
    state = sub_bytes(state)  # SubBytes
    state = shift_rows(state)  # ShiftRows
    state = add_round_key(state, key_schedule)  # AddRoundKey again

    return bytes(state)

def decrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Decrypt a single 16-byte block using the reverse of AES steps.
    """
    state = list(block)
    key_schedule = list(key)  # Simplified: static key as the round key

    # Reverse main round
    state = add_round_key(state, key_schedule)  # AddRoundKey
    # Reverse ShiftRows
    state = [
        state[0], state[13], state[10], state[7],
        state[4], state[1], state[14], state[11],
        state[8], state[5], state[2], state[15],
        state[12], state[9], state[6], state[3],
    ]
    # Reverse SubBytes
    inv_s_box = {v: k for k, v in enumerate(S_BOX)}
    state = [inv_s_box[b] for b in state]

    # Reverse initial round: AddRoundKey
    state = add_round_key(state, key_schedule)

    return bytes(state)

def encrypt(plaintext: str, key: bytes) -> bytes:
    """
    Encrypt the plaintext using the custom AES.
    """
    plaintext_bytes = pad(plaintext.encode())
    ciphertext = b""
    for i in range(0, len(plaintext_bytes), BLOCK_SIZE):
        block = plaintext_bytes[i:i+BLOCK_SIZE]
        ciphertext += encrypt_block(block, key)
    return ciphertext

def decrypt(ciphertext: bytes, key: bytes) -> str:
    """
    Decrypt the ciphertext using the custom AES.
    """
    plaintext = b""
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        plaintext += decrypt_block(block, key)
    return unpad(plaintext).decode()

# Test the implementation
if __name__ == "__main__":
    key = os.urandom(16)  # Random 16-byte key
    plaintext = "Hello, AES! This is a test."

    print("Original plaintext:", plaintext)

    ciphertext = encrypt(plaintext, key)
    print("Ciphertext (hex):", ciphertext.hex())

    decrypted_text = decrypt(ciphertext, key)
    print("Decrypted text:", decrypted_text)
