# Generated by Django 4.2.5 on 2023-11-07 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exam_sch", "0018_semester"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="semester",
            name="semester_code",
        ),
    ]
