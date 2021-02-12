#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

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
sys.exit(0)
