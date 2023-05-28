import json
from http import HTTPStatus

from django.contrib.auth.models import User
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
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))


class TestEmployeeViewSet(TestCase):
    uri = '/organization/employees/'

    def test_get_employees_list_forbidden_for_not_authenticated(self):
        # Arrange
        expected_status = HTTPStatus.FORBIDDEN

        # Act
        response = self.client.get(self.uri)

        # Assert
        self.assertEqual(response.status_code, expected_status)

    def test_get_list_paginated(self):
        # Arrange
        department = Department.objects.create(name='main_department')

        for i in range(10):
            Employee.objects.create(
                **{
                    'name': f'Employee #{i}',
                    'photo': None,
                    'position': 'dev',
                    'salary': 100500,
                    'age': 30,
                    'department_id': department.id
                }
            )

        expected_data_count = 10
        expected_results_count = 3

        username = 'testuser'
        password = '12345'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # Act
        response = self.client.get(self.uri + '?limit=7&offset=7')

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['count'], expected_data_count)
        self.assertEqual(len(response.data['results']), expected_results_count)

    def test_get_list_filter_by(self):
        # Arrange
        it_department = Department.objects.create(name='IT Department')
        accounting_department = Department.objects.create(name='Accounting Department')

        employee_1 = Employee.objects.create(
            **{
                'name': 'Pupa Pupin',
                'photo': None,
                'position': 'Dev',
                'salary': 100500.65,
                'age': 20,
                'department_id': it_department.id
            }
        )
        employee_2 = Employee.objects.create(
            **{
                'name': 'Lupa Lupin',
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

        parameters = [
            (
                f'{self.uri}?department_id={it_department.id}',
                [
                    {
                        'id': employee_1.id,
                        'name': 'Pupa Pupin',
                        'photo': None,
                        'position': 'Dev',
                        'salary': '100500.65',
                        'age': 20,
                        'department_id': 1,
                    },
                    {
                        'id': employee_2.id,
                        'name': 'Lupa Lupin',
                        'photo': None,
                        'position': 'Dev',
                        'salary': '500100.10',
                        'age': 20,
                        'department_id': 1,
                    }
                ]
            ),
            (
                f'{self.uri}?last_name=Mihailovna',
                [
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
            ),
            (
                f'{self.uri}?department_id={it_department.id}&last_name=Lupin',
                [
                    {
                        'id': employee_2.id,
                        'name': 'Lupa Lupin',
                        'photo': None,
                        'position': 'Dev',
                        'salary': '500100.10',
                        'age': 20,
                        'department_id': 1,
                    }
                ],
            ),
            (
                f'{self.uri}?department_id={accounting_department.id}&last_name=Pupin',
                [],
            ),
        ]

        username = 'testuser'
        password = '12345'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # Act
        for uri, expected_data in parameters:
            with self.subTest(uri=uri, expected_data=expected_data):
                response = self.client.get(uri)

                # Assert
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(response.data, expected_data)

    def test_create_employee(self):
        # Arrange
        accounting_department = Department.objects.create(name='Accounting Department')

        data = {
            'name': 'Nina Mihailovna',
            'photo': '',
            'position': 'Buhgalter',
            'salary': 10000000.7,
            'age': 49,
            'department_id': accounting_department.id
        }

        username = 'testuser'
        password = '12345'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # Act
        response = self.client.post(self.uri, data)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        employee = Employee.objects.filter(name='Nina Mihailovna').first()
        self.assertIsNotNone(employee)

    def test_destroy_employee(self):
        # Arrange
        accounting_department = Department.objects.create(name='Accounting Department')

        data = {
            'name': 'Nina Mihailovna',
            'photo': '',
            'position': 'Buhgalter',
            'salary': 10000000.7,
            'age': 49,
            'department_id': accounting_department.id
        }
        employee = Employee.objects.create(**data)

        username = 'testuser'
        password = '12345'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # Act
        response = self.client.delete(f'{self.uri}?pk={employee.id}')

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        employee = Employee.objects.filter(name='Nina Mihailovna').first()
        self.assertIsNone(employee)
