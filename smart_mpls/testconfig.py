from netmiko import Netmiko
import json
from napalm import get_network_driver
from netmiko import ConnectHandler

#driver = get_network_driver('ios')
#host='192.168.231.157'
#host='192.168.200.21'
#username='admin'
#password='admin'
#with driver(host, username, password, optional_args={}) as device:
#    output = device.get_interfaces()


config_commands=[]
params = {
        'ip': '192.168.200.24',
        'username': 'admin',
        'password' : 'admin',
        'device_type' : 'cisco_ios'
    }
command='show ip interface bri | section Loopback0'
#net_connect = Netmiko(**params)
#print(net_connect.find_prompt())
tab=[]
with ConnectHandler(**params) as device_conf:
    output = device_conf.send_command(command)
  
output = output.split()
print(output[1])    
#first, *others = output.splitlines()
#leng= len(first)
#protocol_backbone = first[21:leng -1]
#print(output)
#print(first)
#print(protocol_backbone)
#print(others)
#output = output.split()  
  
#leng= len(output)
#i = 4
#print(leng)
js={}
j=0

#while i< leng:
    
#    js[output[i]] = {
#        "ip-address" : output[i+1],
#        "vrf" : output[i+2],
#        "protocol" : output[i+3]
#    }
    
#    i=i+4

#print(js)     
#while i< leng:
#    if output[i+1]=='<not':
#        js[j] = {
#        "name" : output[i],
#        "rd" : output[i+1] + ' ' + output[i+2],
#        "interface" : output[i+3],
#        }
#        i=i+4
#    else:
#        js[j] = {
#            "name" : output[i],
#            "rd" : output[i+1],
#            "interface" : output[i+2],
#        }
#        i=i+3
#    j=j+1

