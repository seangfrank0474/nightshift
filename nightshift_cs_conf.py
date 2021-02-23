#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

try:
    while True:
        ns_c_config_path = "ns_c_config.json"
        ns_s_config_path = "ns_s_config.json"
        ns_cs_init_uri = str(input('Enter initial communication test URI - (default=/init/comms): ') or '/init/comms')
        ns_cs_init_uri_p = str(input('Enter initial client data post URI - (default=/init/comms/post): ') or '/init/comms/post')
        ns_cs_fof_uri = str(input('Enter 404 command communication URI - (default=/fof/commands): ') or '/fof/commands')
        ns_cs_data_uri_p = str(input('Enter command data output post URI - (default=/command/output): ') or '/command/output')
        ns_cs_get_ua = str(input('Enter a user agent string to be used for get methods - (default=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68): ') or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68')
        ns_cs_post_ua = str(input('Enter a user agent string to be used for post methods - (default=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68): ') or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68')
        ns_cs_listen_port = str(input('Enter port nightshift server will listen on - (default=80): ') or '80')
        ns_s_url_redirect = str(input('Enter false redirect URLs - Server Only - (default=https://en.wikipedia.org/wiki/Botnet#Command_and_control): ') or 'https://en.wikipedia.org/wiki/Botnet#Command_and_control')
        ns_c_fqdn_ip = str(input('Enter the FQDN, IP, or DGA - Client Only - (default=DGA - currently unavailable so please enter FQDN or IP)\nexample FQDN - www.example.com\nexample IP - 1.1.1.1: '))
        ns_init_site_complt = 'http://' + ns_c_fqdn_ip + ':' + ns_cs_listen_port + ns_cs_init_uri
        ns_initp_site_complt = 'http://' + ns_c_fqdn_ip + ':' +ns_cs_listen_port + ns_cs_init_uri_p
        ns_fof_site_complt = 'http://' + ns_c_fqdn_ip + ':' + ns_cs_listen_port + ns_cs_fof_uri
        ns_datap_site_complt = 'http://' + ns_c_fqdn_ip + ':' + ns_cs_listen_port + ns_cs_data_uri_p
        ns_c_config_w = { "ns_init_site": ns_init_site_complt, "ns_init_site_p": ns_initp_site_complt, "ns_fof_site": ns_fof_site_complt, "ns_post_site": ns_datap_site_complt, "ns_get_ua": ns_cs_get_ua, "ns_post_ua": ns_cs_post_ua }
        ns_s_config_w = { "ns_init_suri": ns_cs_init_uri, "ns_init_surip": ns_cs_init_uri_p, "ns_fof_suri": ns_cs_fof_uri, "ns_post_suri": ns_cs_data_uri_p, "ns_get_ua": ns_cs_get_ua, "ns_post_ua": ns_cs_post_ua, "ns_aiohttp_lp": int(ns_cs_listen_port), "ns_redirect_url": ns_s_url_redirect }
        with open(ns_c_config_path, 'w') as ns_cconfig_w:
            json.dump(ns_c_config_w, ns_cconfig_w)
        ns_cconfig_w.close()
        with open(ns_s_config_path, 'w') as ns_sconfig_w:
            json.dump(ns_s_config_w, ns_sconfig_w)
        ns_sconfig_w.close()
        ns_exit_cmd = str(input('Do you want to exit (Y/N) default - N: ') or 'N')
        if ns_exit_cmd == 'N':
            continue
        else:
            print('Exiting NighShit Command')
            break
except KeyboardInterrupt:
    print('\nInterrupted - NightShift Command exited due to a keyboard interrupt.')
sys.exit(0)
