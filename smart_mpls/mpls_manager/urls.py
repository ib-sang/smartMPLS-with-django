from django.urls import path

from . import views

urlpatterns = [
    path('devices', views.devices, name='devices'),
    path('device/vrf/<int:device_id>', views.add_vrf, name='add_vrf'),
    #path('allvrf/<int:device_id>', views.get_vrf, name='all_vrf'),
    #path('api/task/<str:task_id>', views.get_task_status, name="task_status"),
]