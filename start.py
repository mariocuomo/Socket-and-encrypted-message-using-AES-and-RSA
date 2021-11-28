import base64
import logging
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Cipher import AES

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import random


#=========================================================
#        GENERATE PUBLIC AND PRIVATE KEY PAIR
#=========================================================
print('Generating new keypair...')

# GENERATE NEW KEYPAIR 
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
public_key = private_key.public_key()

pem = private_key.private_bytes(
	encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

with open('private_key.pem', 'wb') as f:
    f.write(pem)

pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
with open('public_key.pem', 'wb') as f:
    f.write(pem)
print('Generated /public_key.pem && /private_key.pem file\n\n')



#=========================================================
#             GENERATE COMMON SECRET
#=========================================================
print('Generating new shared secret...')

data="SECRETDATA"
data=bytes(data,'UTF-8')

key=''
for _ in range(16):
    random_integer = random.randint(97, 97 + 26 - 1)
    flip_bit = random.randint(0, 1)
    random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    key += (chr(random_integer))

iv = ''
for _ in range(16):
    random_integer = random.randint(97, 97 + 26 - 1)
    flip_bit = random.randint(0, 1)
    random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    iv += (chr(random_integer))


with open("commonSecret.text", "w") as f:
    k_i=[key,iv]
    f.writelines("%s\n" % l for l in k_i)

print('Generated /commonSecret.text file\n\n')

print('=======================\n\tDONE!\n=======================')
