from django.urls import path

from . import views

urlpatterns = [
    path('devices', views.devices, name='devices'),
    path('interface', views.interface, name='interface'),
    path('device/<int:device_id>', views.get_device_stats, name='device'),
    path('allvrf', views.get_vrf, name='all_vrf'),
    path('test', views.test, name='test'),
    #path('api/task/<str:task_id>', views.get_task_status, name="task_status"),
]