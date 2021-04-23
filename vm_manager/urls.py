from django.urls import path

from . import views

app_name = 'vm_manager'

urlpatterns = [

    path('', views.ManagerView.as_view(), name='manager'),

]

