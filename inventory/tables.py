from django_tables2.utils import A
import django_tables2 as tables
from django.core.paginator import Paginator
import pandas as pd
from django_pandas.io import read_frame

from .models import Device,Donor,Campaign,StorageArea,DonationHouse,EquipmentValue
# def group_by_campgain_heading():
#     qs = Campaign.objects.all()
#     donors = read_frame(qs)
#     campaign_list = Campaign.id.unique().tolist()
#     class_names = campaign_list
#     previous = None
#
#     def inner(record):
#         # in first row and after every change, remove the first element
#         # and use it as the current class name.
#         if previous is None or record.header_2 != previous.header_2:
#             class_name = class_names.pop(0)
#
#         previous = record
#         return class_name
#     return inner

class DeviceTable(tables.Table):
    id = tables.Column(linkify=True)
    donor = tables.Column(linkify=True)
    campaign = tables.Column(linkify=True)
    condition = tables.Column(visible=False)
    class Meta:
        model = Device
        template_name = "inventory/table.html"
        fields = ('id','type','condition','processed','donated_to_recipient','campaign')
        linkify = ('id','donor','campaign')


class CampaignTable(tables.Table):
    title = tables.Column(linkify=True)
    class Meta:
        model = Campaign
        template_name = "inventory/table.html"
        fields = ('title','start_date','end_date')
        linkify = ('title',)

class DonorTable(tables.Table):
    id = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    donation_house = tables.Column(linkify=True)
    class Meta:
        model = Donor
        template_name = "inventory/table.html"
        exclude = ('id',)
        fields = ('name','email','donation_date','sent_a_receipt','donation_house')
        linkify = ('name','donation_house')

class DonoHouseTable(tables.Table):
    title = tables.Column(linkify=True)
    class Meta:
        model = DonationHouse
        template_name = "inventory/table.html"
        fields = ('title',)
        linkify = ('title',)

class StorageTable(tables.Table):
    title = tables.Column(linkify=True)
    class Meta:
        model = StorageArea
        template_name = "inventory/table.html"
        fields = ('title',)
        linkify = ('title',)

class EquipmentValueTable(tables.Table):
    id = tables.Column(linkify=True)
    # average_value = tables.Column(accessor=A('average_value'))

    class Meta:
        model = EquipmentValue
        template_name = "inventory/table.html"
        fields = ('id','source','device_type','source_value')
        # sequence = ('id','source','device_type','source_value','average_value')
        linkify = ('id',)
