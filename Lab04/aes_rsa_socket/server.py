from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients (socket, aes_key) tuples
clients = []

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    
    
    # Key exchange
    client_socket.send(server_key.publickey().export_key(format='PEM'))
    client_public_key = RSA.import_key(client_socket.recv(2048))
        
    # Generate and send AES key
    aes_key = get_random_bytes(16)
    encrypted_aes_key = PKCS1_OAEP.new(client_public_key).encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    clients.append((client_socket, aes_key))
        
    while True:
        encrypted_message = client_socket.recv(1024)
        decrypted_message = decrypt_message(aes_key, encrypted_message)
        print(f"Received from {client_address}: {decrypted_message}")
        for client, key in clients:
            if client != client_socket:
                encrypted = encrypt_message(key, decrypted_message)
                client.send(encrypted)

        if decrypted_message == "exit":
            break
    clients.remove((client_socket,aes_key))
    client_socket.close()
    print(f"Connection with {client_address} closed")
    
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
    client_thread.start()
        