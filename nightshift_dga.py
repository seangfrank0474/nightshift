#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from datetime import date
import ctypes
import socket
import sys
import os
import dns.message
import dns.name
import dns.rdataclass
import dns.rdatatype
import dns.resolver

class NightShift_DGA():
    def _ns_month_seed(self):
        mnthseed = {
            '01': '15789139',
            '02': '19871027',
            '03': '15109199',
            '04': '15709067',
            '05': '16789399',
            '06': '17803147',
            '07': '15499409',
            '08': '14901327',
            '09': '10976489',
            '10': '15499357',
            '11': '15499499',
            '12': '15499387'
            }
        return mnthseed
    
    def ns_dga_algorithm(self,key_domain):
        if key_domain == 'key':
            init_i = 32
            idx = 256
        elif key_domain == 'domain':
            init_i = 16
            idx = 128
        else:
            print('Unknown variable, please try again! ¯\_(``)_/¯')
            sys.exit(1)
        today_tuple = date.today()
        tday_list = str(today_tuple).split('-')
        cur_day = tday_list[2]
        cur_month = tday_list[1]
        cur_year = tday_list[0]
        today_str = '{0}{1}{2}'.format(cur_year, cur_month, cur_day)
        dict_m_seed = self._ns_month_seed()[cur_month]
        t_seed = int(today_str)
        m_seed = int(dict_m_seed)
        init_seed = t_seed + m_seed
        domains = ""
        domain = []
        for i in range(init_i):
            seed = (idx + i + ((init_seed >> 0x18) & 0xff | (init_seed << 0x8)) + 0x65BA0642) & 0xffffffff
            s_seed = ctypes.c_int(seed).value
            domain.append(chr((abs(s_seed) % 0x19) + ord("a")))
        domain = "".join(domain)
        domains = domain 
        return domains
        
    def run(self):
        key_domain = sys.argv[1]
        nsdga_output = self.ns_dga_algorithm(key_domain)
        return nsdga_output

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nsdga_output = NightShift_DGA().run()
        print('Here is the domain/key string you requested - {0}'.format(nsdga_output))
        sys.exit(0)
    else:
        print('Usage:\npython3 nightshift_dga.py key (to generate comm key)\npython3 nightshift_dga.py domain (to generate dga domain)')
        sys.exit(1)

    # Future expansion for DNS check when domain has been requested.    
    #myResolver = dns.resolver.Resolver()
    #myResolver.nameservers = ['8.8.8.8']
    #full_dmn = []
    #for tld in '.su', '.ru', '.tk', '.tr', '.ir':
    #    for sub_dmn in domains:
    #        #print(sub_dmn + tld)
    #        f_domain = sub_dmn + tld
    #        #print(f_domain)
    #        full_dmn.append(f_domain)
    #    #print(full_dmn)
    #    for final in full_dmn:
    #        print(final)
    #        try:
    #            myAnswer=myResolver.query(final, "A", raise_on_no_answer=True)
    #            #time.sleep(2)
    #            #addr = socket.gethostbyname('google.com')
    #            print(myAnswer.rrset)
    #            #print(addr)
    #        #except NoAnswer:
    #        #    pass
    #        except dns.resolver.NXDOMAIN as e:
    #            print(e)
    #            pass
    #        except dns.resolver.Timeout as e:
    #            print(e)
    #            pass
    #        except dns.resolver.NoAnswer as e:
    #            print(e)
    #            pass
