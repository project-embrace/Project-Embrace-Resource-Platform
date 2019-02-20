from django.contrib import admin
from device_app.models import (Donor,DonationHouse,
                              StorageArea,Campaign,
                              Recipient,Device)
# Register your models here.
admin.site.register(Donor)
admin.site.register(DonationHouse)
admin.site.register(StorageArea)
admin.site.register(Campaign)
admin.site.register(Recipient)
admin.site.register(Device)
