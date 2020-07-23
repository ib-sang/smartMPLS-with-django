from django import forms

class AddVRFForm(forms.Form):
    name = forms.CharField(label='name',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"name for customer","name":"name","type":"text"}))
    rd = forms.CharField(label='rd', widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"rd","type":"text","value":""}))
    routeImport = forms.CharField(label='route import',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"routeImport","type":"text","value":""}))
    routeExport = forms.CharField(label='route export',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"asm:asm or a.b.c.d:asm","name":"routeExport","type":"text","value":""}))
