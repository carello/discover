import requests
import json
import socket
import sys
import argparse


switches = ['10.91.86.234', '10.91.86.244']

def get_args():
    parser = argparse.ArgumentParser(description="Grab the MAC")
    parser.add_argument('-n', dest='host_name',  required=True, help='Enter hostname')
    parser.add_argument('-u', dest='login_user', required=True, help='Enter User ID')
    parser.add_argument('-p', dest='login_pass', required=True, help='Enter password')
    return parser.parse_args()


def resolv_hostname(hst_name):
    try:
        r_host_ip = socket.gethostbyname(hst_name)
        return r_host_ip
    except StandardError:
        print "Can't resolve hostname"
        sys.exit(0)


def get_sess():
    s = requests.Session()
    s.auth = (switchuser, switchpassword)
    s.headers = {'content-type':'application/json'}
    s.payload = {"ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": "sh ip arp " + r_host_ip,
                    "output_format": "json"}
                }
    return s


def get_mac():
    for sw in switches:
        url = 'http://' + sw + '/ins'

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
                print "Can't find MAC"


if __name__ == '__main__':
    args = get_args()
    switchuser = args.login_user
    switchpassword = args.login_pass
    hostname = args.host_name

    r_host_ip = resolv_hostname(hostname)

    s = get_sess()

    page = get_mac()

    if page is None:
        print "Can't find MAC"
    else:
        print "\nHOSTNAME: {} | MAC: {} | SWITCH: {}".format(hostname, page[0], page[1])
