from django_filters import FilterSet

from .models import Device,Donor,Campaign,StorageArea,DonationHouse,EquipmentValue


class DeviceFilter(FilterSet):
    class Meta:
        model = Device
        fields = {"type": ["exact"], "condition": ["exact"], "id": ["contains"],'campaign':['exact'],'processed':['exact'],'date_donated_to_project_embrace':['exact']}


class DonorFilter(FilterSet):
    class Meta:
        model = Donor
        fields = {"name": ["contains"],"donation_date": ["contains"],"sent_a_receipt": ["exact"]}

class CampaignFilter(FilterSet):
    class Meta:
        model = Campaign
        fields = {"title": ["contains"]}

class DonationHouseFilter(FilterSet):
    class Meta:
        model = DonationHouse
        fields = {"title": ["contains"]}

class StorageAreaFilter(FilterSet):
    class Meta:
        model = StorageArea
        fields = {"title": ["contains"]}

class EquipmentValueFilter(FilterSet):
    class Meta:
        model = EquipmentValue
        fields = {"device_type": ["exact"]}
