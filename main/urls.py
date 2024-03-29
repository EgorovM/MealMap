# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
	url(r'^register/$',                          views.register, name = 'register'),
    url(r'^settings/$',                          views.settings,  name = 'settings'),
    url(r'^picture/$',                          views.picture,  name = 'picture'),
    url(r'^profile/(?P<views_profile_id>[0-9]+)/$', views.profile,     name = 'profile'),
    url(r'^logout_view/$',                           views.logout_view,     name = 'logout'),
    url(r'^login/$',                           views.login,     name = 'login'),
    url(r'^plus/$',                           views.plus,     name = 'plus'),
    url(r'^about/$',                           views.about,     name = 'about'),
    # url(r'^(?P<order_id>[0-9]+)/$', views.order, name='order'),
    # url(r'^login/$', views.login, name = 'login'),
    # url(r'^logout/$', views.logout, name = 'logout'),
    # url(r'^loginned/$', views.logginned, name = 'loginok'),
    # url(r'^order/(?P<edit_order_id>[0-9]+)/$', views.edit, name='edit'),
    # url(r'^editprofile/(?P<edit_profile_id>[0-9]+)/$', views.editprofile,name='editprofile'),
    # url(r'^profile/(?P<views_profile_id>[0-9]+)/$', views.profile,name='profile')
]
