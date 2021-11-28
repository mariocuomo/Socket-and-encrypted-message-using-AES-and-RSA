import socket
import base64
import logging
import random
import sys
from Crypto.Cipher import AES


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


key_iv=''
with open("commonSecret.text", "r") as f:
    key_iv = f.read().splitlines()

key = key_iv[0]
iv = key_iv[1]
key=bytes(key,'UTF-8')
iv=bytes(iv,'UTF-8')


public_key=''

with open("public_key.pem", "rb") as key_file:
	public_key = serialization.load_pem_public_key(
	key_file.read(),
	backend=default_backend()
)

host = socket.gethostname()
port = 5001

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)



print('Waiting for a connection...')
conn, address = server_socket.accept()
print("Connection from: " + str(address))


#send a challenge to client
challenge = ''
 
for _ in range(100):
    random_integer = random.randint(97, 97 + 26 - 1)
    flip_bit = random.randint(0, 1)
    random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    challenge += (chr(random_integer))
conn.send(challenge.encode())

answer = conn.recv(1024)
try:
	public_key.verify(
    	signature=answer,
		data=challenge.encode('utf-8'),
		padding=padding.PSS(
		mgf=padding.MGF1(hashes.SHA256()),
		salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )
	is_signature_correct = True
	conn.send('1'.encode())
except InvalidSignature:
	is_signature_correct = False
	conn.send('0'.encode())
	sys.exit() 

obj = AES.new(key, AES.MODE_CFB, iv)

while True:
	datas = conn.recv(1024)
	plain_text = obj.decrypt(datas).decode("utf-8") 
	obj = AES.new(key, AES.MODE_CFB, iv)
	
	if not datas:
		break
	print("ALICE: " + str(plain_text))
	datas = input('BOB: ')

	datas=bytes(datas,'UTF-8')
	ciphertxt = obj.encrypt(datas)
	obj = AES.new(key, AES.MODE_CFB, iv)


	conn.send(ciphertxt)


conn.close()
