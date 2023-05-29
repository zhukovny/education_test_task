from typing import Optional

from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    director = models.OneToOneField(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="directed_department",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def get_employees_count(self) -> int:
        return self.employees.count()

    def get_salary_summary(self) -> float:
        return self.employees.aggregate(Sum("salary"))["salary__sum"]


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="employee_photos", null=True, blank=True)
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.PositiveIntegerField()
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )

    class Meta:
        unique_together = ("id", "department")
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    @classmethod
    def filter_objects(
        cls, department_id: Optional[int], last_name: Optional[str]
    ) -> QuerySet:
        if department_id and last_name:
            return cls.objects.filter(department_id=int(department_id)).filter(
                last_name__contains=last_name
            )

        if department_id:
            return cls.objects.filter(department_id=int(department_id))

        if last_name:
            return cls.objects.filter(last_name__contains=last_name)

        return Employee.objects.all()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
