from django.db import models
from django.db.models import Sum


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    director = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        related_name='directed_department',
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_employees_count(self):
        return self.employees.count()

    def get_salary_summary(self):
        return self.employees.aggregate(Sum('salary'))['salary__sum']


class Employee(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employee_photos', null=True, blank=True)
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')

    class Meta:
        unique_together = ('name', 'department')

    @classmethod
    def filter_by_last_name(cls, last_name):
        return cls.objects.filter(name__endswith=last_name)

    def __str__(self):
        return self.name
