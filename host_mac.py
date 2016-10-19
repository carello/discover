import requests
import json
import socket
import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Grab the MAC")
    parser.add_argument('-n', dest='h_name', required=True, type=str,  help="Enter hostname")
    parser.add_argument('-i', dest='ip_addr', required=False, help='Enter IP address')
    parser.add_argument('-u', dest='r_user', help='Enter User ID')
    parser.add_argument('-p', dest='r_pass', help='Enter password')
    return parser.parse_args()

args = get_args()
switchuser = args.r_user
switchpassword = args.r_pass
hostname = args.h_name

switches = ['10.91.86.234', '10.91.86.244']


def resolv_hostname():
    try:
        r_host_ip = socket.gethostbyname(hostname)
        return r_host_ip
    except StandardError:
        print "Can't resolve hostname"
        sys.exit(0)


r_host_ip = resolv_hostname()

s = requests.Session()
s.auth = (switchuser, switchpassword)
s.headers = {'content-type':'application/json'}
s.payload = {
          "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "sh ip arp " + r_host_ip,
            "output_format": "json"
              }
            }

def get_mac():

    for sw in switches:
        url = 'http://' + sw + '/ins'

        #response = requests.post(url, data=json.dumps(s.payload), headers=s.headers, auth=s.auth).json()
        try:
            response = s.post(url, data=json.dumps(s.payload)).json()
        except StandardError:
            print "Can't log into switch: " + sw
            continue

        resp = str(response['ins_api']['outputs']['output']['code'])

        if resp != '200':
            print "ERROR: Logged into device but unable to get data" + sw
            sys.exit(0)

        cnt = response['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['cnt-total']
        if cnt != 0:
            try:
                mac = response['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj']['mac']
                return mac, sw

            except StandardError:
                print "Cant' find MAC"




if __name__ == '__main__':
    page = get_mac()

    if page == None:
        print "can't find MAC"
    else:
        print "\nHOSTNAME: {} | MAC: {} | SWITCH: {}".format(hostname, page[0], page[1])
