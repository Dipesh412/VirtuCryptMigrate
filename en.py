from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def pad_data(data):
    block_size = 16  # AES block size is 128 bits or 16 bytes
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size] * padding_size)
    return data + padding

def unpad_data(data):
    padding_size = data[-1]
    if padding_size > 0 and padding_size <= 16:
        return data[:-padding_size]
    return data

def encrypt_file(input_file,key):
    with open(input_file, 'rb') as file:
        data = file.read()
    data = pad_data(data)
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv+encrypted_data
    # with open(output_file, 'wb') as file:
    #     file.write(iv + encrypted_data)

def decrypt_file(input_file,key):
    with open(input_file, 'rb') as file:
        data = file.read()
    iv = data[:16]  # Extract IV from the beginning of the file
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpad_data(decrypted_data)
    return decrypted_data
    # with open(output_file, 'wb') as file:
    #     file.write(decrypted_data)

# Example usage
# if __name__ == "__main__":
#     input_file = 'input.txt'  # Replace with the path to your input file
#     encrypted_file = 'encrypted_file.enc'  # Replace with the desired encrypted output file path
#     decrypted_file = 'decrypted_file.txt'  # Replace with the desired decrypted output file path

#     key_str = input("Enter the 256-bit encryption key (hexadecimal): ")
#     key = bytes.fromhex(key_str)

#     # encrypt_file(input_file, encrypted_file, key)
#     # print(f'File "{input_file}" encrypted and saved as "{encrypted_file}"')

#     decrypt_file(encrypted_file, decrypted_file, key)
#     print(f'File "{encrypted_file}" decrypted and saved as "{decrypted_file}"')
