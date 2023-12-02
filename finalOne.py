import os

# Generate a 256-bit random key
key_bytes = os.urandom(32)

# Convert the key to a hexadecimal string
key_hex = key_bytes.hex()

print("Generated 256-bit hexadecimal key:", key_hex)
