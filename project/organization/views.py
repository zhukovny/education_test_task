from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Department
from .models import Employee
from .serializers import DepartmentSerializer
from .serializers import EmployeeSerializer


class EmployeeListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = EmployeeSerializer

    def get_queryset(self) -> QuerySet:
        department_id = self.request.query_params.get('department_id')
        last_name = self.request.query_params.get('last_name')
        return Employee.filter_objects(department_id, last_name)

    def list(self, request, *args, **kwargs):
        return super(EmployeeListViewSet, self).list(request, args, kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(request.data)
        Employee.objects.create(**serializer.data)
        return Response()

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        pks = request.query_params.get('pk', [])
        Employee.objects.filter(id__in=pks).delete()
        return Response()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
