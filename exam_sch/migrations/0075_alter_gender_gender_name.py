# Generated by Django 4.2.7 on 2023-12-21 05:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam_sch", "0074_alter_slot_slot_id_alter_slot_slot_list_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gender",
            name="gender_name",
            field=models.CharField(
                choices=[("Male", "male"), ("Female", "female"), ("Other", "other")],
                max_length=12,
                unique=True,
            ),
        ),
    ]