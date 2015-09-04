#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2015, Roman Belyakovsky <ihryamzik@gmail.com>

import json
import string
import os
import argparse
import glob

#===
import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],".ansible")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)


from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing import DataLoader

invetoryfile = '.vagrant/provisioners/ansible/inventory'

parser = argparse.ArgumentParser(description='Process ansible inventory options')
parser.add_argument("-l", "--list", action='store_true', help="list of groups" )
parser.add_argument("-H", "--host", help="dictionary of variables for host")

args = parser.parse_args()

def prettyprint(string):
    print json.dumps(string, indent=4, sort_keys=True)

variable_manager = VariableManager()
loader = DataLoader(vault_password=None)

inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=invetoryfile)
variable_manager.set_inventory(inventory)
# variable_manager.get_vars(loader=loader)
#=====

def getHosts():
    hosts = {}
    for host in inventory.list_hosts():
        vars = host.get_vars()
        del vars['inventory_hostname'], vars['inventory_hostname_short']
        hosts[host.name] = vars
    return hosts


def getGroups():
    groups = {}
    for group in inventory.get_groups():
        if group.name not in ['all','ungrouped']:
            groups[group.name] = [ host.name for host in group.get_hosts() ]
    return groups

hosts = getHosts()
groups = getGroups()
hostlist = {
  "_meta" : {
  "hostvars": hosts
  }
}
hostlist.update(groups)

if args.list:
    prettyprint(hostlist)

elif args.host:
    try:
        prettyprint( hosts[args.host] )
    except:
        pass
else:
    prettyprint(hosts)
