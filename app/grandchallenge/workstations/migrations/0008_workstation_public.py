# Generated by Django 3.0.2 on 2020-02-13 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workstations", "0007_auto_20200121_1554"),
    ]

    operations = [
        migrations.AddField(
            model_name="workstation",
            name="public",
            field=models.BooleanField(
                default=False,
                help_text="If True, all logged in users can use this workstation, otherwise, only the users group can use this workstation.",
            ),
        ),
    ]