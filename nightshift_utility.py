#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cipher and DGA Key Generation.

import base64
import ctypes
import os
import sys
import hashlib
import time

from Crypto.Cipher import AES
from datetime import date

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

class NightShift_DGA():
    def _ns_month_seed(self):
        mnthseed = {
            '01': '15789139',
            '02': '19871027',
            '03': '15109199',
            '04': '15709067',
            '05': '16789399',
            '06': '17803147',
            '07': '15499409',
            '08': '14901327',
            '09': '10976489',
            '10': '15499357',
            '11': '15499499',
            '12': '15499387'
            }
        return mnthseed
    
    def ns_dga_algorithm(self,key_domain):
        if key_domain == 'key':
            init_i = 32
            idx = 256
        elif key_domain == 'domain':
            init_i = 16
            idx = 128
        today_tuple = date.today()
        tday_list = str(today_tuple).split('-')
        cur_day = tday_list[2]
        cur_month = tday_list[1]
        cur_year = tday_list[0]
        today_str = '{0}{1}{2}'.format(cur_year, cur_month, cur_day)
        dict_m_seed = self._ns_month_seed()[cur_month]
        t_seed = int(today_str)
        m_seed = int(dict_m_seed)
        init_seed = t_seed + m_seed
        domains = ""
        domain = []
        for i in range(init_i):
            seed = (idx + i + ((init_seed >> 0x18) & 0xff | (init_seed << 0x8)) + 0x65BA0642) & 0xffffffff
            s_seed = ctypes.c_int(seed).value
            domain.append(chr((abs(s_seed) % 0x19) + ord("a")))
        domain = "".join(domain)
        domains = domain 
        return domains
        
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == '--dga' and sys.argv[2] in ('key','domain'):
                key_domain = sys.argv[2]
                nsutil_output = NightShift_DGA().ns_dga_algorithm(key_domain) 
                print('Here is the DGA {0} string you requested - {1}'.format(key_domain,nsutil_output))
            if sys.argv[1] == '--cipher' and sys.argv[2] in ('-e','-d','-h'): 
                if sys.argv[2] == '-e':
                    ns_encmode = 'encrypted'
                    ns_encrypt = str(sys.argv[3])
                    nsutil_output = NightShift_Cipher().encrypt(ns_encrypt)
                if sys.argv[2] == '-d':
                    ns_encmode = 'decrypted'
                    ns_encrypt = str(sys.argv[3])
                    nsutil_output = NightShift_Cipher().decrypt(ns_encrypt)
                if sys.argv[2] == '-h':
                    ns_encmode = 'hashed'
                    ns_encrypt = str(sys.argv[3])
                    nsutil_output = NightShift_Cipher().hash_keys_hosts(ns_encrypt)
                print('Here is the {0} string/host id - {1}'.format(ns_encmode,nsutil_output))
    except:
        print('Whoops something went wrong, please try again! ¯\_(``)_/¯')
        print('Usage for DGA:\npython3 nightshift_utility.py --dga key (to generate comms key)\npython3 nightshift_utility.py --dga domain (to generate dga domain)')
        print('Usage for Cipher:\npython3 nightshift_utility.py --cipher -e <string> to encrypt\npython3 nightshift_utility.py --cipher -d <encrypted string> to decrypt\npython3 nightshift_utility.py --cipher -h <the thing you want to hash> (i.e. examplehostposix or examplehostnt or output dga key)')
        sys.exit(1)
    sys.exit(0)
