# Generated by Django 3.2.18 on 2023-08-10 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('matric_no', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Matric number')),
                ('staff_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('user_type', models.CharField(blank=True, choices=[('student', 'Student'), ('staff', 'Staff'), ('vendor', 'Vendor')], default='staff', max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='email address')),
                ('phone_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone number')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('level', models.CharField(blank=True, choices=[('JUPEB', 'JUPEB'), ('100', '100L'), ('200', '200L'), ('300', '300L'), ('400', '400L'), ('500', '500L')], max_length=50, null=True)),
                ('department', models.CharField(blank=True, choices=[('mass_com', 'Mass Communication'), ('info_tech', 'Information Technology'), ('interel', 'International Relations'), ('med_lab', 'Medical Laboratory Sciences'), ('accounting', 'Accounting'), ('pol_sci', 'Political Science'), ('nursing', 'Nursing Sciences'), ('bus_admin', 'Business Administration'), ('econs', 'Economics'), ('marketing', 'Marketing'), ('micro_bio', 'Micobiology'), ('bio_tech', 'BioTechnology')], max_length=50, null=True)),
                ('picture', models.FileField(blank=True, null=True, upload_to='user_pictures')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gadget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=150, null=True)),
                ('color', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.CharField(blank=True, choices=[('missing', 'Missing'), ('available', 'Available')], max_length=50, null=True)),
                ('device_id', models.CharField(blank=True, max_length=500, null=True)),
                ('picture', models.FileField(blank=True, null=True, upload_to='gadgets_pictures')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
