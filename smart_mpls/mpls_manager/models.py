from django.db import models
from napalm import get_network_driver
from netmiko import ConnectHandler
from django.contrib import admin
# Create your models here.



NAPALM_MAPPING={
    'cisco_ios':'ios',
    'cisco_xe':'iosxe'
}


NETMIKO_MAPPING={
    'cisco_ios':'ios',
    'cisco_xe':'iosxe'
}



class Topologies(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)   
    
    def __str__(self):
        return self.name
 
 
class Access(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username
    
    
class Device(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=70)
    device_type = models.CharField(max_length=30, choices={('router' , 'Router'), ('switch', 'Switch'),
     ('firewall', 'Firewall') ,}, default="router", blank=True)
    plateform = models.CharField(max_length=30, choices={('cisco_ios', 'CISCO IOS'), 
    ('cisco_iosxe', 'CISCO IOS XE')}, default="cisco_ios", blank=True)
    management =  models.ForeignKey(Access, on_delete=models.CASCADE, null=True)
    topology_ref =  models.ForeignKey(Topologies, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

        
    def napalm_driver(self):
        return NAPALM_MAPPING[self.plateform]


    def netmiko_device_type(self) :
        return NETMIKO_MAPPING[self.plateform]

    @property
    def username(self) -> str:
        return self.management.username
    
    @property
    def password(self):
        return self.management.password
    
    def netmiko_connect(self):
        return ConnectHandler(self.napalm_driver, ip=self.host,
                              username=self.management.username,
                               password=self.management.password)
       
    @property    
    def connect(self):
        driver = get_network_driver(self.napalm_driver)
        device = None
        try:
            device = driver(self.host, self.management.username,
                            self.management.password, timeout=180)
            device.open()
        except Exception as e:
            print(e)
        return device


        
    @property
    def vrf_ip_interface(self):
        leng= len(output)
        i = 4
        js={}
        while i< leng:
    
            js[output[i]] = {
                "ip-address" : output[i+1],
                "vrf" : output[i+2],
                "protocol" : output[i+3]
            }
            
            i=i+4    
        return js    
 

    
class Interface(models.Model):
    name = models.CharField(max_length=255)
    ingress = models.BooleanField(default=False)
    egress = models.BooleanField(default=False)
    backbone = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.name
    
    
class Vrf(models.Model):
    name = models.CharField(max_length=100)
    rd = models.CharField(max_length=255)
    routeImport = models.CharField(max_length=255)
    routeExport = models.CharField(max_length=255)
    devices = models.ManyToManyField(Device, related_name='device', blank=True)

    @property
    def __str__(self):
        return self.name  
    
      
           