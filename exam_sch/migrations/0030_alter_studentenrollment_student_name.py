# Generated by Django 4.2.7 on 2023-11-22 05:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam_sch", "0029_studentenrollment_student_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentenrollment",
            name="student_name",
            field=models.CharField(editable=False, max_length=100),
        ),
    ]
