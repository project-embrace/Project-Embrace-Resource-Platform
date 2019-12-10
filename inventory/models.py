from django.db import models
from django.urls import reverse
from django.db.models import Avg
from django.forms.fields import DateField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import time
import arrow

from common.templatetags.common_tags import (
    is_document_file_image, is_document_file_audio,
    is_document_file_video, is_document_file_pdf,
    is_document_file_code, is_document_file_text,
    is_document_file_sheet, is_document_file_zip
)

from common.models import User


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

    def get_absolute_url(self):
        return reverse('inventory:donation_house_detail',
                        kwargs={'pk':self.pk})

class Donor(models.Model):
    import datetime
    name=models.CharField(max_length=265,blank=False)
    email=models.EmailField(max_length=265,blank=False)
    region=models.CharField(max_length=265,blank=False)
    country=models.CharField(max_length=265,blank=False)
    donation_date=models.DateField(("Date"), default=datetime.date.today)
    donation_house=models.ForeignKey(DonationHouse,
                                     default='1',
                                     related_name='dono_house',
                                     on_delete=models.CASCADE)
    sent_a_receipt=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inventory:donor_detail',
                        kwargs={'pk':self.pk})
    class Meta:
       ordering = ('donation_date',)

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
        return reverse('inventory:storage_detail',
                        kwargs={'pk':self.pk})

class Campaign(models.Model):
    title=models.CharField(max_length=265,default='No Campaign',blank=False)
    partnership=models.CharField(max_length=265,null=True,blank=True)
    organization_recipient=models.CharField(max_length=265,null=True,blank=True)
    region=models.CharField(max_length=265,blank=False)
    country=models.CharField(max_length=265,blank=False)
    start_date=models.DateField(blank=False)
    end_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('inventory:campaign_detail',
                        kwargs={'pk':self.pk})

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
    # Device Values
    cane = 'cane'
    quad_cane = 'cane, quad'
    crutch_adult = 'crutch, adult'
    forearm_crutch_adult = 'forearm crutch, adult'
    crutch_pediatric = 'crutch, pediatric'
    forearm_crutch_pediatric = 'forearm crutch, pediatric'

    walker_nonwheeled = 'walker, non-wheeled'
    walker_two_wheeled = 'walker, two-wheeled'
    walker_three_wheeled = 'walker, three-wheeled'
    walker_four_wheeled = 'walker, four-wheeled'

    knee_injury_scooter = 'knee injury scooter'
    wheelchair_standard = 'wheelchair, standard'
    wheelchair_active_manual ='wheelchair, active-manual'
    wheelchair_pediatric = 'wheelchair, pediatric'
    wheelchair_seat = 'wheelchair, seat cushion'

    medical_boot_adult = 'medical boot, adult'
    medical_boot_pediatric = 'medical boot, pediatric'

    orthotic_brace_adult = 'orthotic brace, adult'
    orthotic_brace_pediatric = 'orthotic brace, pediatric'
    orthotic_shoe_adult = 'orthotic shoe, adult'
    orthotic_shoe_pediatric = 'orthotic shoe, pediatric'
    compression_brace='compression brace'

    showerchair = 'showerchair'
    showerchair_ta = 'shower chair, tub-attachable'
    commode = 'commode'
    sling='sling'
    glasses='glasses'
    splint='splint'
    wrist_splint='splint, wrist'
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
        (cane,'cane'),
        (quad_cane,'cane, quad'),
        (crutch_adult,'crutch, adult'),
        (crutch_pediatric,'crutch, pediatric'),
        (forearm_crutch_adult,'forearm crutch, adult'),
        (forearm_crutch_pediatric,'forearm crutch, pediatric'),
        (walker_nonwheeled,'walker, non-wheeled'),
        (walker_two_wheeled,'walker, two-wheeled'),
        (walker_three_wheeled,'walker, three-wheeled'),
        (walker_four_wheeled,'walker, four-wheeled'),
        (knee_injury_scooter,'knee injury scooter'),
        (wheelchair_standard,'wheelchair, standard'),
        (wheelchair_active_manual,'wheelchair, active-manual'),
        (wheelchair_pediatric,'wheelchair, pediatric'),
        (medical_boot_adult,'medical boot adult'),
        (medical_boot_pediatric,'medical boot, pediatric'),
        (wheelchair_seat, 'wheelchair, seat cushion'),
        (orthotic_brace_adult,'orthotic brace adult'),
        (orthotic_brace_pediatric,'orthotic brace, pediatric'),
        (orthotic_shoe_adult,'orthotic shoe, adult'),
        (orthotic_shoe_pediatric,'orthotic shoe, pediatric'),
        (compression_brace,'compression brace'),
        (sling,'sling'),
        (showerchair,'shower chair'),
        (showerchair_ta,'shower chair, tub-attachable'),
        (commode,'commode'),
        (splint,'splint'),
        (wrist_splint,'wrist, splint'),
        (miscellaneous,'miscellaneous'),
        )

    # Storage Unit Values

    storg_1='109'
    storg_2='115'
    storg_dono = 'Donated Item'

    storg_quad_1 = 'Q1'
    storg_quad_2 = 'Q2'
    storg_quad_3 = 'Q3'
    storg_quad_4 = 'Q4'
    storg_quad_dono = 'Donated Item'

    STORAGE_UNIT_OPTIONS =(
    (storg_1,'109'),
    (storg_2,'115'),
    (storg_dono,'Donated Item')
    )

    STORAGE_UNIT_QUADRANT_OPTIONS =(
    (storg_quad_1,'Q1'),
    (storg_quad_2,'Q2'),
    (storg_quad_3,'Q3'),
    (storg_quad_4,'Q4'),
    (storg_quad_dono,'Donated Item')
    )
    type=models.CharField(max_length=47,choices=sorted(DEVICE_OPTIONS),blank=False)
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
    processed=models.BooleanField(default=False)
    storage_unit = models.CharField(blank=False,choices=sorted(STORAGE_UNIT_OPTIONS),max_length=3)
    storage_unit_quadrant=models.CharField(max_length=13,choices=sorted(STORAGE_UNIT_QUADRANT_OPTIONS),blank=False)
    unique_information=models.TextField(default='None')
    date_donated_to_project_embrace=models.DateField(("Date"), default=datetime.date.today)
    date_donated_to_recipient=models.DateField(("Date Donated to Recipient (YYYY-MM-DD)"),
                                                blank=True,
                                                null=True)


    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('inventory:device_detail',
                        kwargs={'pk':self.pk})
    class Meta:
       ordering = ('id',)

class EquipmentValue(models.Model):
    cane = 'cane'
    quad_cane = 'cane, quad'
    crutch_adult = 'crutch, adult'
    forearm_crutch_adult = 'forearm crutch, adult'
    crutch_pediatric = 'crutch, pediatric'
    forearm_crutch_pediatric = 'forearm crutch, pediatric'

    walker_nonwheeled = 'walker, non-wheeled'
    walker_two_wheeled = 'walker, two-wheeled'
    walker_three_wheeled = 'walker, three-wheeled'
    walker_four_wheeled = 'walker, four-wheeled'

    knee_injury_scooter = 'knee injury scooter'
    wheelchair_standard = 'wheelchair, standard'
    wheelchair_active_manual ='wheelchair, active-manual'
    wheelchair_pediatric = 'wheelchair, pediatric'
    wheelchair_seat = 'wheelchair, seat cushion'

    medical_boot_adult = 'medical boot, adult'
    medical_boot_pediatric = 'medical boot, pediatric'

    orthotic_brace_adult = 'orthotic brace, adult'
    orthotic_brace_pediatric = 'orthotic brace, pediatric'
    orthotic_shoe_adult = 'orthotic shoe, adult'
    orthotic_shoe_pediatric = 'orthotic shoe, pediatric'
    compression_brace='compression brace'

    showerchair = 'showerchair'
    showerchair_ta = 'shower chair, tub-attachable'
    commode = 'commode'
    sling='sling'
    glasses='glasses'
    splint='splint'
    wrist_splint='splint'
    wrap='wrap'
    bed='bed'

    miscellaneous='miscellaneous'

    DEVICE_OPTIONS = (
        (cane,'cane'),
        (quad_cane,'cane, quad'),
        (crutch_adult,'crutch, adult'),
        (crutch_pediatric,'crutch, pediatric'),
        (forearm_crutch_adult,'forearm crutch, adult'),
        (forearm_crutch_pediatric,'forearm crutch, pediatric'),
        (walker_nonwheeled,'walker, non-wheeled'),
        (walker_two_wheeled,'walker, two-wheeled'),
        (walker_three_wheeled,'walker, three-wheeled'),
        (walker_four_wheeled,'walker, four-wheeled'),
        (knee_injury_scooter,'knee injury scooter'),
        (wheelchair_standard,'wheelchair, standard'),
        (wheelchair_active_manual,'wheelchair, active-manual'),
        (wheelchair_pediatric,'wheelchair, pediatric'),
        (wheelchair_seat, 'wheelchair, seat cushion'),
        (medical_boot_adult,'medical boot adult'),
        (medical_boot_pediatric,'medical boot, pediatric'),
        (orthotic_brace_adult,'orthotic brace adult'),
        (orthotic_brace_pediatric,'orthotic brace, pediatric'),
        (orthotic_shoe_adult,'orthotic shoe, adult'),
        (orthotic_shoe_pediatric,'orthotic shoe, pediatric'),
        (compression_brace,'compression brace'),
        (sling,'sling'),
        (showerchair,'shower chair'),
        (showerchair_ta,'shower chair, tub-attachable'),
        (commode,'commode'),
        (splint,'splint'),
        (wrist_splint,'wrist splint'),
        (miscellaneous,'miscellaneous'),
        )
    source=models.URLField(max_length=300,blank=False)
    device_type=models.CharField(max_length=25,
                                 choices=sorted(DEVICE_OPTIONS),
                                 blank=False)
    source_value=models.DecimalField(blank=False, max_digits=6, decimal_places=2)

    # Nice to have but fucking annoying
    # def average_value(self):
    #     return Avg(self.source_value)

    def __str__(self):
        return self.device_type

    def get_absolute_url(self):
        return reverse('inventory:equipment_detail',
                        kwargs={'pk':self.pk})
    class Meta:
       ordering = ('id',)


# Documents

def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class KBDocument(models.Model):

    DOCUMENT_STATUS_CHOICE = (
        ("active", "active"),
        ('inactive', 'inactive')
    )

    title = models.CharField(max_length=1000, blank=True, null=True)
    document_file = models.FileField(upload_to=document_path, max_length=5000)
    created_by = models.ForeignKey(
        User, related_name='document_uploaded+',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default='active')
    shared_to = models.ManyToManyField(User, related_name='document_shared_to+')
    teams = models.ManyToManyField('teams.Teams', related_name='document_teams+')


    class Meta:
        ordering = ('-created_on',)

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if (len(name_ext_list) > 1):
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def __str__(self):
        return self.title

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.shared_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.shared_to.values_list('id', flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

class FinDocument(models.Model):

    DOCUMENT_STATUS_CHOICE = (
        ("active", "active"),
        ('inactive', 'inactive')
    )

    title = models.CharField(max_length=1000, blank=True, null=True)
    document_file = models.FileField(upload_to=document_path, max_length=5000)
    created_by = models.ForeignKey(
        User, related_name='document_uploaded++',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default='active')
    shared_to = models.ManyToManyField(User, related_name='document_shared_to++')
    teams = models.ManyToManyField('teams.Teams', related_name='document_teams++')


    class Meta:
        ordering = ('-created_on',)

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if (len(name_ext_list) > 1):
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def __str__(self):
        return self.title

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.shared_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.shared_to.values_list('id', flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()
