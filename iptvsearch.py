# iptvscan
# Script for scanning and saving IPTV playlist.
# Python v.3 required for using. https://www.python.org/downloads/

# Author: joddude <joddude@gmail.com>

# Disclaimer:
# This script is free and provided "as is" without any warranty.
# You can use it at your own risk.
# The author assumes no responsibility for any moral or material damage caused
# by the use of this software, any loss of profit as a result of or during use.

#------------------------------------------------------------------------------

# Ukrtelecom (udp://@232.0.2.10:3000)
#protocol = 'udp'
#ip_start = '232.0.2.0'
#ip_end =   '232.0.2.254'
#port = 3000

# oll.tv (rtp://@233.12.130.250:2000)
protocol = 'rtp'
ip_start = '239.3.1.1'
ip_end =   '239.3.1.254'
port = 2000

timeout=1   # seconds
random_search = False   # False or True

#------------------------------------------------------------------------------

import socket
import struct
import os, sys
import time, datetime
from random import shuffle

#------------------------------------------------------------------------------

def main():
    ip_list = ip_range(ip_start, ip_end)
    if random_search:
        shuffle(ip_list)
    playlist_name = 'IPTV-'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.m3u'
    found_channels = 0
    print('IP from', ip_start, 'to', ip_end, '('+str(len(ip_list))+')')
    print('Port:', port)
    print('Playlist name:', playlist_name)
    with open(playlist_name, "w") as file:
        print('#EXTM3U', file=file)
        print('', file=file)
        update_progress(0, 'Scan '+ip_start)
        for port1 in [1234, 2000,3120,4120,8000, 8001, 8004,8008,8012, 8016, 8020, 8024, 8028, 8032, 8036, 8040, 8044, 8048, 8052, 8056, 8060, 8064, 8068,8072,8084, 8092, 8104,8108, 8112, 8116, 8120,8124, 8128,8132,8136,8140,8144,8148,8152, 8156,8160,8164,8172,8176,8184,8188, 8192,8196,8200, 8216, 8220,8224,8228, 8232,8236,8268, 8272,8276,8280,8284, 8288,8292,8296,8300,8304,9000,9004,9008,9012,9016,9020, 9024,9136,9244,9252,9268]:
            for counter, ip in enumerate(ip_list, start=1):
                if iptv_test(ip, port1, timeout):
                    print('#EXTINF:-1,'+ip, file=file)
                    print(protocol+'://'+ip+':'+str(port1), file=file)
                    print('', file=file)
                    found_channels +=1
                update_progress(counter/len(ip_list), 'Scan '+ip + ':' + str(port1), '(Found '+str(found_channels)+' channels)    ')
    print('Found '+str(found_channels)+' channels')

#------------------------------------------------------------------------------

def iptv_test(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    try:
        if sock.recv(10240):
            return True
        else:
            return False
    except socket.timeout:
        return False

#------------------------------------------------------------------------------

def ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range

#------------------------------------------------------------------------------

def update_progress(progress, title='Progress', status = ''):
    barLength = 50
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt"+" "*21+"\r\n"
    if progress >= 1:
        progress = 1
        status = "Done"+" "*21+"\r\n"
    block = int(round(barLength*progress))
    text = '\r'+title+': [{0}] {1}% {2}'.format( '#'*block + '-'*(barLength-block), round(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        print('IPTV scan started. Press Ctrl+C to stop.')
        main()
    except KeyboardInterrupt:
        print()
        print('You pressed Ctrl+C. Stop')
        sys.exit()
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print('IPTV scan finished. Press Enter to exit ...')
        input()
