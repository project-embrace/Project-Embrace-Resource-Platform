from django.shortcuts import render,redirect,get_object_or_404
from inventory.forms import UserForm,OutreachForm,DocumentForm,FinDocumentForm
from django.utils.decorators import method_decorator
from django.db.models import Q
import json
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import(Http404,HttpResponseRedirect,HttpResponse,
                        FileResponse,JsonResponse)
from .tables import (DeviceTable,DonorTable,CampaignTable,
                     DonoHouseTable,StorageTable,EquipmentValueTable)
from .filters import (DeviceFilter,DonorFilter,
                      CampaignFilter,DonationHouseFilter,
                      StorageAreaFilter,EquipmentValueFilter)
from .charts import (ReadyToDonatePieChart,
                     DonatedPieChart,
                     InputFrequency,
                     OutputFrequency,
                     DirtyInventory,
                     InventoryTable)
from inventory.models import (KBDocument,Device,Donor,
                              DonationHouse,StorageArea,
                              Campaign,EquipmentValue,
                              FinDocument)

from common.models import Document,User
from teams.models import Teams
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
    return render(request,'inventory/operations_index.html')

def landing_index(request):
    return render(request,'inventory/landing_index.html')

def finance_index(request):
    return render(request,'inventory/finance_index.html')

def marketing_index(request):
    return render(request,'inventory/marketing_index.html')

def relationship_index(request):
    return render(request,'inventory/relationship_index.html')

def knowledge_index(request):
    return render(request,'inventory/knowledge_index.html')

def tutorial(request):
    return render(request,'inventory/tutorial.html')

def public_dash(request):
    return render(request,'inventory/public_dash_index.html')

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
        return render(request,"inventory/login.html")

# class user_login(FormView):
#     template_name = 'inventory/login.html'
#     form_class = LoginForm
#     #if this is a POST request we need to process the form data
#     def post(self, request):
#         if request.method == 'POST':
#                 # create a form instance and populate it with data from the request:
#             form = LoginForm(request.POST)
#             # check whether it's valid:
#             form.is_valid()
#             username = form.cleaned_data['user']
#             password = form.cleaned_data['pw']
#
#             user = authenticate(username=username,password=password)
#
#             if user:
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponseRedirect(reverse('landing_index'))
#                 else:
#                     return HttpResponse('ACCOUNT NOT ACTIVE')
#             else:
#                 print('Someone tried to login and failed')
#                 print("username: {} password {}".format(username,password))
#                 return HttpResponse("invalid login details supplied")
#         else:
#             return render(request,"inventory/login.html")

# CRUD items ----------------------------------------------------------------------------------------------------------------
# Operations Section ----------------------------------------------------------------------------------------------------------------
## Donor Section ----------------------------------------------------------------------------------------------------------------
class FilteredDonorList(SingleTableMixin, FilterView):
    model = Donor
    table_class = DonorTable
    template_name = 'inventory/donor_list.html'
    filterset_class = DonorFilter

# class DonorList(ListView):
#     context_object_name = 'donors'
#     model=models.Donor
#
#     # Search Code
#     def post(self, request):
#             keywords=''
#
#             if request.method=='POST': # form was submitted
#
#                 keywords = request.POST.get("ds", "") # <input type="text" name="keywords">
#                 all_queries = None
#                 search_fields = ('donation_house__title','name','donation_date') # change accordingly
#                 for keyword in keywords.split(' '): # keywords are splitted into words (eg: john science library)
#                     keyword_query = None
#                     for field in search_fields:
#                         each_query = Q(**{field + '__icontains': keyword})
#                         if not keyword_query:
#                             keyword_query = each_query
#                         else:
#                             keyword_query = keyword_query | each_query
#                             if not all_queries:
#                                 all_queries = keyword_query
#                             else:
#                                 all_queries = all_queries & keyword_query
#
#                 searchD= Donor.objects.filter(all_queries).distinct()
#                 context = {'searchD':searchD}
#                 return render(request, 'inventory/donor_list.html', context)
#
#             else: # no data submitted
#
#                 context = {}
#                 return render(request, 'inventory/ops_index.html', context)

class DonorDetail(DetailView):
   context_object_name = 'donor_detail'
   model=Donor
   template_name='inventory/donor_details.html'

class DonorCreateView(CreateView):
    fields = ('name','email','region','country','donation_date','donation_house')
    # fields are used to determine what you can alter in the model
    model=Donor

class DonorUpdateView(UpdateView):
    fields = ('name','email')
    model = Donor

class DonorDeleteView(DeleteView):
    model = Donor
    success_url = reverse_lazy("inventory:donor_list")

## Device Section ----------------------------------------------------------------------------------------------------------------
class FilteredDeviceList(ExportMixin,SingleTableMixin, FilterView,):
    model = Device
    table_class = DeviceTable
    template_name = 'inventory/device_list.html'
    filterset_class = DeviceFilter
    export_formats = ("csv",)

class DeviceDetail(DetailView):
   context_object_name = 'device_detail'
   model=Device
   template_name='inventory/device_details.html'

class DeviceCreateView(CreateView):
    fields = ('date_donated_to_project_embrace','type',
              'condition','donor','campaign','storage_area',
              'storage_unit','storage_unit_quadrant',
              'processed','unique_information')
    # fields are used to determine what you can alter in the model
    model=Device

class DeviceUpdateView(UpdateView):
    fields = ('type','condition','donor',
              'campaign','storage_area','processed',
              'storage_unit','storage_unit_quadrant',
              'donated_to_recipient','unique_information',
              'date_donated_to_recipient')
    model = Device

class DeviceDeleteView(DeleteView):
    model = Device
    success_url = reverse_lazy("inventory:device_list")

class DeviceVisualsView(TemplateView):
    template_name = 'inventory/device_dash.html'
    def get_context_data(self, **kwargs):
        context = super(DeviceVisualsView, self).get_context_data(**kwargs)
        custom_style = Style(colors=('#BE1E2D',))
        cht_readytodonate = ReadyToDonatePieChart(
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            show_legend=False,
                            # legend_at_bottom = True,
                            # legend_at_bottom_columns=3,
                            title='Processed Inventory'
                            )
        context['PI'] = cht_readytodonate.generate()

        cht_donated = DonatedPieChart(
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            show_legend=False,
                            #legend_at_bottom = True,
                            #legend_at_bottom_columns=3,
                            title = 'Campaign Inventory Donated',
                            )
        context['CID'] = cht_donated.generate()

        cht_input_dist = DirtyInventory(
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            show_legend=False,
                            #legend_at_bottom = True,
                            #legend_at_bottom_columns=3,
                            title = 'Non-Processed Inventory',
                            )
        context['NPI'] = cht_input_dist.generate()

        cht_input_dist = InputFrequency(
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Inventory Input Frequency',
                            )
        context['IIF'] = cht_input_dist.generate()

        cht_input_dist = OutputFrequency(
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Campaign Output Frequency',
                            )
        context['IOF'] = cht_input_dist.generate()

        cht_inventory_table = InventoryTable(
                            opacity='.6',
                            opacity_hover='.9',
                            style=custom_style,
                            show_legend=False,
                            #legend_at_bottom = True,
                            #legend_at_bottom_columns=3,
                            title='Processed Inventory'
                            )
        context['IT'] = cht_inventory_table.generate()

        return context

## Donation House Section ----------------------------------------------------------------------------------------------------------------

class FilteredDonationHouseList(SingleTableMixin, FilterView):
    model = DonationHouse
    table_class = DonoHouseTable
    template_name = 'inventory/donationhouse_list.html'
    filterset_class = DonationHouseFilter

class DonationHouseList(ListView):
    context_object_name = 'donationhouses'
    model=DonationHouse

class DonationHouseCreateView(CreateView):
    fields = ('title','street','city','state','zip')
    # fields are used to determine what you can alter in the model
    model=DonationHouse

class DonationHouseUpdateView(UpdateView):
    fields = ('title','street','city','state','zip')
    model = DonationHouse

class DonationHouseDetail(DetailView):
   context_object_name = 'donationhouse_detail'
   model=DonationHouse
   template_name='inventory/donationhouse_details.html'

## Campaign Section ----------------------------------------------------------------------------------------------------------------
class FilteredCampaignList(SingleTableMixin, FilterView):
    model = Campaign
    table_class = CampaignTable
    template_name = 'inventory/campaign_list.html'
    filterset_class = CampaignFilter

class CampaignList(ListView):
    context_object_name = 'campaigns'
    model=Campaign

class CampaignDetail(DetailView):
   context_object_name = 'campaign_detail'
   model=Campaign
   template_name='inventory/campaign_details.html'

class CampaignCreateView(CreateView):
     fields = ('title','region','country','start_date','end_date')
     # fields are used to determine what you can alter in the model
     model=Campaign

class CampaignUpdateView(UpdateView):
     fields = ('title','region','country','end_date')
     model = Campaign

# class FilteredDeviceList(ExportMixin,SingleTableMixin, FilterView,):
#     model = Device
#     table_class = DeviceListTable
#     template_name = 'inventory/device_list.html'
#     filterset_class = DeviceFilter
#     export_formats = ("csv",)

## Storage Area Section ----------------------------------------------------------------------------------------------------------------

class FilteredStorageList(SingleTableMixin, FilterView):
    model = StorageArea
    table_class = StorageTable
    template_name = 'inventory/storagearea_list.html'
    filterset_class = StorageAreaFilter

class StorageList(ListView):
    context_object_name = 'storages'
    model=StorageArea

class StorageCreateView(CreateView):
    fields = ('title','street','city','state','zip')
    # fields are used to determine what you can alter in the model
    model=StorageArea

class StorageUpdateView(UpdateView):
    fields = ('title','street','city','state','zip')
    model = StorageArea

class StorageDetail(DetailView):
    context_object_name = 'storage_detail'
    model=StorageArea
    template_name='inventory/storage_details.html'

# Public Dashboard Section ----------------------------------------------------------------------------------------------------------------
class PublicDashView(TemplateView):
    template_name = 'inventory/public_dash_inventory.html'
    def get_context_data(self, **kwargs):
        context = super(PublicDashView, self).get_context_data(**kwargs)
        custom_style = Style(colors=('#BE1E2D',))
        cht_readytodonate = ReadyToDonatePieChart(
                            # height=300,
                            # width=800,
                            # explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            show_legend=False,
                            # legend_at_bottom = True,
                            # legend_at_bottom_columns=3,
                            title='Inventory Ready for Donation'
                            )
        context['CI2'] = cht_readytodonate.generate()

        cht_donated = DonatedPieChart(
                            # height=300,
                            # width=800,
                            # explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            show_legend=False,
                            # legend_at_bottom = True,
                            # legend_at_bottom_columns=3,
                            title = 'Campaign Inventory Donated',
                            )
        context['CDI2'] = cht_donated.generate()

        cht_input_dist = OutputFrequency(

                            explicit_size=True,
                            style=custom_style,
                            opacity='.6',
                            opacity_hover='.9',
                            title = 'Campaign Output Frequency',
                            )
        context['IOF'] = cht_input_dist.generate()

        return context

def ThanksPublic(request):
    return render(request,'inventory/public_thanks.html')

def PublicDataPolicy(request):
    return render(request,'inventory/public_data_policy.html')

class Outreach(FormView):
    template_name = 'inventory/public_outreach_request.html'
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
                            <br>
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

            recipients = ['outreach@projectembrace.org']
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

            return render(request, 'inventory/public_thanks.html')

        else:
            form = OutreachForm()

            return render(request, 'inventory/public_outreach_request.html', {'form': form})

class Input(FormView):
    template_name = 'inventory/public_input_request.html'
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
                            <br>
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

            recipients = ['abigail@projectembrace.org']
            message = MIMEMultipart()
            message["Subject"] = "Project Embrace Medical Equipment Donation Offering"
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

            return render(request, 'inventory/public_thanks.html')

        else:
            form = OutreachForm()

        return render(request, 'inventory/public_outreach_request.html', {'form': form})

# Finance Section ----------------------------------------------------------------------------------------------------------------
class ReceiptView(ListView):
    template_name = 'inventory/receipts.html'
    context_object_name = 'donors'
    model=Donor
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
                        return render(request, 'inventory/receipts.html', context)

                updated_field = 'Donors were sent a receipt'
                context = {'output':updated_field}
                return render(request, 'inventory/receipts.html', context)
            else: # no data submitted
                no_donors = 'There are no donors who have not been sent a receipt.'
                context = {'alternate_output':no_donors}
                return render(request, 'inventory/receipts.html', context)



# EquipmentValue Section --------------------------------------------------------------------------------------------------

class FilteredEquipmentList(SingleTableMixin, FilterView):
    model = EquipmentValue
    table_class = EquipmentValueTable
    template_name = 'inventory/equipmentvalue_list.html'
    filterset_class = EquipmentValueFilter

class EquipmentValueDetail(DetailView):
   context_object_name = 'equipment_detail'
   model=EquipmentValue
   template_name='inventory/equipmentvalue_details.html'

class EquipmentValueUpdate(UpdateView):
     model = EquipmentValue
     fields = ('source','device_type','source_value')

class EquipmentValueCreate(CreateView):
        model = EquipmentValue
        fields = ('source','device_type','source_value')

class EquipmentValueDeleteView(DeleteView):
    model = EquipmentValue
    success_url = reverse_lazy("inventory:equipment_list")


# Knowledge Base Section -------------------------------------------

def document_create(request):
    template_name = "inventory/doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        users = User.objects.filter(is_active=True).order_by('email')
    else:
        users = User.objects.filter(role='ADMIN').order_by('email')
    form = DocumentForm(users=users)
    if request.POST:
        form = DocumentForm(request.POST, request.FILES, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))
            if request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=request.POST.getlist(
                    'teams')).values_list('users', flat=True)
                assinged_to_users_ids = doc.shared_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        doc.shared_to.add(user_id)

            if request.POST.getlist('teams', []):
                doc.teams.add(*request.POST.getlist('teams'))

            data = {'success_url': reverse_lazy(
                'inventory:knowledge_index'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_form"] = form
    context["users"] = users
    context["teams"] = Teams.objects.all()
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('assigned_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentListView(LoginRequiredMixin, TemplateView):
    model = KBDocument
    context_object_name = "documents"
    template_name = "inventory/knowledge_index.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.is_superuser or self.request.user.role == "ADMIN":
            queryset = queryset
        else:
            if self.request.user.documents():
                doc_ids = self.request.user.documents().values_list('id',
                                                                    flat=True)
                shared_ids = queryset.filter(
                    Q(status='active') &
                    Q(shared_to__id__in=[self.request.user.id])).values_list(
                    'id', flat=True)
                queryset = queryset.filter(
                    Q(id__in=doc_ids) | Q(id__in=shared_ids))
            else:
                queryset = queryset.filter(Q(status='active') & Q(
                    shared_to__id__in=[self.request.user.id]))

        request_post = self.request.POST
        if request_post:
            if request_post.get('doc_name'):
                queryset = queryset.filter(
                    title__icontains=request_post.get('doc_name'))
            if request_post.get('status'):
                queryset = queryset.filter(status=request_post.get('status'))

            if request_post.getlist('shared_to'):
                queryset = queryset.filter(
                    shared_to__id__in=request_post.getlist('shared_to'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(
            is_active=True).order_by('email')
        context["documents"] = self.get_queryset()
        context["status_choices"] = KBDocument.DOCUMENT_STATUS_CHOICE
        context["sharedto_list"] = [
            int(i) for i in self.request.POST.getlist('shared_to', []) if i]
        context["per_page"] = self.request.POST.get('per_page')

        search = False
        if (
            self.request.POST.get('doc_name') or
            self.request.POST.get('status') or
            self.request.POST.get('shared_to')
        ):
            search = True

        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = KBDocument

    def get(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if not request.user == KBDocument.objects.get(id=kwargs['pk']).created_by:
                raise PermissionDenied
        self.object = self.get_object()
        self.object.delete()
        return redirect("inventory:knowledge_index")


@login_required
def document_update(request, pk):
    template_name = "inventory/doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        users = User.objects.filter(is_active=True).order_by('email')
    else:
        users = User.objects.filter(role='ADMIN').order_by('email')
    document = KBDocument.objects.filter(id=pk).first()
    form = DocumentForm(users=users, instance=document)

    if request.POST:
        form = DocumentForm(request.POST, request.FILES,
                            instance=document, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.save()

            doc.shared_to.clear()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))

            if request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=request.POST.getlist(
                    'teams')).values_list('users', flat=True)
                assinged_to_users_ids = doc.shared_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        doc.shared_to.add(user_id)

            if request.POST.getlist('teams', []):
                doc.teams.clear()
                doc.teams.add(*request.POST.getlist('teams'))
            else:
                doc.teams.clear()

            data = {'success_url': reverse_lazy(
                'inventory:knowledge_index'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_obj"] = document
    context["doc_form"] = form
    context["doc_file_name"] = context["doc_obj"].document_file.name.split(
        "/")[-1]
    context["users"] = users
    context["teams"] = Teams.objects.all()
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('shared_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = KBDocument
    template_name = "inventory/doc_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if (not request.user ==
                    KBDocument.objects.get(id=kwargs['pk']).created_by):
                raise PermissionDenied

        return super(DocumentDetailView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context.update({
            "file_type_code": self.object.file_type()[1],
            "doc_obj": self.object,
        })
        return context


def download_document(request, pk):
    # doc_obj = Document.objects.filter(id=pk).last()
    doc_obj = KBDocument.objects.get(id=pk)
    if doc_obj:
        if not request.user.role == 'ADMIN':
            if (not request.user == doc_obj.created_by and
                    request.user not in doc_obj.shared_to.all()):
                raise PermissionDenied
        if settings.STORAGE_TYPE == "normal":
            # print('no no no no')
            path = doc_obj.document_file.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    return response
        else:
            file_path = doc_obj.document_file
            file_name = doc_obj.title
            # print(file_path)
            # print(file_name)
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource('s3')
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                # print('got it')
                with open(file_name, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

            return path
    raise Http404



# Finance Knowledge Base Section -------------------------------------------

def FinDocumentCreate(request):
    template_name = "inventory/fin_doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        users = User.objects.filter(is_active=True).order_by('email')
    else:
        users = User.objects.filter(role='ADMIN').order_by('email')
    form = FinDocumentForm(users=users)
    if request.POST:
        form = FinDocumentForm(request.POST, request.FILES, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))
            if request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=request.POST.getlist(
                    'teams')).values_list('users', flat=True)
                assinged_to_users_ids = doc.shared_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        doc.shared_to.add(user_id)

            if request.POST.getlist('teams', []):
                doc.teams.add(*request.POST.getlist('teams'))

            data = {'success_url': reverse_lazy(
                'inventory:finance_kb'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_form"] = form
    context["users"] = users
    context["teams"] = Teams.objects.all()
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('assigned_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class FinDocumentListView(LoginRequiredMixin, TemplateView):
    model = FinDocument
    context_object_name = "documents"
    template_name = "inventory/finance_kb.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.is_superuser or self.request.user.role == "ADMIN":
            queryset = queryset
        else:
            if self.request.user.documents():
                doc_ids = self.request.user.documents().values_list('id',
                                                                    flat=True)
                shared_ids = queryset.filter(
                    Q(status='active') &
                    Q(shared_to__id__in=[self.request.user.id])).values_list(
                    'id', flat=True)
                queryset = queryset.filter(
                    Q(id__in=doc_ids) | Q(id__in=shared_ids))
            else:
                queryset = queryset.filter(Q(status='active') & Q(
                    shared_to__id__in=[self.request.user.id]))

        request_post = self.request.POST
        if request_post:
            if request_post.get('doc_name'):
                queryset = queryset.filter(
                    title__icontains=request_post.get('doc_name'))
            if request_post.get('status'):
                queryset = queryset.filter(status=request_post.get('status'))

            if request_post.getlist('shared_to'):
                queryset = queryset.filter(
                    shared_to__id__in=request_post.getlist('shared_to'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FinDocumentListView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(
            is_active=True).order_by('email')
        context["documents"] = self.get_queryset()
        context["status_choices"] = FinDocument.DOCUMENT_STATUS_CHOICE
        context["sharedto_list"] = [
            int(i) for i in self.request.POST.getlist('shared_to', []) if i]
        context["per_page"] = self.request.POST.get('per_page')

        search = False
        if (
            self.request.POST.get('doc_name') or
            self.request.POST.get('status') or
            self.request.POST.get('shared_to')
        ):
            search = True

        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class FinDocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = FinDocument

    def get(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if not request.user == FinDocument.objects.get(id=kwargs['pk']).created_by:
                raise PermissionDenied
        self.object = self.get_object()
        self.object.delete()
        return redirect("inventory:finance_kb")


@login_required
def FinDocumentUpdate(request, pk):
    template_name = "inventory/fin_doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        users = User.objects.filter(is_active=True).order_by('email')
    else:
        users = User.objects.filter(role='ADMIN').order_by('email')
    document = FinDocument.objects.filter(id=pk).first()
    form = DocumentForm(users=users, instance=document)

    if request.POST:
        form = DocumentForm(request.POST, request.FILES,
                            instance=document, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.save()

            doc.shared_to.clear()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))

            if request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=request.POST.getlist(
                    'teams')).values_list('users', flat=True)
                assinged_to_users_ids = doc.shared_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        doc.shared_to.add(user_id)

            if request.POST.getlist('teams', []):
                doc.teams.clear()
                doc.teams.add(*request.POST.getlist('teams'))
            else:
                doc.teams.clear()

            data = {'success_url': reverse_lazy(
                'inventory:finance_kb'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_obj"] = document
    context["doc_form"] = form
    context["doc_file_name"] = context["doc_obj"].document_file.name.split(
        "/")[-1]
    context["users"] = users
    context["teams"] = Teams.objects.all()
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('shared_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class FinDocumentDetailView(LoginRequiredMixin, DetailView):
    model = FinDocument
    template_name = "inventory/fin_doc_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if (not request.user ==
                    FinDocument.objects.get(id=kwargs['pk']).created_by):
                raise PermissionDenied

        return super(FinDocumentDetailView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FinDocumentDetailView, self).get_context_data(**kwargs)
        context.update({
            "file_type_code": self.object.file_type()[1],
            "doc_obj": self.object,
        })
        return context


def FinDownloadDocument(request, pk):
    doc_obj = FinDocument.objects.get(id=pk)
    if doc_obj:
        if not request.user.role == 'ADMIN':
            if (not request.user == doc_obj.created_by and
                    request.user not in doc_obj.shared_to.all()):
                raise PermissionDenied
        if settings.STORAGE_TYPE == "normal":
            # print('no no no no')
            path = doc_obj.document_file.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    return response
        else:
            file_path = doc_obj.document_file
            file_name = doc_obj.title
            # print(file_path)
            # print(file_name)
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource('s3')
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                # print('got it')
                with open(file_name, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

            return path
    raise Http404
