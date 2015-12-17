#!/usr/bin/python

import sys
import base64
from Crypto.Cipher import AES


# Encryption Decryption using ECB (Electronic Code block)

# Encryption

encryption_suite = AES.new('Thisisakey123456', AES.MODE_ECB)
message = 'your message to be encrypted'.rjust(32)
cipher_text = encryption_suite.encrypt(message)

#print(cipher_text)

e_b64_cipher_text = base64.b64encode(cipher_text)

print e_b64_cipher_text




# Decryption

d_b64_cipher_text = base64.b64decode(e_b64_cipher_text)

decryption_suite = AES.new('Thisisakey123456', AES.MODE_ECB)

plain_text = decryption_suite.decrypt(d_b64_cipher_text)

print plain_text

strip_plain_text =  plain_text.strip()

print strip_plain_text

