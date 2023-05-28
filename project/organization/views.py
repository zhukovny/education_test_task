from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Department
from .models import Employee
from .serializers import DepartmentSerializer
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        department_id = request.query_params.get('department_id')
        last_name = request.query_params.get('last_name')

        queryset = Employee.filter_objects(department_id, last_name)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = EmployeeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
