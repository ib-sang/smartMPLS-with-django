from django import forms
from django.forms import ModelForm, Textarea, TextInput, ModelMultipleChoiceField
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from .models import *

CHOICES_TYPE =[
    ('router' , 'Router'), ('switch', 'Switch'),
    ('firewall', 'Firewall')    
]

CHOICES_PLATEFORM = [
    ('cisco_ios', 'CISCO IOS'), 
    ('cisco_iosxe', 'CISCO IOS XE')
]


CHOICES_PROTOCOL = [
    ('eigrp', 'EIGRP'),
    ('ospf', 'OSPF'),
    ('bgp', 'BGP'),
]

class AddVRFForm(forms.Form):
    name = forms.CharField(label='name',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"name for customer","name":"name","type":"text"}))
    rd = forms.CharField(label='rd', widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"rd","type":"text","value":""}))
    routeImport = forms.CharField(label='route import',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"routeImport","type":"text","value":""}))
    routeExport = forms.CharField(label='route export',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"routeExport","type":"text","value":""}))




class AddDeviceForm(forms.Form):
    name = forms.CharField(label='name',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"name for customer","name":"name","type":"text"}))
    host = forms.CharField(label='rd', widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"rd","type":"text","value":""}))
    device_type = forms.ChoiceField(widget=forms.Select( ), label='device_type', choices=CHOICES_TYPE, initial="router", required=True, )
    plateform = forms.ChoiceField(label='plateform', choices=CHOICES_PLATEFORM,  initial="cisco_ios", required=True)
    management = forms.ModelChoiceField(queryset = Access.objects.all())
    topology_ref = forms.ModelChoiceField(queryset = Topologies.objects.all())



class AccessForm(forms.ModelForm):
    
    class Meta:
        model = Access
        fields = ["username", "password"]
        widgets = {
        'username': forms.TextInput(attrs={'class':'form-control'}),
        'password': forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
    
        } 
      
      
class TopologyForm(forms.ModelForm):
    
    class Meta:
        model = Topologies
        fields = ["name", "description"] 
        widgets = {
            "name" : forms.TextInput(attrs={'class':'form-control'}),
            "description" :  forms.Textarea(attrs={'class':'form-control','rows': 10}),
        }  
      

class DeviceForm(forms.ModelForm):
    
    class Meta:
        model = Device
        fields = ["name", "host", "device_type", "plateform",  "management", "topology_ref"] 
        widgets = {
            "name" : forms.TextInput(attrs={'class':'form-control'}),
            "host" :  forms.TextInput(attrs={'class':'form-control mb-4'}),
        }  
        widget = {
            'device_type' : forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control" } ), label='device_type', choices=CHOICES_TYPE, initial="router", required=True, ),
            "protocol" : forms.ChoiceField(label='protocol backbone ', choices=CHOICES_PROTOCOL,  initial="bgp", required=True),            
            "plateform" : forms.ChoiceField(label='plateform', choices=CHOICES_PLATEFORM,  initial="cisco_ios", required=True),
            "management" : forms.ModelChoiceField(queryset=Access.objects.all()),
            "topology_ref" : forms.ModelChoiceField(queryset=Topologies.objects.all(),widget=forms.Select(attrs={"class":"form-control" } )),
        }
      

class VRFForm(forms.ModelForm):
    
    class Meta:
        model = Vrf
        fields = ["name", "rd", "routeImport", "routeExport", "devices"]
        widgets = {
                    "name" : forms.TextInput(attrs={'class':'form-control'}),
                    "rd" :  forms.TextInput(attrs={'class':'form-control '}),
                    "routeImport" :  forms.TextInput(attrs={'class':'form-control '}),
                    "routeExport" :  forms.TextInput(attrs={'class':'form-control '}),
                }
        widget = {
            "devices" : forms.ModelMultipleChoiceField(queryset = Access.objects.all()),
        } 
