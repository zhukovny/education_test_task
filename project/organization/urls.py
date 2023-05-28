from django.urls import path

from .views import DepartmentViewSet
from .views import EmployeeViewSet


employee_list = EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})


department_list = DepartmentViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    path('employees/', employee_list, name='employee-list'),
    path('departments/', department_list, name='department-list'),
]
