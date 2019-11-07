from django.shortcuts import render
from device_app.forms import UserForm,OutreachForm
from django.utils.decorators import method_decorator
from django.db.models import Q
from device_app.models import Donor,Device,DonationHouse,Campaign,StorageArea
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from .tables import (DeviceTable,DeviceListTable,
                     DonorListTable,DonorTable,
                     CampaignListTable,CampaignTable,
                     DonoHouseListTable,DonoHouseTable,
                     StorageListTable, StorageTable)
from .filters import (DeviceFilter,DonorFilter,
                      CampaignFilter,DonationHouseFilter,
                      StorageAreaFilter)
from .charts import (ReadyToDonatePieChart,
                     DonatedPieChart,
                     InputFrequency,
                     OutputFrequency,
                     DirtyInventory,
                     InventoryTable)
from . import models
import pygal
from pygal.style import Style
import pandas as pd
from django_pandas.io import read_frame
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from django_tables2.paginators import LazyPaginator


# Index Section ----------------------------------------------------------------------------------------------------------------
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

# User authentication ----------------------------------------------------------------------------------------------------------------
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

# CRUD items ----------------------------------------------------------------------------------------------------------------
# Operations Section ----------------------------------------------------------------------------------------------------------------
## Donor Section ----------------------------------------------------------------------------------------------------------------
class FilteredDonorList(SingleTableMixin, FilterView):
    model = Donor
    table_class = DonorListTable
    template_name = 'device_app/donor_list.html'
    filterset_class = DonorFilter

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
    fields = ('name','email','region','country','donation_date','donation_house')
    # fields are used to determine what you can alter in the model
    model=models.Donor

class DonorUpdateView(UpdateView):
    fields = ('name','email')
    model = models.Donor

class DonorDeleteView(DeleteView):
    model = models.Donor
    success_url = reverse_lazy("device_app:donor_list")

## Device Section ----------------------------------------------------------------------------------------------------------------
class FilteredDeviceList(ExportMixin,SingleTableMixin, FilterView,):
    model = Device
    table_class = DeviceListTable
    template_name = 'device_app/device_list.html'
    filterset_class = DeviceFilter
    export_formats = ("csv",)

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
                            legend_at_bottom_columns=3,
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
                            legend_at_bottom_columns=3,
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
                            legend_at_bottom_columns=3,
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
                            title = 'Campaign Output Frequency',
                            )
        context['IOF'] = cht_input_dist.generate()

        cht_inventory_table = InventoryTable(
                            height=300,
                            width=800,
                            explicit_size=True,
                            opacity='.6',
                            opacity_hover='.9',
                            style=custom_style,
                            legend_at_bottom = True,
                            legend_at_bottom_columns=3,
                            title='Processed Inventory'
                            )
        context['IT'] = cht_inventory_table.generate()

        return context

## Donation House Section ----------------------------------------------------------------------------------------------------------------

class FilteredDonationHouseList(SingleTableMixin, FilterView):
    model = DonationHouse
    table_class = DonoHouseListTable
    template_name = 'device_app/donationhouse_list.html'
    filterset_class = DonationHouseFilter

class DonationHouseList(ListView):
    context_object_name = 'donationhouses'
    model=models.DonationHouse

class DonationHouseCreateView(CreateView):
    fields = ('title','street','city','state','zip')
    # fields are used to determine what you can alter in the model
    model=models.DonationHouse

class DonationHouseUpdateView(UpdateView):
    fields = ('title','street','city','state','zip')
    model = models.DonationHouse

class DonationHouseDetail(DetailView):
   context_object_name = 'donationhouse_detail'
   model=models.DonationHouse
   template_name='device_app/donationhouse_details.html'

## Campaign Section ----------------------------------------------------------------------------------------------------------------
class FilteredCampaignList(SingleTableMixin, FilterView):
    model = Campaign
    table_class = CampaignListTable
    template_name = 'device_app/campaign_list.html'
    filterset_class = CampaignFilter

class CampaignList(ListView):
    context_object_name = 'campaigns'
    model=models.Campaign

class CampaignDetail(DetailView):
   context_object_name = 'campaign_detail'
   model=models.Campaign
   template_name='device_app/campaign_details.html'

class CampaignCreateView(CreateView):
     fields = ('title','region','country','start_date','end_date')
     # fields are used to determine what you can alter in the model
     model=models.Campaign

class CampaignUpdateView(UpdateView):
     fields = ('title','region','country','end_date')
     model = models.Campaign

# class FilteredDeviceList(ExportMixin,SingleTableMixin, FilterView,):
#     model = Device
#     table_class = DeviceListTable
#     template_name = 'device_app/device_list.html'
#     filterset_class = DeviceFilter
#     export_formats = ("csv",)

## Storage Area Section ----------------------------------------------------------------------------------------------------------------

class FilteredStorageList(SingleTableMixin, FilterView):
    model = StorageArea
    table_class = StorageListTable
    template_name = 'device_app/storagearea_list.html'
    filterset_class = StorageAreaFilter

class StorageList(ListView):
    context_object_name = 'storages'
    model=models.StorageArea

class StorageCreateView(CreateView):
    fields = ('title','street','city','state','zip')
    # fields are used to determine what you can alter in the model
    model=models.StorageArea

class StorageUpdateView(UpdateView):
    fields = ('title','street','city','state','zip')
    model = models.StorageArea

class StorageDetail(DetailView):
    context_object_name = 'storage_detail'
    model=models.StorageArea
    template_name='device_app/storage_details.html'

# Public Dashboard Section ----------------------------------------------------------------------------------------------------------------
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
                            legend_at_bottom_columns=3,
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
                            legend_at_bottom_columns=3,
                            title = 'Campaign Inventory Donated',
                            )
        context['CDI2'] = cht_donated.generate()

        cht_input_dist = OutputFrequency(
                            height=250,
                            width=800,
                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Campaign Output Frequency',
                            )
        context['IOF'] = cht_input_dist.generate()

        return context

def ThanksPublic(request):
    return render(request,'device_app/public_thanks.html')

class Outreach(FormView):
    template_name = 'device_app/public_outreach_request.html'
    form_class = OutreachForm
    #if this is a POST request we need to process the form data
    def post(self, request):
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
            form = OutreachForm(request.POST)
            # check whether it's valid:
            form.is_valid()
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            e = form.cleaned_data['email']
            org = form.cleaned_data['organization']
            r = form.cleaned_data['region']
            c = form.cleaned_data['country']
            n = form.cleaned_data['notes']

            # print(file_path)
            # logo = staticfiles_storage.path('static/pe_logo2.jpg')
            # logo = open(logo, 'rb').read()

            html_template = """\
                        <html>
                        <head></head>
                        <body style= 'background-color: white; color:black'>
                        <p>Hi there Community Organization Team!</p>
                            <p>
                            {} {} has requested our services. They have reached out to us through our public campaign portal. <br><br>
                             They are a representative from {} located in {},{}. Here are the notes they left for us:
                             <br>
                             {}
                            <br>
                            <p>
                            <br>
                            Here is their contact email:
                            <br>
                            {}

                            <br>

                        Regards,
                        <br><br>
                                Automated Project Embrace Emails
                        </p>


                        </body>
                        </html>
                        """.format(fn,ln,org,r,c,n,e)
            port = 465
            sender = 'proememails@gmail.com'
            password = 'meohvgatpjcdrnyt'

            recipients = ['ckinkadedarling@gmail.com']
            message = MIMEMultipart(_subtype='related')
            message["Subject"] = "Project Embrace Campaign Request"
            message["From"] = sender
            message["To"] = ", ".join(recipients)
            message_guts = html_template
            guts1 = MIMEText(message_guts, "html")
            # img = MIMEImage(logo, 'jpeg')
            # img.add_header('Content-Id', '<myimage>')  # angle brackets are important
            # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
            # message.attach(img)
            message.attach(guts1)

            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com", port)
                server.ehlo()
                server.login(sender,password)
                server.send_message(message)
                server.close()
                print('Email Sent!')
            except:
                print('Everything is all fucked!')

            return render(request, 'device_app/public_thanks.html')

        else:
            form = OutreachForm()

            return render(request, 'device_app/public_outreach_request.html', {'form': form})

class Input(FormView):
    template_name = 'device_app/public_input_request.html'
    form_class = OutreachForm
    #if this is a POST request we need to process the form data
    def post(self, request):
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
            form = OutreachForm(request.POST)
            # check whether it's valid:
            form.is_valid()
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            e = form.cleaned_data['email']
            org = form.cleaned_data['organization']
            r = form.cleaned_data['region']
            c = form.cleaned_data['country']
            n = form.cleaned_data['notes']
            # Load the image you want to send as bytes
            # logo = open(static('pe_logo3.jpg')).read()

            html_template = """\
                        <html>
                        <head>
                        </head>
                        <body style= 'background-color: #FFFFFF; color:#000000'>
                            <br>
                            <p>Hi there Outreach Team!</p>
                            <p>
                            {} {} has requested information related to donating medical equipment. They have reached out to us through our public device donation portal. <br><br>
                             They are a representative from {} located in {},{}. Here are the notes they left for us:
                             <br>
                             {}
                            <br>
                            <p>
                            <br>
                            Here is their contact email:
                            <br>
                            {}
                            <br>

                        Regards,
                        <br><br>
                                Automated Project Embrace Emails
                        </p>

                        </body>
                        </html>
                        """.format(fn,ln,org,r,c,n,e)
            port = 465
            sender = 'proememails@gmail.com'
            password = 'meohvgatpjcdrnyt'

            recipients = ['ckinkadedarling@gmail.com']
            message = MIMEMultipart()
            message["Subject"] = "Project Embrace Medical Equipment Donation EXAMPLE"
            message["From"] = sender
            message["To"] = ", ".join(recipients)
            message_guts = html_template
            guts1 = MIMEText(message_guts, "html")
            message.attach(guts1)

            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com", port)
                server.ehlo()
                server.login(sender,password)
                server.send_message(message)
                server.close()
                print('Email Sent!')
            except:
                print('Everything is all fucked!')

            return render(request, 'device_app/public_thanks.html')

        else:
            form = OutreachForm()

        return render(request, 'device_app/public_outreach_request.html', {'form': form})

# Finance Section ----------------------------------------------------------------------------------------------------------------
class ReceiptView(ListView):
    template_name = 'device_app/receipts.html'
    context_object_name = 'donors'
    model=models.Donor
    def post(self, request):
            if request.method=='POST': # form was submitted
                qs = Donor.objects.all()
                donors = read_frame(qs)
                donor_list = donors.id.unique().tolist()
                for donor in donor_list:
                    x_donor = donors[donors.id==donor]
                    x_donor_id=x_donor.iloc[0]['id'].copy()
                    x_donor_status=x_donor.iloc[0]['sent_a_receipt'].copy()
                    if x_donor_status == False:
                        # Updates the database record noting a receipt has been sent to the donor
                        #update_donor_field = Donor.objects.get(id=x_donor_id)
                        #update_donor_field.sent_a_receipt = True
                        #update_donor_field.save()

                        # Gathers email for usage below
                        donor_email = 'connerkinkade@mac.com'
                        #x_donor[['email']]

                        # Gathers device data points related to the donor
                        device_match = Q(**{'donor_id': donor})
                        devices_qs = Device.objects.filter(device_match)
                        devices = read_frame(devices_qs)
                        donor_name = devices.iloc[0]['donor']
                        donor_group = pd.DataFrame(devices.groupby('type').size())

                        donor_group = donor_group.reset_index()
                        donor_group = donor_group.rename(columns={'type':'Type of Device',0:'Number of Devices'})
                        html_template = """\
                                    <html>
                                    <head></head>
                                    <body>
                                    <p>Hi there {}!</p>
                                        <p>
                                        Thank you for donating medical equipment to Project Embrace {}! <br><br>
                                         We can't express how much your donation means to our organization and to those your donation will benefit.<br><br>
                                         This email is your reciept for your donation. The following items are what we cateloged your donation as in our system.<br><br>
                                         Our EIN number for you tax records: 82-1814956
                                        </p>
                                        <table>
                                            <tr>
                                                {}
                                            </tr>
                                        </table>
                                        <br>
                                        <p>
                                        Again we would like to thank you for your donation and your willingness to Give Global Good!
                                        <br>
                                    Regards,
                                    <br><br>
                                            The Project Embrace Team
                                    </p>
                                    </body>
                                    </html>
                                    """.format(donor_name,donor_name,donor_group.to_html(index=False).replace('border="1"','border="0"'))

                        port = 465
                        sender = 'proememails@gmail.com'
                        password = 'meohvgatpjcdrnyt'

                        recipients = ['ckinkadedarling@gmail.com','connerkinkade@mac.com']
                        message = MIMEMultipart()
                        message["Subject"] = "Project Embrace Donation Receipt EXAMPLE"
                        message["From"] = sender
                        message["To"] = ", ".join(recipients)
                        message_guts = html_template
                        guts1 = MIMEText(message_guts, "html")
                        message.attach(guts1)

                        try:
                            server = smtplib.SMTP_SSL("smtp.gmail.com", port)
                            server.ehlo()
                            server.login(sender,password)
                            server.send_message(message)
                            server.close()

                            print('Email Sent!')
                        except:
                            print('Everything is all fucked!')
                    else: # no data submitted
                        no_donors = 'Some donors already received a receipt.'
                        context = {'alternate_output':no_donors}
                        return render(request, 'device_app/receipts.html', context)

                updated_field = 'Donors were sent a receipt'
                context = {'output':updated_field}
                return render(request, 'device_app/receipts.html', context)
            else: # no data submitted
                no_donors = 'There are no donors related to your entered date.'
                context = {'alternate_output':no_donors}
                return render(request, 'device_app/receipts.html', context)

# class EquipmentValue(CreateView):
#     model = models.EquipmentValue
#     fields = ('source','device_type','value')
