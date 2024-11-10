from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from flask import Flask, request, jsonify

app = Flask(__name__)

def decrypt_data(encrypted_data, key):
    try:
        # Ensure that encrypted_data is in bytes and not a dictionary
        ciphertext = encrypted_data['ciphertext']
        cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')
    except ValueError as e:
        return f"Padding Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging line to check the incoming data

        # Convert hex value back to bytes
        ciphertext = bytes.fromhex(data['ciphertext'])

        # Use the same key as the sender
        shared_key = b'Sixteen byte key'  # Ensure it matches the sender's key

        # Decrypt the data
        decrypted_message = decrypt_data({'ciphertext': ciphertext}, shared_key)

        # Log the decrypted message for debugging
        print("Decrypted message:", decrypted_message)

        if "Error" in decrypted_message:
            return jsonify({"error": decrypted_message}), 500

        return jsonify({"message": decrypted_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
