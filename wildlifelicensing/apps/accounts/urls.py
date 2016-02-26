from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^validation-sent/$', views.ValidationSentView.as_view(), name='validation_sent'),

    url(r'^verification/(?P<token>[^/]+)/$', views.VerificationView.as_view(), name='verification'),

    url('^logout/', auth_views.logout, {'next_page': 'home'}, name='logout'),

    url(r'create/?$', views.CustomerCreateView.as_view(), name='customer_create'),

]