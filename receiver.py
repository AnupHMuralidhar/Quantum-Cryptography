from flask import Flask, request, jsonify
import base64
from bb84 import bb84_key_exchange
from custom_aes import encrypt, decrypt

app = Flask(__name__)

def decrypt_data(encrypted_data, key):
    try:
        # Decode from Base64
        encrypted_data = base64.b64decode(encrypted_data)

        # Use custom AES decryption
        aes = decrypt(encrypted_data,key)
        decrypted_text = decrypt(encrypted_data,key)

        print("Decryption successful! Message:", decrypted_text)
        return decrypted_text

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

        # Decrypt using custom AES
        print("Decrypting...")
        decrypted_message = decrypt_data(ciphertext, shared_key)
        if "Error" in decrypted_message:
            return jsonify({"error": decrypted_message}), 500

        return jsonify({"message": decrypted_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
