# Generated by Django 3.2.18 on 2023-10-27 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_gadget_missing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='matric_no',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Matric number / Staff ID'),
        ),
        migrations.AddField(
            model_name='gadget',
            name='missing_date',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.CharField(blank=True, choices=[('mass_com', 'Mass Communication'), ('info_tech', 'Information Technology'), ('interel', 'International Relations'), ('med_lab', 'Medical Laboratory Sciences'), ('accounting', 'Accounting'), ('pol_sci', 'Political Science'), ('nursing', 'Nursing Sciences'), ('bus_admin', 'Business Administration'), ('econs', 'Economics'), ('b_tech', 'B-Tech'), ('marketing', 'Marketing'), ('micro_bio', 'Micobiology'), ('bio_tech', 'BioTechnology'), ('comp_sci', 'Computer Science')], max_length=50, null=True),
        ),
    ]