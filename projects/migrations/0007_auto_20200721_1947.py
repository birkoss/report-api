# Generated by Django 3.0.8 on 2020-07-21 23:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_entry_entrylevel_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='entry',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Folder'),
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
