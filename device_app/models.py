from django.db import models
from django.urls import reverse
from django.forms.fields import DateField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# Create your models here.
class DonationHouse(models.Model):
    title=models.CharField(max_length=265,blank=False)
    street=models.CharField(max_length=265,blank=False)
    city=models.CharField(max_length=265,blank=False)
    state=models.CharField(max_length=2,blank=False)
    zip=models.IntegerField(blank=False,validators=[
                            MaxValueValidator(99999),
                            MinValueValidator(1)])

    def __str__(self):
        return self.title


class Donor(models.Model):
    import datetime
    name=models.CharField(max_length=265,blank=False)
    email=models.EmailField(max_length=265,blank=False)
    donation_date=models.DateField(("Date"), default=datetime.date.today)
    donation_house=models.ForeignKey(DonationHouse,
                                     default='1',
                                     related_name='dono_house',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device_app:donor_detail',kwargs={'pk':self.pk})

class StorageArea(models.Model):
    title=models.CharField(max_length=265,blank=False)
    street=models.CharField(max_length=265,blank=False)
    city=models.CharField(max_length=265,blank=False)
    state=models.CharField(max_length=2,blank=False)
    zip=models.IntegerField(blank=False,
                            validators=[
                            MaxValueValidator(99999),
                            MinValueValidator(1)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('device_app:storage_detail',
                        kwargs={'pk':self.pk})

class Campaign(models.Model):
    title=models.CharField(max_length=265,
                           default='No Campaign',
                           blank=False)
    partnership=models.CharField(max_length=265,null=True,blank=True)
    organization_recipient=models.CharField(max_length=265,null=True,blank=True)
    start_date=models.DateField(blank=False)
    end_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.title

class Recipient(models.Model):
    man='MAN'
    woman='WOMAN'
    boy='BOY'
    girl='GIRL'
    non_binary='Non-Binary'
    RECIPIENT_OPTIONS = (
        (man,'man'),
        (woman,'woman'),
        (boy,'boy'),
        (girl,'girl'),
        (non_binary,'non_binary'),
    )
    first_name=models.CharField(max_length=265,blank=True)
    age=models.IntegerField(blank=True,
                            validators=[
                            MaxValueValidator(200),
                            MinValueValidator(1)])
    type=models.CharField(max_length=13,
                          choices=RECIPIENT_OPTIONS,blank=True)
    date_recieved=models.DateField(blank=True)
    campaign=models.ForeignKey(Campaign,
                              default='1',
                              related_name='campaign',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class Device(models.Model):
    import datetime
    ez_crutch='ez-crutch'
    crutch='crutch'
    walker='walker'
    wheelchair='wheelchair'
    medicalboot='medical boot'
    orthoticshoe='orthotic shoe'
    sling='sling'
    glasses='glasses'
    compressionbrace='compression brace'
    orthoticbrace='orthotic brace'
    splint='splint'
    wrap='wrap'
    bed='bed'
    miscellaneous='miscellaneous'
    A='A'
    B='B'
    C='C'
    Broken='BROKEN'
    DEVICE_CONDITIONS = (
        (A,'A'),
        (B,'B'),
        (C,'C'),
        (Broken,'Broken'),
    )

    DEVICE_OPTIONS = (
        (crutch,'crutch'),
        (ez_crutch,'EZ-crutch'),
        (walker,'walker'),
        (wheelchair,'wheelchair'),
        (medicalboot,'medical boot'),
        (orthoticshoe,'orthotic shoe'),
        (sling,'sling'),
        (glasses,'glasses'),
        (compressionbrace,'compression brace'),
        (orthoticbrace,'orthotic brace'),
        (splint,'splint'),
        (wrap,'wrap'),
        (bed,'bed'),
        (miscellaneous,'miscellaneous'),
    )

    type=models.CharField(max_length=25,choices=DEVICE_OPTIONS,blank=False)
    condition=models.CharField(max_length=10,choices=DEVICE_CONDITIONS,blank=False)
    donor=models.ForeignKey(Donor,
                            related_name='devices',
                            on_delete=models.CASCADE)
    storage_area=models.ForeignKey(StorageArea,
                            related_name='device_storage_area',
                            on_delete=models.CASCADE)
    campaign=models.ForeignKey(Campaign,
                              related_name='device_campaign',
                              on_delete=models.CASCADE)
    donated_to_recipient=models.BooleanField(default=False)
    cleaned=models.BooleanField(default=False)
    unique_information=models.TextField()
    date_donated_to_recipient=models.DateField(("Date Donated to Recipient (YYYY-MM-DD)"),
                                                blank=True,
                                                null=True)


    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('device_app:device_detail',
                        kwargs={'pk':self.pk})
