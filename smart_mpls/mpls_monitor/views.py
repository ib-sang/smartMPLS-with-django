from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpRequest, JsonResponse
from netmiko import ConnectHandler
from napalm import get_network_driver
from netmiko import Netmiko
from .models import Device

# Create your views here.

INTERFACE_STATS_CHANGE_TEMPLATE = """interface (interface_name)
"""


def get_device_stats(request,device_id):
    device=Device.objects.get(id=device_id)
    if request.method=='POST':
        interface_name = request.POST.get('interface_name')
        enable_interface = request.POST.get('enable')
        device=Device.objects.get(id = device_id)
        config_commands=[ f'interface {interface_name}']
        result = {"interface_name": interface_name}
        if enable_interface==False:
            config_commands.append('shutdown')
            result['up'] = False
        else:
            config_commands.append('no shutdown')
            result['up'] = True
        params = {
            'ip': device.host,
            'username': device.username,
            'password' : device.password,
            'device_type' : device.plateform
        }
        with ConnectHandler(**params) as device_conf:
            device_conf.send_config_set(config_commands)
        #task_id = tasks.router_interface.delay(device_id, interface_name, enable_interface).id
        #print(task_id)
        return redirect('device', device_id=device_id)
    else:   
        driver = get_network_driver(device.napalm_driver)
        host = device.host
        username = device.username
        password = device.password
        device_run = driver(host, username, password, timeout=180)
        try:
            device_run.open()
            interfaces = device_run.get_interfaces()
        except Exception as e:
            request.session['error'] = "Cannot connect to "+device.host
            request.session.set_expiry(10)
            return redirect('devices')
        #with driver(host, username, password, optional_args={}) as device_run:
        #    interfaces = device_run.get_interfaces()
        content={
            'device':device,
            'interfaces': interfaces,
        }
        print(device)
        return render(request, 'interface.html',content)

def interface(request):
    return HttpResponse('<h2>les interface </h2>')


      