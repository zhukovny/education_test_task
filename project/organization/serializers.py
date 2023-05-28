from rest_framework import serializers

from .models import Department
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'photo',
            'position',
            'salary',
            'age',
            'department_id',
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(source='get_employees_count')
    salary_summary = serializers.DecimalField(source='get_salary_summary', max_digits=10, decimal_places=2)
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'director',
            'employees_count',
            'salary_summary',
            'employees',
        ]
