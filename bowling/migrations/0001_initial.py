# Generated by Django 2.0.5 on 2018-07-12 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstThrow', models.IntegerField(default=0)),
                ('secondThrow', models.IntegerField(default=0)),
                ('isSpare', models.BooleanField(default=False)),
                ('isStrike', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameId', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='frame',
            name='gameId',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='bowling.Game'),
        ),
    ]
