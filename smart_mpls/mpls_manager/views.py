from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpRequest, JsonResponse, HttpResponseRedirect
from netmiko import ConnectHandler
from napalm import get_network_driver
from netmiko import Netmiko
from .models import *
from .forms import *

CHOICES_PROTOCOL = [
    ('static', 'STATIC ROUTAGE'), 
    ('rip', 'RIP verssion 2'),
    ('eigrp', 'EIGRP'),
    ('ospf', 'OSPF'),
    ('bgp', 'BGP'),
]


def index(request)-> HttpResponse:
    content = {}
    return render(request, "index.html", content)


def index_manager(request)-> HttpResponse:
    device = Device.objects.all().count()
    access = Access.objects.all().count()
    topology = Topologies.objects.all()
    topos = topology.count()
    vrf = Vrf.objects.all().count()
    pseudos = Pseudowire.objects.all().count()
    vpls = Vpls.objects.all().count()
    projects = topology.order_by("id").reverse()[:2]
    content = {
        "device" : device,
        "access" : access,
        "topo" : topos,
        "vrf" : vrf,
        "pseudos" : pseudos,
        "vpls" : vpls,
        "title": "manager",
        "path": "manager",
        'projects':projects
    }
    return render(request, 'manager/index.html', content)


def accesses(request):
    access = Access.objects.all()
    number = access.count()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    content = {
        "accesses" : access,
        "number" : number,
        'projects': projects
    }
    
    return render(request,"manager/access/indexaccess.html", content)


def edit_access(request, access_id) -> HttpResponse:
    projects = Topologies.objects.order_by("id").reverse()[:2]
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
        "title" : "access",
        'projects' :projects,
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
    projects = Topologies.objects.order_by("id").reverse()[:2]
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
        "title":'topology',
        'projects' : projects,
        }
    return render(request, "manager/topology/new/addtopology.html", content)


def edit_topo(request, topo_id)-> HttpResponse:
    projects = Topologies.objects.order_by("id").reverse()[:2]
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
        "title" : "access",
        'projects' : projects,
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
    projects = Topologies.objects.order_by("id").reverse()[:2]
    content = {
        "devices" : device,
        "number" : number,
        "title": "device",
        'projects' : projects,
    }
    
    return render(request,"manager/device/indexdevice.html", content)


def edit_device(request, device_id) -> HttpResponse: 
    device = Device.objects.get(id=device_id)
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method== "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device.save()
            request.session['success'] = "You have modified a device : " + request.POST["name"]
            request.session.set_expiry(10)    
        return HttpResponseRedirect("/manager/device")    
        
    form = DeviceForm(instance=device)
    content = {
        "form" : form ,
        "device" : device, 
        "title" : "device",
        "projects": projects,
        } 
    return render(request, "manager/device/edit/editdevice.html", content)


def del_device(request, device_id) -> HttpResponse: 
    device = Device.objects.get(id = device_id)
    request.session['error'] = device.name +" was deleted"
    request.session.set_expiry(10)
    device.delete()
    return  HttpResponseRedirect('/manager/device')

def add_device(request)-> HttpResponse:
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method=='POST':
        new_device = DeviceForm(request.POST)
        if new_device.is_valid():
            new_device.save()
            device = Device.objects.get(name = request.POST['name'])
            loop = device.show_loop
            device.loopback = loop   
            device.save()         
            request.session['success'] = "You have added a new device in database"
            request.session.set_expiry(10) 
        return  HttpResponseRedirect('/manager/device') 
    device_form = DeviceForm()
    content={
        'device_form' : device_form,
        "title" : "device",
        "projects": projects,
    }
    return render(request, 'manager/device/new/adddevice.html',content)

   
def vrf(request) -> HttpResponse:
    vrf = Vrf.objects.all()
    number = vrf.count()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    content = {
        "vrfs" : vrf,
        "number" : number,
        "path":"manager",
        "title": 'manager',
        "projects": projects,
    }    
    return render(request,"manager/vrf/indexvrf.html", content)


def add_vrf(request) :
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method=='POST':
        vrf_form = VRFForm(request.POST)
        if vrf_form.is_valid():
            name= request.POST["name"]
            rd = request.POST["rd"]
            routeImport = request.POST["routeImport"]
            routeExport = request.POST["routeExport"]
            
            config_commands = [
                    "ip vrf "+name,
                    "rd " +rd,
                    "route-target import " + routeImport,
                    "route-target export "+ routeExport
            ]
            new_vrf = Vrf(name = name, rd = rd, routeImport = routeImport, routeExport = routeExport)
            new_vrf.save()
            devices = vrf_form.cleaned_data['devices']
            for device in devices:
                device.config_device(config_commands = config_commands)
                device_run = Device.objects.get(name = device)
                new_vrf.devices.add(device_run)
        return  HttpResponseRedirect('/manager/vrf/forwarding/'+str(new_vrf.id))
    vrf_form = VRFForm()
    content={
        'form' : vrf_form,
        "path":"manager",
        "title": 'manager',
        "projects": projects,
    }    
    return render(request, 'manager/vrf/new/addvrf.html',content)  


def del_vrf(request, vrf_id):
    vrf = Vrf.objects.get(id = vrf_id)
    device_vrf = vrf.devices.all()
    config_commands = {
                    "no ip vrf  "+vrf.name,
                }
    for device in device_vrf:
        with ConnectHandler(**device.params) as device_conf:
            device_conf.send_config_set(config_commands)
    request.session['error'] = vrf.name +" was deleted"
    request.session.set_expiry(10)
    vrf.delete()
    return HttpResponseRedirect("/manager/vrf") 
   
   
def in_vrf(request, vrf_id):
    vrf = Vrf.objects.get(id = vrf_id)
    device_vrf = vrf.devices.all()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method =="POST":
        for device in device_vrf:
            interface_fors = request.POST["int"+device.name]
            network = request.POST["net"+device.name]
            mask = request.POST["mask"+device.name]
            config_commands = [
                    "interface "+interface_fors,
                    "ip vrf forwarding "+vrf.name,
                    "ip address " +network + " "+mask,
                    "no shutdown ",
                ]
            device.config_device(config_commands = config_commands)
        return HttpResponseRedirect("/manager/vrf/vrfrouting/"+str(vrf.id))    
    forward_interface = {}
    interfaces = {}
    hosts =""
    for device in device_vrf:
        driver = get_network_driver(device.napalm_driver)
        host = device.host
        username = device.username
        password = device.password
        try:
            with driver(host, username, password, optional_args={}) as device_run:
                interfaces = device_run.get_interfaces()
        except Exception as e:
            hosts = hosts + host +", "
            print(e)
            request.session['error'] = "deosn't connected of device : "+hosts
            request.session.set_expiry(10)
        
        forward_interface[device] = interfaces       
    content={
        "devices" : device_vrf,
        "forward_interfaces" : forward_interface,
        'title': "interface provider edge",
        "projects": projects,
    }
    return render(request,"manager/vrf/edit/vrfforward.html",content)
   

def routing_vrf(request, vrf_id):
    projects = Topologies.objects.order_by("id").reverse()[:2]
    vrf = Vrf.objects.get(id = vrf_id)
    device_vrf = vrf.devices.all()
    if request.method == "POST":
        proto = request.POST["protocol"]
        proto_backbone = device_vrf[0].routing_backbone
        name = vrf.name
        if proto == "eigrp":
            as_number = request.POST["as_number"]
            system = request.POST["system"]
            config_commands = [
                    "router "+ proto_backbone,
                    "address-family ipv4 vrf  "+name,
                    "redistribute eigrp "+system,
                    "exit-address-family",
                    "router "+proto+" "+as_number,
                    "address-family ipv4 vrf  "+name,
                    "autonomous-system "+system,
                    "redistribute "+proto_backbone+" metric 1",
                    
            ]

            for device in device_vrf:
                host = device.name
                network = request.POST["net"+host]
                mask = request.POST["mask"+host]
                config_commands.append("network " +network + " "+mask)
                device.config_device(config_commands)
                config_commands.pop() 
        elif proto == 'rip':
            config_commands = [
                    "router rip ",
                    "router "+ proto_backbone,
                    "address-family ipv4 vrf  "+name,
                    "redistribute rip ",
                    "exit-address-family ",
                    "router rip ",
                    "version 2 ",
                    "address-family ipv4 vrf  "+name,
                    "redistribute "+proto_backbone+" metric  transparent ",
            ]
            for device in device_vrf:
                host = device.name
                network = request.POST["net"+host]
                config_commands.append("network " +network)
                device.config_device(config_commands)
                config_commands.pop()
        elif proto == 'ospf':
            as_number = request.POST["as_number"]
            area = request.POST['area']
            config_commands = [
                    "router "+proto+" "+as_number+" vrf "+name,
                    "router "+ proto_backbone,
                    "address-family ipv4 vrf  "+name,
                    "redistribute ospf "+as_number + " metric 1 ",
                    "exit-address-family",
                    "router "+proto+" "+as_number+" vrf "+name,
                    #"network  " +network + " "+mask,
                    "redistribute "+proto_backbone+" subnets ",
            ]

            for device in device_vrf:
                host = device.name
                network = request.POST["net"+host]
                mask = request.POST["mask"+host]
                config_commands.append("router-id " +network)
                config_commands.append("network " +network + " "+mask+ " area " +area)
                device.config_device(config_commands)
                config_commands.pop()
                config_commands.pop()
        request.session['success'] = "You are added a new customer : "+name
        request.session.set_expiry(10)
        return HttpResponseRedirect("/manager/vrf") 
    content ={
        "title" : "routing for vrf",
        "path" : "management",
        "vrf" : vrf,
        "devices" : device_vrf,
        "projects" : projects,
    }
    return render(request,"manager/vrf/edit/vrfrouting.html",content)

   
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
  
  
def pseudo(request):
    pseudos = Pseudowire.objects.all()
    number = pseudos.count()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    content = {
        "pseudos" : pseudos,
        "number" : number,
        "path":"manager",
        "title": 'pseudowire eth-to-eth',
        "projects" : projects,
    }    
    return render(request,"manager/pseudowire/indexpseudo.html", content)
  

def add_pseudo(request) :
    devices = Device.objects.all()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method=='POST':
        form = PseudowireForm(request.POST)
        if form.is_valid():
            name_pseudo= request.POST["name"]
            encapsulation = request.POST["encapsulation"]
            vcid = request.POST["vcid"]
            interface_pseudos = {}
            for device in devices :
                name = device.name
                inter =request.POST["int"+name]
                if inter != "":
                    interface_pseudos[name] = {"interface": inter,'loopback':device.loopback}    
            config_commands = [
                    "pseudowire-class "+name_pseudo,
                    "encapsulation " +encapsulation,
                ]
            new_pseudo = Pseudowire(name = name, vcid = vcid ,encapsulation = encapsulation,)
            new_pseudo.save()
            for device in devices :
                name = device.name
                config = False
                if name in interface_pseudos:
                    config = True
                    interface_remo = interface_pseudos[name]
                    interface = interface_pseudos[name]["interface"]
                    config_commands.append("interface " + interface)
                    star= len(config_commands)
                    interface_pseudos.pop(name)
                    for interface_pseudo, inter_item in interface_pseudos.items():
                        loop = inter_item['loopback']
                        config_commands.append('xconnect '+loop+' ' +vcid+' encapsulation '
                                               +encapsulation+' pw-class '+name_pseudo)
                        config_commands.append('no shutdo')
                    if config :
                        device.config_device(config_commands=config_commands)
                    del config_commands[star-1:]
                    interface_pseudos[name] =interface_remo       
        return  HttpResponseRedirect('/manager/pseudowire')
    form = PseudowireForm()
    forward_interface = {}
    interfaces = {}
    hosts =""
    
    for device in devices:
        driver = get_network_driver(device.napalm_driver)
        host = device.host
        username = device.username
        password = device.password
        try:
            with driver(host, username, password, optional_args={}) as device_run:
                interfaces = device_run.get_interfaces()
        except Exception as e:
            hosts = hosts + host +", "
            request.session['error'] = "deosn't connected of device : "+hosts
            request.session.set_expiry(10)
        
        forward_interface[device] = interfaces 
    content={
        'form' : form,
        'forward_interfaces' : forward_interface,
        "path":"manager",
        "title": 'new eth-to-eth',
        "projects" : projects,
    }    
    return render(request, 'manager/pseudowire/new/addpseudo.html',content)  



def int_pseudo(request, int_pseudo):
    pseudo = Pseudowire.objects.get(id = vrf_id)
    device_pseudo = vrf.devices.all()
    projects = Topologies.objects.order_by("id").reverse()[:2]
    if request.method =="POST":
        for device in device_vrf:
            interface_fors = request.POST["int"+device.name]
            network = request.POST["net"+device.name]
            mask = request.POST["mask"+device.name]
            config_commands = [
                    "interface "+interface_fors,
                    "ip vrf forwarding "+vrf.name,
                    "ip address " +network + " "+mask,
                    "no shutdown ",
                ]
            device.config_device(config_commands=config_commands)
        return HttpResponseRedirect("/manager/vrf/vrfrouting/"+str(vrf.id))        
    content={
        "devices" : device_vrf,
        "forward_interfaces" : forward_interface,
        'title': "interface provider edge",
        'path': "manager",
        "projects" : projects
    }
    return render(request,"manager/vrf/edit/vrfforward.html",content)



def vpls(request):
    pseudos = Vpls.objects.all()
    number = pseudos.count()
    
    content = {
        "vpls" : pseudos,
        "number" : number,
        "path":"manager",
        "title": 'pseudowire eth-to-eth',
    }    
    return render(request,"manager/vpls/indexvpls.html", content)


def add_vpls(request):
    devices = Device.objects.all()
    if request.method=='POST':
        form = VplsForm(request.POST)
        description = request.POST["description"]
        vcid = request.POST["vcid"]
        for device in devices:
            inter = request.POST["int"+device.name]
            if vcid != "":
                config_commands=[
                    "interface "+inter,
                ]
                return HttpResponse("ok")
        
    forward_interface = {}
    interfaces = {}
    hosts =""
    for device in devices:
        driver = get_network_driver(device.napalm_driver)
        host = device.host
        username = device.username
        password = device.password
        try:
            with driver(host, username, password, optional_args={}) as device_run:
                interfaces = device_run.get_interfaces()
        except Exception as e:
            hosts = hosts + host +", "
            print(e)
            request.session['error'] = "deosn't connected of device : "+hosts
            request.session.set_expiry(10)
        
        forward_interface[device] = interfaces
    form = VplsForm()       
    content={
        "form" : form,
        "devices" : devices,
        "forward_interfaces" : forward_interface,
        'title': "interface provider edge",
    }
    return render(request,"manager/vpls/new/addvpls.html",content)


def int_vpls(request,vpls_id):
    return HttpResponse("hello")



def config_device(params, **config_commands):
    device = None
    try:
        with ConnectHandler(params) as device_conf:
            device = device_conf.send_config_set(config_commands)
    except Exception as e:
        print(e) 
    return device