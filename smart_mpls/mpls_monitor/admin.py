from django.contrib import admin

# Register your models here.
from .models import Device
from .models import Interface
from .models import Topologies
from .models import Vrf

admin.site.register(Device)
admin.site.register(Interface)
admin.site.register(Topologies)
admin.site.register(Vrf)
