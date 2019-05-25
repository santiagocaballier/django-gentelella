from django.urls import path, re_path
from sensor import views

urlpatterns = [
    path('test/<str:_username>', views.test, name='test'),
    path('setdata/<str:_mac_address>/<int:_dataint>.<int:_datadec>',views.set_data,name='sensor_setdata'),
    path('refresh_graph/<str:_sensor_name>/', views.refresh_graph, name = 'refresh_graph')
    #path('test/', views.test, name='test')
    
]
