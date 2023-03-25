# Generated by Django 2.2.6 on 2019-11-27 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_avatar'),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredients',
            old_name='Ingdescript',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='ingredients',
            old_name='Ingname',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='ingredients',
            name='Ingquantity',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='rcp_imgurl',
        ),
        migrations.AddField(
            model_name='ingredients',
            name='rcpId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='rcp_img',
            field=models.ImageField(default='#', upload_to='recipes/'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_view',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipestep',
            name='rcpId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe'),
        ),
        migrations.AddField(
            model_name='recipestep',
            name='stepImg',
            field=models.ImageField(default='#', upload_to='recipes/'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cateid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Category'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='rcp_descript',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tasteid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Taste'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
                ('video', models.FileField(upload_to='videos/')),
                ('cover', models.ImageField(upload_to='videos/')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]