# Generated by Django 4.2.7 on 2023-11-22 07:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("exam_sch", "0030_alter_studentenrollment_student_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user_table",
            old_name="user_id",
            new_name="userid",
        ),
    ]
