"""
    URL configuration for config project.

    The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (MailingListView, MailingCreateView, MessageCreateView,
                           ClientCreateView, MailingDetailView, MailingUpdateView,
                           MailingDeleteView, MailingEndingListView, ClientUpdateView,
                           ClientDeleteView, ClientListView)


app_name = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('completed/', MailingEndingListView.as_view(), name='mailing_complete'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),

    path('message/', MessageCreateView.as_view(), name='message_create'),

    path('client/', ClientCreateView.as_view(), name='client_create'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
]
