# Generated by Django 3.0.2 on 2020-05-09 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('creator', '0004_adventurecontainer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health', models.IntegerField(default=100)),
                ('checkPointSet', models.BooleanField(default=False)),
                ('checkPoint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='creator.Slide')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
