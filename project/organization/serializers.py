from rest_framework import serializers

from .models import Department
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'name',
            'photo',
            'position',
            'salary',
            'age',
            'department',
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = [
            'name',
            'director',
            'employees',
        ]
