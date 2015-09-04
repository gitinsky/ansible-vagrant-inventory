#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2015, Roman Belyakovsky <ihryamzik@gmail.com>

import json
import string
import os
import argparse
import glob

parser = argparse.ArgumentParser(description='Process ansible inventory options')
parser.add_argument("-l", "--list", action='store_true', help="list of groups" )
parser.add_argument("-H", "--host", help="dictionary of variables for host")

args = parser.parse_args()

def prettyprint(string):
    print json.dumps(string, indent=4, sort_keys=True)


def getClients():
    clientListString = os.popen("grep ssh .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory|tr '=' ' '").read()
    clients = {}
    for clientString in clientListString.split('\n'):
        clientVars = clientString.split()
        if len(clientVars) == 5:
            c={}
            name, _, c['ansible_ssh_host'], _, c['ansible_ssh_port'] = clientVars
            clients[name] = c
    return clients

clients=getClients()

if args.list:
    hostlist = {
      "_meta" : {
      "hostvars": clients
      },
      "groupclients": clients.keys(),
    }
    prettyprint(hostlist)

elif args.host:
    try:
        prettyprint( clients[args.host] )
    except:
        pass
else:
    prettyprint(clients)
