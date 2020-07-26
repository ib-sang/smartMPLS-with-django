from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpRequest, JsonResponse, HttpResponseRedirect
from netmiko import ConnectHandler
from napalm import get_network_driver
from netmiko import Netmiko
from .models import *
from .forms import *



def index(request)-> HttpResponse:
    content = {}
    return render(request, "index.html", content)


def index_manager(request)-> HttpResponse:
    device = Device.objects.all().count()
    access = Access.objects.all().count()
    topos = Topologies.objects.all().count()
    vrf = Vrf.objects.all().count()
    content = {
        "device" : device,
        "access" : access,
        "topo" : topos,
        "vrf" : vrf,
        "title": "manager"
    }
    return render(request, 'manager/index.html', content)


def accesses(request):
    access = Access.objects.all()
    number = access.count()
    content = {
        "accesses" : access,
        "number" : number
    }
    
    return render(request,"manager/access/indexaccess.html", content)


def edit_access(request, access_id) -> HttpResponse:
    access = Access.objects.get(id=access_id)
    if request.method== "POST":
        form = AccessForm(request.POST, instance=access)
        if form.is_valid():
            access.save()
            request.session['success'] = "You have edited management : " + request.POST["username"]
            request.session.set_expiry(10) 
        else:
            request.session['error'] = "Username or Password is not valid"
            request.session.set_expiry(10)    
        return HttpResponseRedirect("/manager/accesses")    
        
    form = AccessForm(instance=access)
    content = {
        "form" : form ,
        "access" : access, 
        "title" : "access"
        } 
    return render(request, "manager/access/edit/editaccess.html", content)


def add_access(request)-> HttpResponse:
    if request.method=='POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success'] = "You have added a new management in database"
            request.session.set_expiry(10) 
        return  HttpResponseRedirect('/manager/accesses') 
    access_form = AccessForm()
    content={
        'access_form' : access_form,
        "title": 'access'
        }
    return render(request, "manager/access/new/addaccess.html", content)


def del_access(request, access_id)-> HttpResponse:
    access = Access.objects.get(id = access_id)
    request.session['error'] = access.username +" was deleted"
    request.session.set_expiry(10)
    access.delete()
    return  HttpResponseRedirect('/manager/accesses')


def topology(request)-> HttpResponse:
    topo = Topologies.objects.all()
    number = topo.count()
    content = {
        "topology" : topo,
        "number" : number
    }
    
    return render(request,"manager/topology/indextopology.html", content)


def add_topo(request)-> HttpResponse:
    if request.method=='POST':
        form = TopologyForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success'] = "You have added a new topology in database"
            request.session.set_expiry(10) 
        return  HttpResponseRedirect('/manager/topology') 
    topo_form = TopologyForm()
    content={
        'topo_form' : topo_form,
        "title":'topology'
        }
    return render(request, "manager/topology/new/addtopology.html", content)


def edit_topo(request, topo_id)-> HttpResponse:
    topo = Topologies.objects.get(id=topo_id)
    if request.method== "POST":
        form = TopologyForm(request.POST, instance=topo)
        if form.is_valid():
            topo.save()
            request.session['success'] = "You have modified a topology : " + request.POST["name"]
            request.session.set_expiry(10)    
        return HttpResponseRedirect("/manager/topology")    
        
    form = TopologyForm(instance=topo)
    content = {
        "form" : form ,
        "topo" : topo, 
        "title" : "access"
        } 
    return render(request, "manager/topology/edit/edittopology.html", content)


def del_topo(request, topo_id)-> HttpResponse:
    topo = Topologies.objects.get(id = topo_id)
    request.session['error'] = topo.name +" was deleted"
    request.session.set_expiry(10)
    topo.delete()
    return  HttpResponseRedirect('/manager/topology')

    
def device(request):
    device = Device.objects.all()
    number = device.count()
    content = {
        "devices" : device,
        "number" : number,
        "title": "device"
    }
    
    return render(request,"manager/device/indexdevice.html", content)

def edit_device(request, device_id) -> HttpResponse: 
    device = Device.objects.get(id=device_id)
    if request.method== "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device.save()
            request.session['success'] = "You have modified a topology : " + request.POST["name"]
            request.session.set_expiry(10)    
        return HttpResponseRedirect("/manager/device")    
        
    form = DeviceForm(instance=device)
    content = {
        "form" : form ,
        "device" : device, 
        "title" : "device"
        } 
    return render(request, "manager/device/edit/editdevice.html", content)


def del_device(request, device_id) -> HttpResponse: 
    device = Device.objects.get(id = device_id)
    request.session['error'] = device.name +" was deleted"
    request.session.set_expiry(10)
    device.delete()
    return  HttpResponseRedirect('/manager/device')

def add_device(request)-> HttpResponse:
    if request.method=='POST':
        new_device = DeviceForm(request.POST)
        if new_device.is_valid():
            new_device.save()
            request.session['success'] = "You have added a new device in database"
            request.session.set_expiry(10) 
        return  HttpResponseRedirect('/manager/device') 
    device_form = DeviceForm()
    content={
        'device_form' : device_form,
    }
    return render(request, 'manager/device/new/adddevice.html',content)

   
def vrf(request) -> HttpResponse:
    vrf = Vrf.objects.all()
    number = vrf.count()
    content = {
        "vrfs" : vrf,
        "number" : number,
        "path":"manager",
        "title": 'manager',
    }
    
    return render(request,"manager/vrf/indexvrf.html", content)


def add_vrf(request) :
    if request.method=='POST':
        vrf_form = VRFForm(request.POST)
        if vrf_form.is_valid():
            name= request.POST["name"]
            rd = request.POST["rd"]
            routeImport = request.POST["routeImport"]
            routeExport = request.POST["routeExport"]
            devices = vrf_form.cleaned_data['devices']
            params_all= {}
            outputs=[]
            config_commands = {
                    "ip vrf "+name,
                    "rd " +rd,
                    "route-target import " + routeImport,
                    "route-target export "+ routeExport
                }
            command = 'show ip vrf interf'
            for device in devices:
                device_run = Device.objects.get(name = device)
                
                params = {
                    "host" : device_run.host,
                    "username" : device_run.username,
                    "password" : device_run.password,
                    'device_type' : device_run.plateform,
                }
                params_all[device.name]= params
                with ConnectHandler(**params) as device_conf:
                    device_conf.send_config_set(config_commands)            
            vrf_form.save()    
        return  HttpResponseRedirect('/manager/vrf')
    vrf_form = VRFForm()
    content={
        'form' : vrf_form,
        "path":"manager",
        "title": 'manager'
    }    
    return render(request, 'manager/vrf/new/addvrf.html',content)  


def del_vrf(request, vrf_id):
    return HttpResponse('hello vrf')   
   
def add_vrf_device(request,device_id) -> HttpResponse:
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
            return redirect('add_vrf_device',device.id)     
    else:
        vrf_form = AddVRFForm()
        content={
            'device' : device,
            'vrf_form' : vrf_form,
        }
        return render(request, 'addVrfinDevice.html',content)
  
  


