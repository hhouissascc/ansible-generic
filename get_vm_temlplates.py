#!/usr/bin/python
from pyVmomi import vim
from pyVim import connect
import ssl

def get_vim_objects(content, vim_type):
    '''Get vim objects of a given type.'''
    return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vim_type], recursive=True).view]

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#context.verify_mode = ssl.CERT_NONE
context = ssl._create_unverified_context()
si = connect.SmartConnect(host="192.168.31.137", user="root", pwd="@ddVantage2019", port=443, sslContext=context)
content = si.RetrieveContent()
for vm in get_vim_objects(content, vim.VirtualMachine):
    print type(vm)
    print type(content)
    print ""
