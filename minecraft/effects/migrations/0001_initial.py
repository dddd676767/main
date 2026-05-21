import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('versions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effect_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(blank=True, max_length=100)),
                ('numeric_id_je', models.IntegerField(blank=True, null=True)),
                ('numeric_id_be', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('versions', models.ManyToManyField(related_name='effects', to='versions.minecraftversion')),
            ],
            options={
                'verbose_name': 'Эффект',
                'verbose_name_plural': 'Эффекты',
            },
        ),
    ]
