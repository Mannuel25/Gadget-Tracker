# Generated by Django 3.2.18 on 2023-10-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customuser_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gadget',
            name='picture',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.CharField(blank=True, choices=[('mass_com', 'Mass Communication'), ('info_tech', 'Information Technology'), ('interel', 'International Relations'), ('med_lab', 'Medical Laboratory Sciences'), ('accounting', 'Accounting'), ('pol_sci', 'Political Science'), ('nursing', 'Nursing Sciences'), ('bus_admin', 'Business Administration'), ('econs', 'Economics'), ('marketing', 'Marketing'), ('micro_bio', 'Micobiology'), ('bio_tech', 'BioTechnology'), ('comp_sci', 'Computer Science')], max_length=50, null=True),
        ),
    ]