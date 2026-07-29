from cryptography.fernet import Fernet, InvalidToken

key = Fernet.generate_key()
cipher = Fernet(key)

sensitive = b"Credit card: 1234-5678-9012-3456"
encrypted = cipher.encrypt(sensitive)
print(f"Key: {key}")
print(f"Encrypted: {encrypted}")

decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

wrong_key = Fernet.generate_key()
wrong_cipher = Fernet(wrong_key)

try:
    wrong_cipher.decrypt(encrypted)
except InvalidToken:
    print("Decryption failed with wrong key")
