from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import permissions
from rest_framework import serializers
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
        department_id = self.request.query_params.get("department_id")
        last_name = self.request.query_params.get("last_name")
        return Employee.filter_objects(department_id, last_name)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="last_name",
                description="Filter by last_name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="department_id",
                description="Filter by department_id",
                required=False,
                type=int,
            ),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super(EmployeeListViewSet, self).list(request, args, kwargs)

    @extend_schema(
        request=inline_serializer(
            name="InlineCreateEmployeeSerializer",
            fields={
                "first_name": serializers.CharField(),
                "last_name": serializers.CharField(),
                "photo": serializers.ImageField(),
                "position": serializers.CharField(),
                "salary": serializers.DecimalField(max_digits=10, decimal_places=2),
                "age": serializers.IntegerField(),
                "department_id": serializers.IntegerField(),
            },
        ),
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(request.data)
        Employee.objects.create(**serializer.data)
        return Response()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="pk", description="Employee id", required=True, type=int
            ),
        ]
    )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        pks = request.query_params.get("pk", [])
        Employee.objects.filter(id__in=pks).delete()
        return Response()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
