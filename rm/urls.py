from django.contrib import admin
from django.urls import path,include
from rm import rm_views
app_name = 'rm'

urlpatterns = [
path('relationship_management/',rm_views.relationship_index,name='relationship_index'),
]
