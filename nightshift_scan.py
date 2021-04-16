#! /usr/bin/env python3

#import asyncio
import dns.message
import dns.name
import dns.rdataclass
import dns.rdatatype
import dns.resolver
import json
import logging
import random
import socket
import time
from colorama import Fore, Back, Style
from ipaddress import IPv4Network
from scapy.all import *

class NightShift_Recon():

    def run(self):
        ns_ps_results = self.ns_ping_sweep()
        ns_neib_host = ns_ps_results[0]
        ns_neib_cnt = ns_ps_results[1]
        if ns_neib_cnt > 0:
            ns_prtscn_results = self.ns_port_scan(ns_neib_host)
        else:
            print('Nothing to see here')
        print(ns_prtscn_results)
        #print(ns_neib_host)
        #print(ns_neib_cnt)

    def ns_ping_sweep(self):
        ns_cdef_iface = conf.iface
        ns_cdef_ip = get_if_addr(ns_cdef_iface)
        ns_ip_net_split = ns_cdef_ip.split(".")
        ns_net_ccidr = ns_ip_net_split[0] + '.' + ns_ip_net_split[1] + '.' + ns_ip_net_split[2] + '.0/24'
        addresses = IPv4Network(ns_net_ccidr)
        ns_neib_cnt = 0
        ns_neib_host = []
        for host in addresses:
            if (host == ns_cdef_ip or host in (addresses.network_address, addresses.broadcast_address)):
                continue
            ns_ps_resp = sr1(IP(dst=str(host))/ICMP(),timeout=1,verbose=0)
            if ns_ps_resp is None:
                continue
                #print(f"{host} is down or not responding.")
            elif (int(ns_ps_resp.getlayer(ICMP).type)==3 and int(ns_ps_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                continue
                #print(f"{host} is blocking ICMP.")
            else:
                #print(f"{host} is responding.")
                ns_neib_host.append(str(host))
                ns_neib_cnt += 1
        #print(f"{ns_neib_cnt}/{addresses.num_addresses} hosts are online.")
        return ns_neib_host, ns_neib_cnt


    #async def ns_neighbors(self,ns_cdef_ip,ns_net_ccidr):
    def ns_port_scan(self,ns_neib_host):
        ns_scan_res_array = []
        for ns_up_host in ns_neib_host:
            ns_top_ports = [ 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1433, 1723, 3306, 3389, 5900, 8080, 9100 ]
            for dst_port in ns_top_ports:
                src_port = random.randint(1025,65534)
                resp = sr1(IP(dst=ns_up_host)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,verbose=0)
                if resp is None:
                    #print(f"{ns_up_host}:{dst_port} is dropped")
                    continue
                elif(resp.haslayer(TCP)):
                    if(resp.getlayer(TCP).flags == 0x12):
                        # Send a gratuitous RST to close the connection
                        send_rst = sr(IP(dst=ns_up_host)/TCP(sport=src_port,dport=dst_port,flags='R'),timeout=1,verbose=0)
                        #print(f"{ns_up_host}:{dst_port} is open")
                        ns_scan_res_array.append(dict(ns_neighbor_ip = ns_up_host, ns_neighbor_port = dst_port))
                    elif (resp.getlayer(TCP).flags == 0x14):
                        #print(f"{ns_up_host}:{dst_port} is closed")
                        continue
        return ns_scan_res_array
    
if __name__ == "__main__":
    print(Fore.YELLOW + r"""
    ╔═╗─╔╗───╔╗─╔╗╔═══╦╗───╔═╦╗──╔══╗─────────────────╔╗╔╗─────╔═╗╔═╗──╔╗──────╔╗─╔╗─╔═══╗╔╗
    ║║╚╗║║───║║╔╝╚╣╔═╗║║───║╔╝╚╗─║╔╗║────────────────╔╝╚╣║─────║║╚╝║║──║║──────║║╔╝╚╗║╔═╗║║║
    ║╔╗╚╝╠╦══╣╚╩╗╔╣╚══╣╚═╦╦╝╚╗╔╬╗║╚╝╚╦╗╔╦═╦═╗╔╦═╗╔══╗╚╗╔╣╚═╦══╗║╔╗╔╗╠╦═╝╠═╗╔╦══╣╚╩╗╔╝║║─║╠╣║
    ║║╚╗║╠╣╔╗║╔╗║║╚══╗║╔╗╠╬╗╔╣║╚╝║╔═╗║║║║╔╣╔╗╬╣╔╗╣╔╗║─║║║╔╗║║═╣║║║║║╠╣╔╗║╔╗╬╣╔╗║╔╗║║─║║─║╠╣║
    ║║─║║║║╚╝║║║║╚╣╚═╝║║║║║║║║╚╦╗║╚═╝║╚╝║║║║║║║║║║╚╝║─║╚╣║║║║═╣║║║║║║║╚╝║║║║║╚╝║║║║╚╗║╚═╝║║╚╗
    ╚╝─╚═╩╩═╗╠╝╚╩═╩═══╩╝╚╩╝╚╝╚═╩╝╚═══╩══╩╝╚╝╚╩╩╝╚╩═╗║─╚═╩╝╚╩══╝╚╝╚╝╚╩╩══╩╝╚╩╩═╗╠╝╚╩═╝╚═══╩╩═╝
    ──────╔═╝║───────────────────────────────────╔═╝║───────────────────────╔═╝║ Scanner
    ──────╚══╝───────────────────────────────────╚══╝───────────────────────╚══╝ version 0.9
            """)
    NightShift_Recon().run()

# Define end host and TCP port range
#host = "192.168.40.1"
#port_range = [22, 23, 80, 443, 3389]

# Send SYN with random Src Port for each Dst port
#for dst_port in port_range:
#    src_port = random.randint(1025,65534)
#    resp = sr1(
#        IP(dst=host)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,
#        verbose=0,
#    )
#
#    if resp is None:
#        print(f"{host}:{dst_port} is filtered (silently dropped).")
#
#    elif(resp.haslayer(TCP)):
#        if(resp.getlayer(TCP).flags == 0x12):
#            # Send a gratuitous RST to close the connection
#            send_rst = sr(
#                IP(dst=host)/TCP(sport=src_port,dport=dst_port,flags='R'),
#                timeout=1,
#                verbose=0,
#            )
#            print(f"{host}:{dst_port} is open.")
#
#        elif (resp.getlayer(TCP).flags == 0x14):
#            print(f"{host}:{dst_port} is closed.")
#
#    elif(resp.haslayer(ICMP)):
#        if(
#            int(resp.getlayer(ICMP).type) == 3 and
#            int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]
#        ):
#            print(f"{host}:{dst_port} is filtered (silently dropped).")
