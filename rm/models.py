from django.db import models

# Create your models here.
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
