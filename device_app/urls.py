from django.contrib import admin
from django.urls import path,include
from device_app import views
app_name = 'device_app'

urlpatterns = [
    path('user_login/',views.user_login,name='user_login'),
    path('operations/',views.operations_index,name='operations_index'),
    path('finance/',views.finance_index,name='finance_index'),
    path('relationship_mgmt/',views.relationship_index,name='relationship_index'),
    path('marketing/',views.marketing_index,name='marketing_index'),
    path('knowledge_base/',views.knowledge_index,name='knowledge_index'),

    path('donor_list/',views.DonorList.as_view(),name='donor_list'),
    path('donor_list/<int:pk>/',views.DonorDetail.as_view(),name='donor_detail'),
    path('donor_create/',views.DonorCreateView.as_view(),name='donor_create'),
    path('donor_update/<int:pk>/',views.DonorUpdateView.as_view(),name='donor_update'),
    path('donor_delete/<int:pk>/',views.DonorDeleteView.as_view(),name='donor_delete'),

    path('device_list/',views.DeviceList.as_view(),name='device_list'),
    path('device_list/<int:pk>/',views.DeviceDetail.as_view(),name='device_detail'),
    path('device_create/',views.DeviceCreateView.as_view(),name='device_create'),
    path('device_update/<int:pk>/',views.DeviceUpdateView.as_view(),name='device_update'),
    path('device_delete/<int:pk>/',views.DeviceDeleteView.as_view(),name='device_delete'),

    path('donation_house_list/',views.DonationHouseList.as_view(),name='donation_house_list'),
    path('donation_house_list/<int:pk>/',views.DonationHouseDetail.as_view(),name='donation_house_detail'),

    path('campaign_list/',views.CampaignList.as_view(),name='campaign_list'),
    path('campaign_list/<int:pk>/',views.CampaignDetail.as_view(),name='campaign_detail'),

    path('storage_list/',views.StorageList.as_view(),name='storage_list'),
    path('storage_list/<int:pk>/',views.StorageDetail.as_view(),name='storage_detail'),

]
