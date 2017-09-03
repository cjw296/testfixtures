from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='samplemodel',
            name='foreign_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_django.OtherModel'),
            preserve_default=False,
        ),
    ]
