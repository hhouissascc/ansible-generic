#!/usr/bin/env python

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
#import rapid7 esxi
import vm_automation



try:
    import json
except ImportError:
    import simplejson as json

class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            lollo=self.get_esxi_inventory(vm_automation)
            self.inventory = self.example_inventory(lollo)
            #self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print (json.dumps(self.inventory))#;

    # connect to esxi and get vmName vmIp.
    def get_esxi_inventory(self, vm_automation):
        myserver = vm_automation.esxiServer("192.168.31.137", "root", "@ddVantage2019", "443", "first_log_rapid7.log")
        #print myserver.connect()
        #print myserver.getVersion()
        myserver.enumerateVms()
        vmnamelist=[]
        for vm in myserver.vmList:
            #print vm.__dict__.keys()
            #print vm.vmName
            #print "vm.vmIp is: {} ".format(vm.vmIp)
            #print "vm OS is {}".format(vm.vmOS)
            #print "vm.vmUsername is: {} ".format(vm.vmUsername)
            #print ""
            vmnamelist.append(vm.vmName)
        vmnamelist=[]
        #create empty list of IPs
        vmips=[]
        #print "create vm Dictionary"

        vmDic = {}
        for vm in myserver.vmList:
            vmDic[vm.vmName] = vm
            #print vmDic[vm.vmName].getVmIp()
            vmips.append(vmDic[vm.vmName].getVmIp())

        #print "vmnamelist"
        #print vmnamelist
        #print "vm ips list"
        #print vmips

        return vmips

    # Example inventory for testing.
    def example_inventory(self, vmips):
        return {
            'group': {
                'hosts': vmips ,
                'vars': {
                    'ansible_ssh_user': 'ansible',
                    'ansible_ssh_private_key_file':
                        '/home/ansible/.ssh/id_rsa',
                    'example_variable': 'value'
                }
            },
            '_meta': {
                'hostvars': {
                    '192.168.28.71': {
                        'host_specific_var': 'foo'
                    },
                    '192.168.28.72': {
                        'host_specific_var': 'bar'
                    }
                }
            }
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}


    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
ExampleInventory()
#ansible all -m ping -i generate_dynamyc_inv.py --ask-pass
