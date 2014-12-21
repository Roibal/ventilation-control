#!/usr/local/bin/python
# coding: ascii

import argparse
import sys

sys.path.insert(0, './lnetatmo')
import lnetatmo

def main(args):
    # 1 : Authenticate
    authorization = lnetatmo.ClientAuth( clientId = args.clientid,
                                         clientSecret = args.clientsecret,
                                         username = args.username,
                                         password = args.password
                                       )

    # 2 : Get devices list
    devList = lnetatmo.DeviceList(authorization)

    # 3 : Access most fresh data directly
    print ("Current temperature (inside/outside): %s / %s C" %
            ( devList.lastData()['Innen']['Temperature'],
              devList.lastData()['Outdoor']['Temperature'])
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
    parser.add_argument('--clientid', type=str, required=True, help='Netatmo CLIENT_ID')
    parser.add_argument('--clientsecret', type=str, required=True, help='Netatmo CLIENT_SECRET')
    parser.add_argument('--username', type=str, required=True, help='Netatmo USERNAME')
    parser.add_argument('--password', type=str, required=True, help='Netatmo PASSWORD')
    args = parser.parse_args()
    main(args)
