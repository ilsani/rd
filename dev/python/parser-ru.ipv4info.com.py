#!/bin/env python
# Parse http://ru.ipv4info.com/ page
#
# input file creation: grep "href" rawpage.html  |grep -E "ip-address|dns" |xargs -L2 > out.txt
# input file: href=/ip-address/sc93b8b/IPADDRESS.html>IPADDRESS</a></td> <a href=/dns/s1cfdb7/HOSTNAME>
import sys
import re
import socket

from netaddr import IPAddress, IPNetwork

def read_file(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            yield line

def get_file_line_info(line):
    ip = re.match(".*html\>(.*?)\<.*", line).group(1)
    vhost = re.match(".*/(.*?)\>", line).group(1)
    return (ip, vhost)

def is_valid_ip(ip, scope):
    return IPAddress(ip) in scope

def check_ip(vhost, srcip):
    (hostname, aliases, ipaddresses) = socket.gethostbyname_ex(vhost)
    return srcip in ipaddresses

def process_valid_file_line(ip, vhost):
    print "%s;%s" %(ip, vhost)
            
def main():
    try:
        path = sys.argv[1]
        scope = IPNetwork(sys.argv[2])

        for line in read_file(path):
            (ip, vhost) = get_file_line_info(line)

            if not is_valid_ip(ip, scope):
                continue

            if not check_ip(vhost, ip):
                continue

            process_valid_file_line(ip, vhost)

    except Exception, e:
        print str(e)

if __name__ == "__main__":
    main()
