from django.shortcuts import render
from device_app.forms import UserForm
from django.utils.decorators import method_decorator
from django.db.models import Q
from device_app.models import Donor,Device,DonationHouse,Campaign,StorageArea
from django.urls import reverse_lazy
from django.views.generic import (View,
                                  TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from .charts import (ReadyToDonatePieChart,
                     DonatedPieChart,
                     InputFrequency,
                     OutputFrequency,
                     DirtyInventory)
from . import models
import pygal
from pygal.style import Style

# Create your views heree
def operations_index(request):
    return render(request,'device_app/operations_index.html')

def landing_index(request):
    return render(request,'device_app/landing_index.html')

def finance_index(request):
    return render(request,'device_app/finance_index.html')

def marketing_index(request):
    return render(request,'device_app/marketing_index.html')

def relationship_index(request):
    return render(request,'device_app/relationship_index.html')

def knowledge_index(request):
    return render(request,'device_app/knowledge_index.html')

def tutorial(request):
    return render(request,'device_app/tutorial.html')

def public_dash(request):
    return render(request,'device_app/public_dash_index.html')

# User authentication
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing_index'))


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('landing_index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed')
            print("username: {} password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,"device_app/login.html")

# CRUD items
# Donor Section
# gathers total row count if needed
# def get_context_data(self,**kwargs):
#     context = super().get_context_data(**kwargs)
#     donor_count = Donor.objects.all().count()
#     context = {'donor_count':donor_count}
#     return context

class DonorList(ListView):
    context_object_name = 'donors'
    model=models.Donor

    # Search Code
    def post(self, request):
            keywords=''

            if request.method=='POST': # form was submitted

                keywords = request.POST.get("ds", "") # <input type="text" name="keywords">
                all_queries = None
                search_fields = ('donation_house__title','name','donation_date') # change accordingly
                for keyword in keywords.split(' '): # keywords are splitted into words (eg: john science library)
                    keyword_query = None
                    for field in search_fields:
                        each_query = Q(**{field + '__icontains': keyword})
                        if not keyword_query:
                            keyword_query = each_query
                        else:
                            keyword_query = keyword_query | each_query
                            if not all_queries:
                                all_queries = keyword_query
                            else:
                                all_queries = all_queries & keyword_query

                searchD= Donor.objects.filter(all_queries).distinct()
                context = {'searchD':searchD}
                return render(request, 'device_app/donor_list.html', context)

            else: # no data submitted

                context = {}
                return render(request, 'device_app/ops_index.html', context)

class DonorDetail(DetailView):
   context_object_name = 'donor_detail'
   model=models.Donor
   template_name='device_app/donor_details.html'

class DonorCreateView(CreateView):
    fields = ('name','email','donation_date','donation_house')
    # fields are used to determine what you can alter in the model
    model=models.Donor

class DonorUpdateView(UpdateView):
    fields = ('name','email')
    model = models.Donor

class DonorDeleteView(DeleteView):
    model = models.Donor
    success_url = reverse_lazy("device_app:donor_list")

# Device Section
class DeviceList(ListView):
    context_object_name = 'devices'
    model=models.Device

    def post(self, request):
            keywords=''

            if request.method=='POST': # form was submitted

                keywords = request.POST.get("device_search", "") # <input type="text" name="keywords">
                all_queries = None
                search_fields = ("id","type","campaign__title") # change accordingly
                for keyword in keywords.split(' '): # keywords are splitted into words (eg: john science library)
                    keyword_query = None
                    for field in search_fields:
                        each_query = Q(**{field + '__icontains': keyword})
                        if not keyword_query:
                            keyword_query = each_query
                        else:
                            keyword_query = keyword_query | each_query
                            if not all_queries:
                                all_queries = keyword_query
                            else:
                                all_queries = all_queries & keyword_query

                searchDevices= Device.objects.filter(all_queries).distinct()
                context = {'searchDevices':searchDevices}
                return render(request, 'device_app/device_list.html', context)

            else: # no data submitted

                context = {}
                return render(request, 'device_app/device_list.html', context)

class DeviceDetail(DetailView):
   context_object_name = 'device_detail'
   model=models.Device
   template_name='device_app/device_details.html'

class DeviceCreateView(CreateView):
    fields = ('date_donated_to_project_embrace','type',
              'condition','donor','campaign','storage_area',
              'storage_unit','storage_unit_quadrant',
              'processed','unique_information')
    # fields are used to determine what you can alter in the model
    model=models.Device

class DeviceUpdateView(UpdateView):
    fields = ('type','condition','donor',
              'campaign','storage_area','processed',
              'storage_unit','storage_unit_quadrant',
              'donated_to_recipient','unique_information',
              'date_donated_to_recipient')
    model = models.Device

class DeviceDeleteView(DeleteView):
    model = models.Device
    success_url = reverse_lazy("device_app:device_list")

class DeviceVisualsView(TemplateView):
    template_name = 'device_app/device_dash.html'
    model = models.Device
    def get_context_data(self, **kwargs):
        context = super(DeviceVisualsView, self).get_context_data(**kwargs)
        custom_style = Style(colors=('#BE1E2D',))
        cht_readytodonate = ReadyToDonatePieChart(
                            height=300,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            legend_at_bottom = True,
                            title='Processed Inventory'
                            )
        context['PI'] = cht_readytodonate.generate()

        cht_donated = DonatedPieChart(
                            height=300,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            legend_at_bottom = True,
                            title = 'Campaign Inventory Donated',
                            )
        context['CID'] = cht_donated.generate()

        cht_input_dist = DirtyInventory(
                            height=300,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            legend_at_bottom = True,
                            title = 'Non-Processed Inventory',
                            )
        context['NPI'] = cht_input_dist.generate()

        cht_input_dist = InputFrequency(
                            height=250,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Inventory Input Frequency',
                            )
        context['IIF'] = cht_input_dist.generate()

        cht_input_dist = OutputFrequency(
                            height=250,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Inventory Output Frequency',
                            )
        context['IOF'] = cht_input_dist.generate()

        return context

# Donation House Section
class DonationHouseList(ListView):
    context_object_name = 'donationhouses'
    model=models.DonationHouse

class DonationHouseDetail(DetailView):
   context_object_name = 'donationhouse_detail'
   model=models.DonationHouse
   template_name='device_app/donationhouse_details.html'

# Campaign Section
class CampaignList(ListView):
    context_object_name = 'campaigns'
    model=models.Campaign

class CampaignDetail(DetailView):
   context_object_name = 'campaign_details'
   model=models.Campaign
   template_name='device_app/campaign_details.html'

# Storage Area Section
class StorageList(ListView):
    context_object_name = 'storages'
    model=models.StorageArea

class StorageDetail(DetailView):
    context_object_name = 'storage_detail'
    model=models.StorageArea
    template_name='device_app/storage_detail.html'

    # Search Code
    def post(self,request):
            keywords=''

            if request.method=='POST': # form was submitted

                keywords = request.POST.get("ss", "") # <input type="text" name="keywords">
                all_queries = None
                search_fields = ("id","campaign__title","type",'campaign__title') # change accordingly
                for keyword in keywords.split(' '): # keywords are splitted into words (eg: john science library)
                    keyword_query = None
                    for field in search_fields:
                        each_query = Q(**{field + '__icontains': keyword})
                        if not keyword_query:
                            keyword_query = each_query
                        else:
                            keyword_query = keyword_query | each_query
                            if not all_queries:
                                all_queries = keyword_query
                            else:
                                all_queries = all_queries & keyword_query

                searchDevices= Device.objects.filter(all_queries).distinct()
                context = {'searchDevices':searchDevices}
                return render(request, 'device_app/storage_detail.html', context)

            else: # no data submitted

                context = {}
                return render(request, 'device_app/storage_details.html', context)

class PublicDashView(TemplateView):
    template_name = 'device_app/public_dash_inventory.html'
    def get_context_data(self, **kwargs):
        context = super(PublicDashView, self).get_context_data(**kwargs)
        custom_style = Style(colors=('#BE1E2D',))
        cht_readytodonate = ReadyToDonatePieChart(
                            height=300,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            legend_at_bottom = True,
                            title='Inventory Ready for Donation'
                            )
        context['CI2'] = cht_readytodonate.generate()

        cht_donated = DonatedPieChart(
                            height=300,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            legend_at_bottom = True,
                            title = 'Campaign Inventory Donated',
                            )
        context['CDI2'] = cht_donated.generate()

        return context

# class EquipmentValue(CreateView):
#     model = models.EquipmentValue
#     fields = ('source','device_type','value')
