from device_app.models import Donor,Device
from django_pandas.io import read_frame
from django.db.models import Q
import pandas as pd
import pygal
import sys,os
from pathlib import Path
from pygal import Config
# Inventory Visualizations
class ReadyToDonatePieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Treemap(**kwargs)

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.filter(donated_to_recipient=False,processed=True,condition='A')
        pei = read_frame(qs)
        ready_to_distribute = pd.DataFrame(pei.groupby('type')['condition'].count())
        ready_to_distribute = ready_to_distribute.reset_index()
        ready_to_distribute = ready_to_distribute.rename(columns = {'condition':'count'})
        ready_to_distribute = ready_to_distribute.set_index('type')['count'].to_dict()

        return ready_to_distribute

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
class DonatedPieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Treemap(**kwargs)
        #self.chart.title = 'Donated Inventory'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.filter(donated_to_recipient=True)

        pei= read_frame(qs)

        ready_to_distribute=pd.DataFrame(pei.groupby('type')['condition'].count())
        ready_to_distribute=ready_to_distribute.reset_index()
        ready_to_distribute = ready_to_distribute.rename(columns = {'condition':'count'})
        ready_to_distribute = ready_to_distribute.set_index('type')['count'].to_dict()

        return ready_to_distribute

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
class DirtyInventory():

    def __init__(self, **kwargs):
        self.chart = pygal.Treemap(**kwargs)

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.filter(donated_to_recipient=False,processed=False)

        pei= read_frame(qs)

        dirty=pd.DataFrame(pei.groupby('type')['condition'].count())
        dirty=dirty.reset_index()
        dirty = dirty.rename(columns = {'condition':'count'})
        dirty = dirty.set_index('type')['count'].to_dict()

        return dirty
    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
class InputFrequency():

    def __init__(self, **kwargs):
        self.chart = pygal.Line(**kwargs)

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.all()

        pei= read_frame(qs)

        pei = pd.DataFrame(pei.groupby('date_donated_to_project_embrace').size())
        pei = pei.rename(columns={0:'Count'})
        pei = pei.reset_index()
        pei_list = pei.set_index('date_donated_to_project_embrace')['Count'].to_list()
        labels = pei['date_donated_to_project_embrace']
        return pei_list, labels

    def generate(self):
        # Get chart data
        pei_list, labels = self.get_data()
        self.chart.x_labels = map(str,labels)
        self.chart.add('Inventory',pei_list)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
class OutputFrequency():

    def __init__(self, **kwargs):
        self.chart = pygal.Line(**kwargs)

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.filter(donated_to_recipient=True)

        pei= read_frame(qs)

        pei = pd.DataFrame(pei.groupby('date_donated_to_recipient').size())
        pei = pei.rename(columns={0:'Count'})
        pei = pei.reset_index()
        pei_list = pei.set_index('date_donated_to_recipient')['Count'].to_list()
        labels = pei['date_donated_to_recipient']
        return pei_list, labels

    def generate(self):
        # Get chart data
        pei_list, labels = self.get_data()
        self.chart.x_labels = map(str,labels)
        self.chart.add('Inventory',pei_list)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


# Finance Visualizations
