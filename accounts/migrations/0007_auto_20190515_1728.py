# Generated by Django 2.1.7 on 2019-05-15 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20190515_1728'),
        ('accounts', '0006_auto_20190515_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperature',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='temps', to='people.People'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='loving_people',
            field=models.ManyToManyField(related_name='loved', to='people.People'),
        ),
    ]