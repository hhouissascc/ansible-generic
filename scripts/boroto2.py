#!/usr/bin/env python

import vm_automation
import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json
def get_esxi_inventory(vm_automation):
    #create esxi instance
    myserver = vm_automation.esxiServer("192.168.31.137", "root", "@ddVantage2019", "443", "first_log_rapid7.log")
    print myserver.connect()
    print myserver.getVersion()
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

bibou=get_esxi_inventory(vm_automation)
print bibou
