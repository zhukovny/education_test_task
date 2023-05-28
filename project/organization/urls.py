from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DepartmentViewSet
from .views import EmployeeDetailViewSet
from .views import EmployeeListViewSet


employee_list = EmployeeListViewSet.as_view({
    'get': 'list',
})


employee_detail = EmployeeDetailViewSet.as_view({
    'post': 'create',
    'delete': 'destroy',
})


department_api = DepartmentViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    path('employees/', employee_list, name='employee-list'),
    path('employees/<str:last_name>', employee_list, name='employee-list'),
    path('employees/<int:department_id>', employee_list, name='employee-list'),
    path('employees/', employee_detail, name='employee-detail'),
    path('employees/<int:pk>', employee_detail, name='employee-detail'),
    path('departments/', department_api, name='department-api'),
]
