import socket
import base64
import sys
import rsa
from Crypto.Cipher import AES

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


private_key=''

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
    key_file.read(),
    backend=default_backend(),
    password=None
)

    

host = socket.gethostname()
port = 5001

client_socket = socket.socket()
client_socket.connect((host, port))

t = 0

challenge = client_socket.recv(1024).decode()
signed = private_key.sign(
    challenge.encode('utf-8'),
    padding.PSS(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
client_socket.send(signed)

answer = client_socket.recv(1024).decode()

if(answer=='0'):
    print('you are NOT authenticated from the server')
    sys.exit() 

print('you ARE authenticated from the server')


key_iv=''
with open("commonSecret.text", "r") as f:
    key_iv = f.read().splitlines()

key = key_iv[0]
iv = key_iv[1]
key=bytes(key,'UTF-8')
iv=bytes(iv,'UTF-8')


message = input('ALICE: ')


while message.lower().strip() != 'exit':
    try:
        obj = AES.new(key, AES.MODE_CFB, iv)
        message=bytes(message,'UTF-8')
        ciphertxt = obj.encrypt(message)

        client_socket.send(ciphertxt)
        client_socket.settimeout(10.0)

        data = client_socket.recv(1024)
        if not data:
            break
        obj = AES.new(key, AES.MODE_CFB, iv)
        plain_text = obj.decrypt(data).decode("utf-8") 
        t=0
        print('BOB: ' + plain_text)

        message = input("ALICE: ")
    except socket.timeout:
        t+=1
        if(t>3):
            break
        print('** No response within the expected time :( **')
        print('** Waiting for a message from the server ... ** \n')

client_socket.close()
print('The server did not respond ...')
