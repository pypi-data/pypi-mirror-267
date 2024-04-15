#!/bin/python3
from base64 import urlsafe_b64encode
import hashlib as hashlib
from cryptography.fernet import Fernet


class CryptogramAPI:
    """
    The CryptographyMethodsAPI class enscapulates methods used for keeping
    secrets in both one-way and two-way forms.

    SHA-256 is delivered in a much simpler syntax than the default method
    utilized by hashlib; the CryptographyMethods.SHA256 object merely
    requires a secret to be hashed and delivers the hexdigest of the
    resulting byte object.

    For two-way secret keeping CryptographyMethods.Encryption and
    CryptographyMethods.Decryption are offered; both of which utilize the
    CryptographyMethods.BuildKey function for locking and unlocking secrets,
    respectively.
    """



    def sha_256(self, secret: str):
      """
      Create a SHA-256 hash of whatever value is given as 'secret' and
      return the the hexdigest of the bytes-encoded secret.
      """
      return hashlib.sha256( secret.encode() )\
                    .hexdigest()
  
  
    def build_key(self, key: str):
      """
      Create a two-way encryption token using the first 32
      digits of the hash of a given string named 'key'.
    
      The results are then encoded in urlsafe-base64 bytes
      and returned to the caller.
      """
      basecode = self.sha_256( str(key) )[:32]
      return urlsafe_b64encode( basecode.encode() )
  
  
    def encryption(self, phrase: bytes, target: str):
      """
      Encrypt a 'target' string using a byte 'phrase' provided by
      CryptographyMethods.BuildKey as an encryption token.
      """
      return Fernet( phrase ).encrypt( bytes(target, 'utf-8') )
  
  
    def decryption(self, phrase: bytes, target: str):
      """
      Decrypt a 'target' string using a byte 'phrase' provided by
      CryptographyMethods.BuildKey as an encryption token.
      """
      return Fernet( phrase ).decrypt( target )\
                             .decode()


def EncryptionTest(username, password, secret):
    cryptogram = CryptogramAPI()
    key = cryptogram.build_key(f"{username}{password}")
    username = cryptogram.sha_256(username)
    password = cryptogram.sha_256(password)
    secret = cryptogram.encryption(key, secret)
    username_verification = input("Type your username: ")
    password_verification = input("Type your password: ")
    key = cryptogram.build_key(f"{username_verification}{password_verification}")
    secret = cryptogram.decryption(key, secret)
    print(f"Secret is: {secret}")
