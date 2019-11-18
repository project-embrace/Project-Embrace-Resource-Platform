"""ProjEmb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import include, path
from common.views import handler404, handler500

app_name = 'ProjEmb'

urlpatterns = [

    path('', include('common.urls', namespace="common")),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('cases/', include('cases.urls', namespace="cases")),
    path('contacts/', include('contacts.urls', namespace="contacts")),
    path('emails/', include('emails.urls', namespace="emails")),
    path('events/', include('events.urls', namespace="events")),
    path('inventory/',include('inventory.urls',namespace='inventory')),
    path('invoices/', include('invoices.urls', namespace="invoices")),
    path('leads/', include('leads.urls', namespace="leads")),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name="logout"),
    path('marketing/', include('marketing.urls', namespace="marketing")),
    path('opportunities/',
         include('opportunity.urls', namespace="opportunities")),
    path('tasks/', include('tasks.urls', namespace="tasks")),
    path('teams/', include('teams.urls', namespace="teams")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = handler404
handler500 = handler500
