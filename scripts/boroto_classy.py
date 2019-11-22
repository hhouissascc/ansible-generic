#!/usr/bin/env python

import vm_automation
import os
import sys
import argparse

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
            self.inventory = self.prepare_esxi_inventory(lollo)
            #self.inventory = self.get_esxi_inventory(vm_automation)
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print (json.dumps(self.inventory))#;

    def get_esxi_inventory(self, vm_automation):
        #create esxi instance
        myserver = vm_automation.esxiServer("192.168.31.137", "root", "@ddVantage2019", "443", "first_log_rapid7.log")
        #print myserver.connect()
        #print myserver.getVersion()
        #myserver.enumerateVms()
        return myserver


    def prepare_esxi_inventory(self, myserver):
        myserver.enumerateVms()
        
        mainus = {}
        hostvars={} # is the content of metas: metas.update("hostvars": hostvars)
        debianss={"children": [], "vars": {}} #is the value of linxy
        redss= {"children": [], "vars": {}} #is the Value of redservers
        ungroupss = {"children": [], "vars": {}}#is the Value ofungrouped
        winss = {"children": [], "vars": {}}#is the Value of winservers

        #prepare _meta hostvars
        hostvarius={}
        hostvarius_element= {}   #{"{}".format(vm.VmName): "{}".format(hostvaius_element_details)}
        hostvaius_element_details= {"ansible_user": "ansible"}   #{"ansible_host": "192.168.31.142",  }

        reds=[]
        debians=[]
        wins=[]
        ungrouped_hosts=[]

        all = {"children": ["ungrouped","redservers","linxy", "winservers"],"hosts": [],"vars": {}}
        #create empty list of IPs
        vmips=[]


        vmDic = {}
        for vm in myserver.vmList:
            vmDic[vm.vmName] = vm
            vmips.append(vmDic[vm.vmName].getVmIp())

            new_sub_meta={"ansible_user": "ansible"}
            ipoun = vmDic[vm.vmName].getVmIp()
            new_sub_meta.update({"ansible_host": vmDic[vm.vmName].getVmIp()})
            hostvars.update({vmDic[vm.vmName].vmName: new_sub_meta})
            #non_meta.
            if "Red Hat" in vmDic[vm.vmName].vmOS:
                reds.append(vmDic[vm.vmName].vmName)
            elif "Ubuntu" in vmDic[vm.vmName].vmOS:
                debians.append(vmDic[vm.vmName].vmName)
            elif "Windows" in vmDic[vm.vmName].vmOS:
                wins.append(vmDic[vm.vmName].vmName)
            else:
                ungrouped_hosts.append(vmDic[vm.vmName].vmName)

        metastase = {}
        metastase.update({"hostvars": hostvars})
        mainus.update({"_meta": metastase})

        mainus.update({"all": all})

        debianss.update({"hosts": debians})
        mainus.update({"linxy": debianss})

        redss.update({"hosts": reds})
        mainus.update({"redservers": redss})


        winss.update({"hosts": wins})
        mainus.update({"winservers": winss})

        ungroupss.update({"hosts": ungrouped_hosts})
        mainus.update({"ungrouped": ungroupss})


        return mainus
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
#bibou=get_esxi_inventory(self, vm_automation)
#print bibou
