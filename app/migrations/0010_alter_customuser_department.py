# Generated by Django 3.2.18 on 2023-10-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_customuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.CharField(blank=True, choices=[('mass_com', 'Mass Communication'), ('info_tech', 'Information Technology'), ('interel', 'International Relations'), ('med_lab', 'Medical Laboratory Sciences'), ('accounting', 'Accounting'), ('pol_sci', 'Political Science'), ('nursing', 'Nursing Sciences'), ('bus_admin', 'Business Administration'), ('econs', 'Economics'), ('computing', 'Computing'), ('marketing', 'Marketing'), ('micro_bio', 'Micobiology'), ('bio_tech', 'BioTechnology'), ('comp_sci', 'Computer Science')], max_length=50, null=True),
        ),
    ]
