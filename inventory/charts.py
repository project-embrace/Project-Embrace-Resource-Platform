from inventory.models import Donor,Device
from django_pandas.io import read_frame
from django.db.models import Q
import pandas as pd
import pygal
import sys,os
from pathlib import Path
from pygal import Config
# Inventory Visualizations
class InventoryTable():
    def __init__(self,**kwargs):
        self.chart = pygal.Bar(**kwargs)

    def get_data(self):
        qs = Device.objects.all()
        pei = read_frame(qs)
        dono_counts = pd.DataFrame(pei.groupby('donated_to_recipient').size())
        dono_counts = dono_counts.rename(columns={0:'count'})
        dono_counts = dono_counts.reset_index()

        pei_donated = dono_counts[dono_counts.donated_to_recipient ==True]
        pei_donated = pei_donated.iloc[0,1]

        pei_not_donated= dono_counts[dono_counts.donated_to_recipient == False]
        pei_not_donated = pei_not_donated.iloc[0,1]

        processed_counts = pd.DataFrame(pei.groupby('processed').size())
        processed_counts = processed_counts.rename(columns={0:'count'})
        processed_counts = processed_counts.reset_index()

        pei_unprocessed = processed_counts[processed_counts.processed ==False]
        pei_unprocessed = processed_counts.iloc[0,1]

        pei_processed = processed_counts[processed_counts.processed ==True]
        pei_processed = pei_processed.iloc[0,1]

        return pei_donated, pei_not_donated, pei_unprocessed, pei_processed

    def generate(self):

        pei_donated, pei_not_donated, pei_unprocessed, pei_processed = self.get_data()
        self.chart.add('Total Current Inventory',pei_not_donated)
        self.chart.add('Total Unprocessed Inventory',pei_unprocessed)
        self.chart.add('Total Processed Inventory',pei_processed)
        self.chart.add('Total Donated Inventory',pei_donated)

        # Return the rendered SVG
        return self.chart.render_table(style=True)
class ReadyToDonatePieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)

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
