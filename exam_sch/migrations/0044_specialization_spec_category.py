# Generated by Django 4.2.7 on 2023-12-06 05:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam_sch", "0043_electives_studentenrollment_elec"),
    ]

    operations = [
        migrations.AddField(
            model_name="specialization",
            name="spec_category",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
