from django.urls import path

from .views import DepartmentViewSet
from .views import EmployeeListViewSet


employee_list = EmployeeListViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})


department_api = DepartmentViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    path('employees/', employee_list, name='employee-list'),
    path('departments/', department_api, name='department-api'),
]
