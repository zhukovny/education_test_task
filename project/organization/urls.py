from django.urls import path

from .views import DepartmentViewSet
from .views import EmployeeViewSet


employee_api = EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})


department_api = DepartmentViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    path('employees/', employee_api, name='employee-api'),
    path('employees/<int:pk>', employee_api, name='employee-api'),
    path('employees/<str:last_name>', employee_api, name='employee-api'),
    path('employees/<int:department_id>', employee_api, name='employee-api'),
    path('departments/', department_api, name='department-api'),
]
