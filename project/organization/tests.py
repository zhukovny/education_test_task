import json

from django.test import TestCase

from .models import Department
from .models import Employee


class TestDepartmentViewSet(TestCase):
    uri = '/organization/departments/'

    def test_get_list(self):
        # Arrange
        it_department = Department.objects.create(name='IT Department')
        accounting_department = Department.objects.create(name='Accounting Department')

        employee_1 = Employee.objects.create(
            **{
                'name': 'Pupa',
                'photo': None,
                'position': 'Dev',
                'salary': 100500.65,
                'age': 20,
                'department_id': it_department.id
            }
        )
        employee_2 = Employee.objects.create(
            **{
                'name': 'Lupa',
                'photo': None,
                'position': 'Dev',
                'salary': 500100.10,
                'age': 20,
                'department_id': it_department.id
            }
        )
        employee_3 = Employee.objects.create(
            **{
                'name': 'Nina Mihailovna',
                'photo': None,
                'position': 'Buhgalter',
                'salary': 10000000.7,
                'age': 49,
                'department_id': accounting_department.id
            }
        )

        expected_data = [
            {
                'id': it_department.id,
                'name': 'IT Department',
                'director': None,
                'employees_count': 2,
                'salary_summary': f'{employee_1.salary + employee_2.salary}',
                'employees': [
                    {
                        'id': employee_1.id,
                        'name': 'Pupa',
                        'photo': None,
                        'position': 'Dev',
                        'salary': '100500.65',
                        'age': 20,
                        'department_id': 1,
                    },
                    {
                        'id': employee_2.id,
                        'name': 'Lupa',
                        'photo': None,
                        'position': 'Dev',
                        'salary': '500100.10',
                        'age': 20,
                        'department_id': 1,
                    }
                ],
            },
            {
                'id': accounting_department.id,
                'name': 'Accounting Department',
                'director': None,
                'employees_count': 1,
                'salary_summary': '10000000.70',
                'employees': [
                    {
                        'id': employee_3.id,
                        'name': 'Nina Mihailovna',
                        'photo': None,
                        'position': 'Buhgalter',
                        'salary': '10000000.70',
                        'age': 49,
                        'department_id': 2,
                    },
                ],
            }
        ]

        # Act
        response = self.client.get(self.uri)

        # Assert
        self.maxDiff = None
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))
