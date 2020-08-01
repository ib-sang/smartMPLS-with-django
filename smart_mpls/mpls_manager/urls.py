from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manager', views.index_manager, name='index_manager'),
    path('manager/accesses', views.accesses, name='accesses'),
    path('manager/access/edit/<int:access_id>', views.edit_access, name='edit_access'),
    path('manager/access/add', views.add_access, name='add_access'),
    path('manager/access/delete/<int:access_id>', views.del_access, name='del_access'),
    path('manager/topology', views.topology, name='topo'), 
    path('manager/topology/add', views.add_topo, name='add_topo'),
    path('manager/topology/edit/<int:topo_id>', views.edit_topo, name='edit_topo'),
    path('manager/topology/delete/<int:topo_id>', views.del_topo, name='del_topo'),
    path('manager/device', views.device, name='device'),
    path('manager/device/add', views.add_device, name='add_device'),
    path('manager/device/edit/<int:device_id>', views.edit_device, name='edit_device'),
    path('manager/device/delete/<int:device_id>', views.del_device, name='del_device'),
    path('manager/vrf', views.vrf, name='vrf'),
    path('manager/vrf/add', views.add_vrf, name='add_vrf'),
    path('manager/vrf/forwarding/<int:vrf_id>', views.in_vrf, name='int_vrf'),
    path('manager/vrf/vrfrouting/<int:vrf_id>', views.routing_vrf, name='routing_vrf'),
    path('manager/vrf/delete/<int:vrf_id>', views.del_vrf, name='del_vrf'),
    path('manager/pseudowire', views.pseudo, name='pseudo'),
    path('manager/pseudowire/add', views.add_pseudo, name='add_pseudo'),
    path('manager/pseudowire/interface/<int:pseudo_id>', views.int_pseudo, name='int_pseudo'),
    
    path('manager/vpls', views.vpls, name='vpls'),
    path('manager/vpls/add', views.add_vpls, name='add_vpls'),
    path('manager/vpls/interface/<int:vpls_id>', views.int_vpls, name='int_vpls'),

    path('manager/device/vrf/<int:device_id>', views.add_vrf_device, name='add_vrf_device'),

    #path('allvrf/<int:device_id>', views.get_vrf, name='all_vrf'),
    #path('api/task/<str:task_id>', views.get_task_status, name="task_status"),
]