# Generated by Django 5.2.4 on 2025-07-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.CharField(choices=[('😡', '😡'), ('😞', '😞'), ('😐', '😐'), ('😊', '😊'), ('😍', '😍')], default='😊', max_length=2),
        ),
    ]
