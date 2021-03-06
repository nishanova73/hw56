# Generated by Django 4.0.2 on 2022-02-07 06:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='other', max_length=15)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('detailed_description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='detailed_description')),
                ('remainder', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='webapp.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'good',
                'verbose_name_plural': 'goods',
                'db_table': 'Goods',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remainder', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good', to='webapp.good', verbose_name='Good')),
            ],
            options={
                'verbose_name': 'basket',
                'verbose_name_plural': 'baskets',
                'db_table': 'Basket',
            },
        ),
    ]
