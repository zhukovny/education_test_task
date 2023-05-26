from django.http import HttpResponse
from rest_framework import viewsets

from .models import Employee
from .serializers import EmployeeSerializer


def index(request):
    return HttpResponse("Test")


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
