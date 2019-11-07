# Generated by Django 2.2.4 on 2019-11-04 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_app', '0031_auto_20191101_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='type',
            field=models.CharField(choices=[('cane', 'cane'), ('cane, quad', 'cane, quad'), ('commode', 'commode'), ('compression brace', 'compression brace'), ('crutch, adult', 'crutch, adult'), ('crutch, pediatric', 'crutch, pediatric'), ('forearm crutch, adult', 'forearm crutch, adult'), ('forearm crutch, pediatric', 'forearm crutch, pediatric'), ('knee injury scooter', 'knee injury scooter'), ('medical boot, adult', 'medical boot adult'), ('medical boot, pediatric', 'medical boot, pediatric'), ('miscellaneous', 'miscellaneous'), ('orthotic brace, adult', 'orthotic brace adult'), ('orthotic brace, pediatric', 'orthotic brace, pediatric'), ('orthotic shoe, adult', 'orthotic shoe, adult'), ('orthotic shoe, pediatric', 'orthotic shoe, pediatric'), ('shower chair, tub-attachable', 'shower chair, tub-attachable'), ('showerchair', 'shower chair'), ('sling', 'sling'), ('splint', 'splint'), ('splint', 'wrist splint'), ('walker, four-wheeled', 'walker, four-wheeled'), ('walker, non-wheeled', 'walker, non-wheeled'), ('walker, three-wheeled', 'walker, three-wheeled'), ('walker, two-wheeled', 'walker, two-wheeled'), ('wheelchair, active-manual', 'wheelchair, active-manual'), ('wheelchair, pediatric', 'wheelchair, pediatric'), ('wheelchair, seat cushion', 'wheelchair, seat cushion'), ('wheelchair, standard', 'wheelchair, standard')], max_length=47),
        ),
        migrations.AlterField(
            model_name='equipmentvalue',
            name='device_type',
            field=models.CharField(choices=[('cane', 'cane'), ('cane, quad', 'cane, quad'), ('commode', 'commode'), ('compression brace', 'compression brace'), ('crutch, adult', 'crutch, adult'), ('crutch, pediatric', 'crutch, pediatric'), ('forearm crutch, adult', 'forearm crutch, adult'), ('forearm crutch, pediatric', 'forearm crutch, pediatric'), ('knee injury scooter', 'knee injury scooter'), ('medical boot, adult', 'medical boot adult'), ('medical boot, pediatric', 'medical boot, pediatric'), ('miscellaneous', 'miscellaneous'), ('orthotic brace, adult', 'orthotic brace adult'), ('orthotic brace, pediatric', 'orthotic brace, pediatric'), ('orthotic shoe, adult', 'orthotic shoe, adult'), ('orthotic shoe, pediatric', 'orthotic shoe, pediatric'), ('shower chair, tub-attachable', 'shower chair, tub-attachable'), ('showerchair', 'shower chair'), ('sling', 'sling'), ('splint', 'splint'), ('splint', 'wrist splint'), ('walker, four-wheeled', 'walker, four-wheeled'), ('walker, non-wheeled', 'walker, non-wheeled'), ('walker, three-wheeled', 'walker, three-wheeled'), ('walker, two-wheeled', 'walker, two-wheeled'), ('wheelchair, active-manual', 'wheelchair, active-manual'), ('wheelchair, pediatric', 'wheelchair, pediatric'), ('wheelchair, seat cushion', 'wheelchair, seat cushion'), ('wheelchair, standard', 'wheelchair, standard')], max_length=25),
        ),
    ]
