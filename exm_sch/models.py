from django.db import models


class Department(models.Model):
    DEPT_CHOICES = [
        ('Ol', 'Online Learning'),
        ('Odl', 'Open and Distance Learning'),
        ('Regular', 'Regular Classroom'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=20, choices=DEPT_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return self.dept_name
