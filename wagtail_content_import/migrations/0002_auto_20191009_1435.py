# Generated by Django 2.1.8 on 2019-10-09 13:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_content_import", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="oauthcredentials",
            name="user",
        ),
        migrations.DeleteModel(
            name="OAuthCredentials",
        ),
    ]
