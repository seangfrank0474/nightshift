#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cipher and encodeing for Night Shift communication

import base64
import os
import sys
import hashlib

from Crypto.Cipher import AES
from nightshift_dga import NightShift_DGA

class NightShift_Cipher():
	
    def _getcipher(self):
        key_var = "key"
        get_key = NightShift_DGA()
        enc_key = get_key.ns_dga_algorithm(key_var)
        #enc_key = 'TEST-hMP#rgzt4!*EL7#psC@pgayB!G3'
	enc_key = bytes(enc_key, 'utf-8')
        cipher = AES.new(enc_key, AES.MODE_ECB)
        blksz = 16
        padding = '{'
        pad = lambda s: s + (blksz - len(s) % blksz) * padding
        return cipher, pad, padding
    
    def encrypt(self,clear_text):
	get_cipher = self._getcipher()
        cipher = get_cipher[0]
        pad = get_cipher[1]
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s).encode('utf-8'))).decode('ascii')
        encoded = EncodeAES(cipher, clear_text)
        return encoded
    
    def decrypt(self,enc_passwd):
	get_cipher = self._getcipher()
        cipher = get_cipher[0]
        padding = get_cipher[2]
        DecodeAES = lambda c, b: c.decrypt(base64.b64decode(bytes(b, 'utf-8'))).decode('ascii').rstrip(padding)
        decoded = DecodeAES(cipher, enc_passwd)
        return decoded

    def hash_keys_hosts(self,keys_hosts):
        host_hash = hashlib.sha256(keys_hosts.encode('utf-8')).hexdigest()
        return host_hash

    def run(self):
        if sys.argv[1] == '-e':
            clear_text = str(sys.argv[2])
            e_d_passwd = self.encrypt(clear_text)
            return e_d_passwd
        elif sys.argv[1] == '-d':
            enc_passwd = str(sys.argv[2])
            e_d_passwd = self.decrypt(enc_passwd)
            return e_d_passwd
        elif sys.argv[1] == '-h':
            keys_hosts = str(sys.argv[2])
            e_d_passwd = self.hash_keys_hosts(keys_hosts)
            return e_d_passwd
        else:
            print('-e <string> to encrypt\n-d <encrypted string> to decrypt\n-i <hostname+ostype> (i.e. examplehostposix or examplehostnt or output key from nightshift_dga.py)')
            sys.exit(1)
				
if __name__ == "__main__":
    if len(sys.argv) > 1:
        e_d_output = NightShift_Cipher().run()
        print('Here is the encoded/decoded string/host id - {0}'.format(e_d_output))
        sys.exit(0)
    else:
        print('-e <string> to encrypt\n-d <encrypted string> to decrypt\n-h <hostname+ostype or DGA key> (i.e. examplehostposix or examplehostnt or output key from nightshift_dga.py)')
        sys.exit(1)
