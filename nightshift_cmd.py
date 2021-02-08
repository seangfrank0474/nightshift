#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

while True:
    ns_cmd_path = "ns_404_config.json"
    host_404_w = str(input('Enter Host Hash or ALL (default ALL): ') or 'ALL')
    #print(host_404_w)
    host_os_404_w = str(input('Enter Host OS - currently available (nt/posix) (default nt): ') or 'nt')
    #print(host_os_404_w)
    host_cmd_404_w = str(input('Enter Host OS - (default sleep): ') or 'sleep')
    #print(host_cmd_404_w)
    ns_cmd_config_w = { "host_404": host_404_w, "host_os_404": host_os_404_w, "host_cmd_404": host_cmd_404_w }
    #print(ns_cmd_config_w)
    with open(ns_cmd_path, 'w') as ns_cmd_w:
        json.dump(ns_cmd_config_w, ns_cmd_w)
    ns_cmd_w.close()
    ns_exit_cmd = str(input('Do you want to exit (Y/N) default - N: ') or 'N')
    if ns_exit_cmd == 'N':
        continue
    else:
        print('Exiting NighShit Command')
        break
        
sys.exit(0)
