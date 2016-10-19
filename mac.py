import requests
import json
import socket
import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Grab the MAC")
    parser.add_argument('-H', dest='h_name', required=True, type=str,  help="Enter hostname")
    parser.add_argument('-i', dest='ip_addr', required=False, help='Enter IP address')
    return parser.parse_args()

args = get_args()
hostname = args.h_name

switches = ['enter_switch_ip']
# ip_addr = '10.239.10.101'
# hostname = "unreal"

try:
    r_host_ip = socket.gethostbyname(hostname)
except StandardError:
    print "Can't resolve hostname"
    sys.exit(0)


# url='http://YOURIP/ins'
switchuser='enter_user_name'
switchpassword='enter_password'

def get_mac():

    for sw in switches:
        url = 'http://' + sw + '/ins'
        myheaders={'content-type':'application/json'}
        payload={
          "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "sh ip arp " + r_host_ip,
            "output_format": "json"
          }
        }
        try:
            response = requests.post(url,data=json.dumps(payload),
                                     headers=myheaders,auth=(switchuser,switchpassword)).json()
        except StandardError:
            print "can't execute query"
            sys.exit(0)

        try:
            mac = response['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj']['mac']
        except StandardError:
            print "Cant' find IP"
            sys.exit(0)

        return mac

print hostname + ' ' + get_mac()
