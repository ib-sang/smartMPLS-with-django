from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpRequest, JsonResponse, HttpResponseRedirect
from netmiko import ConnectHandler
from napalm import get_network_driver
from netmiko import Netmiko
from mpls_monitor.models import Device
from .forms import *

# Create your views here.


def devices(request) -> HttpResponse:
    devices=Device.objects.all()
    content={
    'devices': devices,
    'title':'Hello stream',
    'name':'ib'
    }
    return render(request, 'devices.html',content)

def add_vrf(request,device_id) -> HttpResponse:
    device=Device.objects.get(id=device_id)
    if request.method=='POST':
        driver = get_network_driver(device.napalm_driver)
        host = device.host
        username = device.username
        password = device.password
        params = {
            'ip': device.host,
            'username': device.username,
            'password' : device.password,
            'device_type' : device.plateform
        }
        name_vrf = request.POST["name"]
        rd = request.POST["rd"]
        routeImport = request.POST['routeImport']
        routeExport = request.POST["routeExport"]
        
        config_commands=[ 
            "ip vrf "+name_vrf,
            "rd "+rd,
            "route-target import "+routeImport,
            "route-target export "+routeExport,
        ]
        try:
            with ConnectHandler(**params) as device_conf:
                device_conf.send_config_set(config_commands)
            request.session['success'] = "a vrf "+name_vrf+" is created on the device "+device.name
            request.session.set_expiry(10)
            vrf_form= AddVRFForm(request.POST)  
            if vrf_form.is_valid():
                new_vrf = Vrf(name = name_vrf, rd = rd, routeImport = routeImport, routeExport = routeExport)
                new_vrf.save()    
            return  HttpResponseRedirect('/devices') 
        except Exception as e:
            request.session['error'] = "Cannot connect to "+device.host
            request.session.set_expiry(10)
            return redirect('add_vrf',device.id)     
    else:
        vrf_form = AddVRFForm()
        content={
            'device' : device,
            'vrf_form' : vrf_form,
        }
        return render(request, 'addVrf.html',content)
  