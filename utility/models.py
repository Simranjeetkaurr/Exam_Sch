from django.db import models

class Department(models.Model):
    DEPT_CHOICES = (
        ('ol', 'Online'),
        ('odl', 'Online-Distance Learning'),
        ('regular', 'Regular'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=10, choices=DEPT_CHOICES)
    dept_status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.dept_name

class Session(models.Model):
    MONTH_CHOICES = (
        ('Jan', 'January'),
        ('Jul', 'July'),
    )

    id = models.CharField(max_length=7, primary_key=True)
    year = models.PositiveIntegerField()
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    session_id = models.CharField(max_length=7)

    def save(self, *args, **kwargs):
        # Generate the session_id as a combination of month and year
        self.session_id = f'{self.month}{self.year}'
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_month_display()} {self.year}'
