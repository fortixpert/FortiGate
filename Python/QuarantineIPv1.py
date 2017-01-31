#!/usr/bin/env python2
# Created by Fortixpert @SE team - Iberia

import paramiko
import argparse
from ConfigParser import SafeConfigParser
import time

sleepTime = 0.2
recvSize = 1024

def parseArgs():
    # Parse arguments and display help
    parser = argparse.ArgumentParser(description='Tool that add banned IP from i variable')
    parser.add_argument('-d', help='IP address of FG', default="192.168.1.99")
    parser.add_argument('-u', help='username', default="admin")
    parser.add_argument('-p', help='password', default="")
    parser.add_argument('-i', help='badip', default="1.1.1.1")
    args = parser.parse_args()
    return args

def configParser(parser, args, location):
    if parser.has_option(location, 'ip'):
        ip = parser.get(location, 'ip')
    else:
        ip = "192.168.1.99"
    if parser.has_option(location, 'device'):
        device = parser.get(location, 'device')
    else:
        device = "192.168.1.99"
    if parser.has_option(location, 'user'):
        user = parser.get(location, 'user')
    else:
        user = "admin"
    if parser.has_option(location, 'pass'):
        password = parser.get(location, 'pass')
    else:
        password = ""
    return (device, user, password, ip)

def connect(device, user, passw):
    # Connect to FGT device.
    global ssh
    global chan

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device, username=user, password=passw)
    chan = ssh.invoke_shell()

def disconnect():
    # Disconnect from FGT device
    chan.close()
    ssh.close()

def exeCommand(command):
    # Execute command on FGT device.
    chan.send('%s\n' % command )
    time.sleep(sleepTime)
    resp = chan.recv(recvSize)
    return resp

def banBadIP(banthisip):
    # Add bad ip to user banned
      exeCommand('diagnose user quarantine add src4 %s' % banthisip )

def main():
    # Main function of this program.
    args = parseArgs()
    device = args.d
    user = args.u
    password = args.p
    banthisip = args.i + ' 10 ips'
    connect(device, user, password)
    banBadIP(banthisip)
    disconnect()

if __name__ == "__main__":
    main()
