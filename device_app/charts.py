from device_app.models import Donor,Device
from django_pandas.io import read_frame
from django.db.models import Q
import pandas as pd
import pygal
import sys,os
from pathlib import Path

class ReadyToDonatePieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'Current Inventory'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        qs = Device.objects.filter(donated_to_recipient=False,processed=True,condition='A')

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


# if os.path.exists("/Users/kinkadedarling/Desktop/Project_Embrace/Software/proem-ims-heroku-live/projemb-device-app/static/") :
#     # Change the current working Directory
#     os.chdir("/Users/kinkadedarling/Desktop/Project_Embrace/Software/proem-ims-heroku-live/projemb-device-app/static/")
