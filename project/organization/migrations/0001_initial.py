# Generated by Django 4.2.1 on 2023-05-29 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="employee_photos"
                    ),
                ),
                ("position", models.CharField(max_length=50)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("age", models.PositiveIntegerField()),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="organization.department",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="director",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="directed_department",
                to="organization.employee",
            ),
        ),
        migrations.AddIndex(
            model_name="employee",
            index=models.Index(
                fields=["last_name", "first_name"],
                name="organizatio_last_na_ee7bda_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="employee",
            unique_together={("id", "department")},
        ),
    ]
