from Crypto.Cipher import AES
from flask import Flask, request, jsonify
import base64
from bb84 import bb84_key_exchange

app = Flask(__name__)

def decrypt_data(encrypted_data, key):
    try:
        # Decode from base64 and separate nonce, tag, ciphertext
        encrypted_data = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

        # Initialize AES decryption with nonce
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        print("Decrypting with key:", key.hex())  # Print the shared key in hex format for verification
        decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
        print("Decryption successful! Message:", decrypted_text.decode('utf-8'))  # Print decrypted message
        return decrypted_text.decode('utf-8')

    except ValueError as e:
        return f"Decryption Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext')

        # Generate shared key using BB84
        shared_key = bb84_key_exchange()
        print("Receiver Shared Key:", shared_key.hex())  # Print the shared key in hex format for verification

        # Ensure key length is 16 bytes for AES
        if len(shared_key) != 16:
            shared_key = shared_key[:16]

        # Decrypt using AES-GCM
        print("Decrypting...")
        decrypted_message = decrypt_data(ciphertext, shared_key)
        if "Error" in decrypted_message:
            return jsonify({"error": decrypted_message}), 500

        return jsonify({"message": decrypted_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
