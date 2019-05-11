from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentelella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'login.html', views.login_user, name='login'),
    re_path(r'dash_sensor.html', views.dash_sensor, name='dash_sensor'),
    re_path(r'dash_ubicacion.html', views.dash_ubicacion, name='dash_ubicacion'),
    re_path(r'^.*\.html', views.gentelella_html, name='gentelella'),
    

    # The home page
    path('', views.index, name='index'),
]
