from django.contrib import admin
from django.urls import path,include
from inventory import views

app_name = 'inventory'

urlpatterns = [
    path('landing/',views.landing_index,name='landing_index'),
    path('operations/',views.operations_index,name='operations_index'),
    path('finance/',views.finance_index,name='finance_index'),
    path('marketing/',views.marketing_index,name='marketing_index'),
    path('knowledge_base/',views.knowledge_index,name='knowledge_index'),

    path('receipts/',views.ReceiptView.as_view(),name='receipts'),
    path('receipts/<int:pk>/',views.DonorDetail.as_view(),name='donor_detail'),

    path('public_dash/',views.public_dash,name='public_dash'),
    path('public_outreach_request/',views.Outreach.as_view(),name='public_outreach_request'),
    path('public_input_request/',views.Input.as_view(),name='public_input_request'),
    path('public_thanks/',views.ThanksPublic,name='public_thanks'),
    path('public_dash_inventory/',views.PublicDashView.as_view(),name='public_dash_inventory'),

    path('donor_list/',views.FilteredDonorList.as_view(),name='donor_list'),
    path('donor_list/<int:pk>/',views.DonorDetail.as_view(),name='donor_detail'),
    path('donor_create/',views.DonorCreateView.as_view(),name='donor_create'),
    path('donor_update/<int:pk>/',views.DonorUpdateView.as_view(),name='donor_update'),
    path('donor_delete/<int:pk>/',views.DonorDeleteView.as_view(),name='donor_delete'),

    path('device_list/',views.FilteredDeviceList.as_view(),name='device_list'),
    path('device_dash/',views.DeviceVisualsView.as_view(),name='device_dash'),
    path('device_list/<int:pk>/',views.DeviceDetail.as_view(),name='device_detail'),
    path('device_create/',views.DeviceCreateView.as_view(),name='device_create'),
    path('device_update/<int:pk>/',views.DeviceUpdateView.as_view(),name='device_update'),

    path('donation_house_list/',views.FilteredDonationHouseList.as_view(),name='donation_house_list'),
    path('donation_house_list/<int:pk>/',views.DonationHouseDetail.as_view(),name='donation_house_detail'),
    path('donation_house_create/',views.DonationHouseCreateView.as_view(),name='donation_house_create'),
    path('donation_house_update/<int:pk>/',views.DonationHouseUpdateView.as_view(),name='donation_house_update'),

    path('campaign_list/',views.FilteredCampaignList.as_view(),name='campaign_list'),
    path('campaign_list/<int:pk>/',views.CampaignDetail.as_view(),name='campaign_detail'),
    path('campaign_create/',views.CampaignCreateView.as_view(),name='campaign_create'),
    path('campaign_update/<int:pk>/',views.CampaignUpdateView.as_view(),name='campaign_update'),

    path('storage_list/',views.FilteredStorageList.as_view(),name='storage_list'),
    path('storage_list/<int:pk>/',views.StorageDetail.as_view(),name='storage_detail'),
    path('storage_create/',views.StorageCreateView.as_view(),name='storage_create'),
    path('storage_update/<int:pk>/',views.StorageUpdateView.as_view(),name='storage_update'),

    # Equipment Value
    path('equipment_value/',views.FilteredEquipmentList.as_view(),name='equipment_list'),
    path('equipment_value/<int:pk>/',views.EquipmentValueDetail.as_view(),name='equipment_detail'),
    path('equipment_value_create/',views.EquipmentValueCreate.as_view(),name='equipment_create'),
    path('equipment_value_update/<int:pk>/',views.EquipmentValueUpdate.as_view(),name='equipment_update'),
    path('equipment_delete/<int:pk>/',views.EquipmentValueDeleteView.as_view(),name='equipment_delete'),


    # Knowledge Base
    path('documents/', views.DocumentListView.as_view(), name='knowledge_index'),
    path('documents/create/', views.document_create, name='create_doc'),
    path('documents/<int:pk>/edit/', views.document_update, name="edit_doc"),
    path('documents/<int:pk>/view/',
         views.DocumentDetailView.as_view(), name='view_doc'),
    path('documents/<int:pk>/delete/',
         views.DocumentDeleteView.as_view(), name='remove_doc'),

    # download
    path('documents/<int:pk>/download/',
         views.download_document, name='download_document'),

    # Finance Knowledge Base
    path('finance_documents/', views.FinDocumentListView.as_view(), name='finance_kb'),
    path('finance_documents/create/', views.FinDocumentCreate, name='fin_create_doc'),
    path('finance_documents/<int:pk>/edit/', views.FinDocumentUpdate, name="fin_edit_doc"),
    path('finance_documents/<int:pk>/view/',
         views.FinDocumentDetailView.as_view(), name='fin_view_doc'),
    path('finance_documents/<int:pk>/delete/',
         views.FinDocumentDeleteView.as_view(), name='fin_remove_doc'),

    # download
    path('fin_documents/<int:pk>/download/',
         views.FinDownloadDocument, name='fin_download_document'),
]
