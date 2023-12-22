# Generated by Django 4.2.7 on 2023-12-20 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("exam_sch", "0068_alter_slot_slot_list"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpecSlot",
            fields=[
                ("slot_id", models.AutoField(primary_key=True, serialize=False)),
                ("slot_list", models.TextField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_sch.session",
                    ),
                ),
                (
                    "spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_sch.specialization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ElecSlot",
            fields=[
                ("slot_id", models.AutoField(primary_key=True, serialize=False)),
                ("slot_list", models.TextField()),
                (
                    "elec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_sch.electives",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_sch.session",
                    ),
                ),
            ],
        ),
    ]
