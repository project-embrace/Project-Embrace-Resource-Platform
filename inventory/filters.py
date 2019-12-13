from django_filters import FilterSet,NumberFilter,DateRangeFilter,DateFilter

from .models import Device,Donor,Campaign,StorageArea,DonationHouse,EquipmentValue


class DeviceFilter(FilterSet):
    device_date__gt = DateFilter(field_name='date_donated_to_project_embrace', lookup_expr='gt')
    device_date__lt = DateFilter(field_name='date_donated_to_project_embrace', lookup_expr='lt')
    class Meta:
        model = Device
        fields = {"type": ["exact"],
                  "condition": ["exact"],
                  "id": ["contains"],
                  'campaign':['exact'],
                  'processed':['exact'],
                  'device_date__gt':['contains'],
                  'device_date__lt':['contains']}


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
