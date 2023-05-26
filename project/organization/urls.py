from django.urls import path

from . import views
from .views import EmployeeViewSet


employee_list = EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


urlpatterns = [
    path('', views.index, name='index'),
    path('employees/', employee_list, name='employee-list'),
]
