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
    cane = 'cane'
    quad_cane = 'quad cane'
    ez_crutch = 'EZ_crutch'
    adult_crutch='adult crutch'
    adult_forearm_crutch='adult forearm crutch'
    pediatric_crutch = 'pediatric crutch'
    pediatric_forearm_crutch='pediatric forearm crutch'

    nonwheeled_walker='nonwheeled walker'
    two_wheeled_walker = 'two wheeled walker'
    three_wheeled_walker = 'three wheeled walker'
    four_wheeled_walker = 'four wheeled walker'
    knee_injury_scooter = 'knee injury scooter'

    standard_wheelchair='standard wheelchair'
    active_manual_wheelchair = 'active manual wheelchair'
    pediatric_wheelchair = 'pediatric wheelchair'

    adult_medical_boot='adult medical boot'
    pediatric_medical_boot = 'pediatric medical boot'

    orthotic_brace = 'orthotic brace'
    orthotic_shoe='orthotic shoe'
    compression_brace='compression brace'

    showerchair = 'showerchair'
    btshowerchair = 'btshowerchair'
    commode = 'commode'
    sling='sling'
    glasses='glasses'
    splint='splint'
    wrist_splint='splint'
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
        (quad_cane,'quad cane'),
        (adult_crutch,'adult crutch'),
        (adult_forearm_crutch,'adult forearm crutch'),
        (pediatric_crutch,'pediatric crutch'),
        (pediatric_forearm_crutch,'pediatric forarm crutch'),
        (ez_crutch,'EZ-crutch'),
        (nonwheeled_walker,'nonwheeled walker'),
        (two_wheeled_walker,'two wheeled walker'),
        (three_wheeled_walker,'three wheeled walker'),
        (four_wheeled_walker,'four wheeled walker'),
        (knee_injury_scooter,'knee injury scooter'),
        (standard_wheelchair,'standard wheelchair'),
        (active_manual_wheelchair,'active manual wheelchair'),
        (pediatric_wheelchair,'pediatric wheelchair'),
        (adult_medical_boot,'adult medical boot'),
        (pediatric_medical_boot,'pediatric medical boot'),
        (orthotic_brace,'orthotic brace'),
        (orthotic_shoe,'orthotic shoe'),
        (compression_brace,'compression brace'),
        (sling,'sling'),
        (showerchair,'shower chair'),
        (btshowerchair,'tub attachable shower chair'),
        (commode,'commode'),
        (glasses,'glasses'),
        (splint,'splint'),
        (wrist_splint,'wrist splint'),
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
    processed=models.BooleanField(default=False)
    storage_unit = models.IntegerField(blank=False,validators=[
                            MaxValueValidator(9999),
                            MinValueValidator(1)])
    storage_unit_quadrant=models.CharField(max_length=6,blank=False)
    unique_information=models.TextField(default='None')
    date_donated_to_project_embrace=models.DateField(("Date"), default=datetime.date.today)
    date_donated_to_recipient=models.DateField(("Date Donated to Recipient (YYYY-MM-DD)"),
                                                blank=True,
                                                null=True)


    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('device_app:device_detail',
                        kwargs={'pk':self.pk})
class EquipmentValue(models.Model):
    cane = 'cane'
    quad_cane = 'quad cane'
    ez_crutch = 'EZ_crutch'
    adult_crutch='adult crutch'
    adult_forearm_crutch='adult forearm crutch'
    pediatric_crutch = 'pediatric crutch'
    pediatric_forearm_crutch='pediatric forearm crutch'

    nonwheeled_walker='nonwheeled walker'
    two_wheeled_walker = 'two wheeled walker'
    three_wheeled_walker = 'three wheeled walker'
    four_wheeled_walker = 'four wheeled walker'
    knee_injury_scooter = 'knee injury scooter'

    standard_wheelchair='standard wheelchair'
    active_manual_wheelchair = 'active manual wheelchair'
    pediatric_wheelchair = 'pediatric wheelchair'

    adult_medical_boot='adult medical boot'
    pediatric_medical_boot = 'pediatric medical boot'

    orthotic_brace = 'orthotic brace'
    orthotic_shoe='orthotic shoe'
    compression_brace='compression brace'

    showerchair = 'showerchair'
    btshowerchair = 'btshowerchair'
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
        (quad_cane,'quad cane'),
        (adult_crutch,'adult crutch'),
        (adult_forearm_crutch,'adult forearm crutch'),
        (pediatric_crutch,'pediatric crutch'),
        (pediatric_forearm_crutch,'pediatric forarm crutch'),
        (ez_crutch,'EZ-crutch'),
        (nonwheeled_walker,'nonwheeled walker'),
        (two_wheeled_walker,'two wheeled walker'),
        (three_wheeled_walker,'three wheeled walker'),
        (four_wheeled_walker,'four wheeled walker'),
        (knee_injury_scooter,'knee injury scooter'),
        (standard_wheelchair,'standard wheelchair'),
        (active_manual_wheelchair,'active manual wheelchair'),
        (pediatric_wheelchair,'pediatric wheelchair'),
        (adult_medical_boot,'adult medical boot'),
        (pediatric_medical_boot,'pediatric medical boot'),
        (orthotic_brace,'orthotic brace'),
        (orthotic_shoe,'orthotic shoe'),
        (compression_brace,'compression brace'),
        (sling,'sling'),
        (showerchair,'shower chair'),
        (btshowerchair,'tub attachable shower chair'),
        (commode,'commode'),
        (glasses,'glasses'),
        (splint,'splint'),
        (wrist_splint,'wrist splint'),
        (wrap,'wrap'),
        (bed,'bed'),
        (miscellaneous,'miscellaneous'),
        )
    source=models.URLField(max_length=300,blank=False)
    device_type=models.CharField(max_length=25,
                                 choices=DEVICE_OPTIONS,
                                 blank=False)
    source_value=models.CharField(max_length=5,blank=False)


# class Contact(models.Model):
#
#     campaign_partnership ='campaign partnership'
#     equipment_donation = 'equipment donation'
#     community_partnership='community partnership'
#
#     CONTACT_REASONS=(
#     (campaign_partnership,'campaign partnership'),
#     (equipment_donation,'equipment donation'),
#     (community_partnership,'community partnership'),
#     )
#
#     first_name = models.CharField(max_length=265,blank=False)
#     last_name = models.CharField(max_length=265,blank=False)
#     email=models.EmailField(max_length=265,blank=False)
#     phone=models.CharField(max_length=265,blank=False)
#     state_province=models.CharField(max_length=265,blank=False)
#     country=models.CharField(max_length=265,blank=False)
#     reason_for_contact=models.CharField(max_length=265,
#                                         choices=CONTACT_REASONS,
#                                         blank=False)
#     organization=models.CharField(max_length=265,blank=False)
#     position=models.CharField(max_length=265,blank=True)
#
#     def __str__(self):
#         return self.type
#
#     # def get_absolute_url(self):
#     #     return reverse('device_app:device_detail',
#     #                     kwargs={'pk':self.pk})
#
# class ProjectEmbraceEmployee(models.Model):
#     first_name = models.CharField(max_length=265,blank=False)
#     last_name = models.CharField(max_length=265,blank=False)
#     position=models.CharField(max_length=265,blank=True)
#
#     def __str__(self):
#         return self.type
#
# class Engagement(models.Model):
#     import datetime
#     introductory = 'introductory'
#
#     finance='finance'
#     community_organization='community organization'
#     operations='operations'
#     marketing='marketing'
#     campaign_outreach='campaign outreach'
#
#     ENGAGEMENT_TYPES=(
#     (finance,'finance'),
#     (community_organization,'community organization'),
#     (operations,'operations'),
#     (marketing,'marketing'),
#     (campaign_outreach,'campaign outreach'),
#     )
#
#     STATUS_TYPES=(
#     (introductory,'introductory'),
#     )
#
#     date_of_first_contact=models.DateField(("Date"), default=datetime.date.today)
#     date_of_recent_contact=models.DateField(("Date of Recent Communication (YYYY-MM-DD)"),
#                                             blank=True,
#                                             null=True)
#     engagement_type=models.CharField(max_length=265,
#                                      choices=ENGAGEMENT_TYPES,
#                                      blank=False)
#     status=models.CharField(max_length=265,
#                             choices=STATUS_TYPES,
#                             blank=False)
#     contact=models.ForeignKey(Contact,
#                             related_name='contact',
#                             on_delete=models.CASCADE)
#     project_embrace_employee=models.ForeignKey(ProjectEmbraceEmployee,
#                                     related_name='project_embrace_employee',
#                                     on_delete=models.CASCADE)
#     def __str__(self):
#         return self.type
#
# class NeedsAssessment(models.Model):
#     # Need quantity groupings
#     zero_ten = '0 - 10'
#     eleven_twenty = '11 - 20'
#     twenty1_thirty = '21 - 30'
#     thirty1_fourty = '31 - 40'
#     greater_than_fifty = 'Greater than 50'
#
#     DEVICE_QUANTITIES=(
#     (zero_ten,'0 - 10'),
#     (eleven_twenty,'11 - 20'),
#     (twenty1_thirty,'21 - 30'),
#     (thirty1_fourty,'31 - 40'),
#     (greater_than_fifty,'Greater than 50')
#     )
#
#     patients_served_weekly=models.CharField(max_length=265,blank=False)
#     need_for_crutches=models.CharField(max_length=265,
#                                        choices=DEVICE_QUANTITIES,
#                                        blank=False)
#     need_for_wheelchairs=models.CharField(max_length=265,
#                                        choices=DEVICE_QUANTITIES,
#                                        blank=False)
#     need_for_walkers=models.CharField(max_length=265,
#                                        choices=DEVICE_QUANTITIES,
#                                        blank=False)
#     need_for_kneebraces=models.CharField(max_length=265,
#                                        choices=DEVICE_QUANTITIES,
#                                        blank=False)
#     items_notes=models.TextField(default='None')
#     engagement=models.ForeignKey(Engagement,
#                             related_name='engagement',
#                             on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.type
#
# class EngagementNotes(models.Model):
#     engagement=models.ForeignKey(Engagement,
#                             related_name='engagement_notes',
#                             on_delete=models.CASCADE)
#     project_embrace_employee=models.ForeignKey(ProjectEmbraceEmployee,
#                                     related_name='project_embrace_employee_notes',
#                                     on_delete=models.CASCADE)
#     notes=models.TextField(default='None')
#
#     def __str__(self):
#         return self.type
