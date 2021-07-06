# Generated by Django 3.2.4 on 2021-07-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_on', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('status', models.CharField(blank=True, choices=[('y', 'yes'), ('n', 'no')], default='n', help_text='Approval status by librarian', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='about',
            field=models.TextField(blank=True, default='NULL', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='code',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]