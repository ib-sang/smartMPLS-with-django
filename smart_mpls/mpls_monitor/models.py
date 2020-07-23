from django.db import models

# Create your models here.


NAPALM_MAPPING={
    'cisco_ios':'ios',
    'cisco_xe':'iosxe'
}


NETMIKO_MAPPING={
    'cisco_ios':'ios',
    'cisco_xe':'iosxe'
}


class Device(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=70)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=30, choices={('router' , 'Router'), ('switch', 'Switch'),
     ('firewall', 'Firewall') ,}, default="router", blank=True)
    plateform = models.CharField(max_length=30, choices={('cisco_ios', 'CISCO IOS'), 
    ('cisco_iosxe', 'CISCO IOS XE')}, default="cisco_ios", blank=True)

    def __str__(self) ->str:
        return self.name

    @property
    def napalm_driver(self)->str:
        return NAPALM_MAPPING[self.plateform]


    @property
    def netmiko_device_type(self)->str:
        return NETMIKO_MAPPING[self.plateform]

    @property
    def ingress(self):
            interfaces = Interface.objects.filter(ingress=True, device_ref=self)
            if interfaces is not None:
                return True
            else:
                return False

    @property
    def egress(self):
        interfaces = Interface.objects.filter(egress=True, device_ref=self)
        if interfaces is not None:
            return True
        else:
            return False

    @property
    def backbone(self):
        interfaces = Interface.objects.filter(wan=True, device_ref=self)
        if interfaces is not None:
            return True
        else:
            return False
        
class Access(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    


class Topologies(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)   
    
    def __str__(self):
        return self.name
    
    
class Interface(models.Model):
    name = models.CharField(max_length=255)
    ingress = models.BooleanField(default=False)
    device_ref = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    egress = models.BooleanField(default=False)
    backbone = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.name
    
    
class Vrf(models.Model):
    name = models.CharField(max_length=100)
    rd = models.CharField(max_length=255)
    routeImport = models.CharField(max_length=255)
    routeExport = models.CharField(max_length=255)

    @property
    def __str__(self):
        return self.name  
          