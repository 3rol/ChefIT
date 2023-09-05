# Generated by Django 4.2.4 on 2023-09-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='recipe_type',
            name='name',
            field=models.TextField(max_length=200),
        ),
    ]
