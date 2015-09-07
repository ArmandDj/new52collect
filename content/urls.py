from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^browse/$', views.browse, name='browse'),	
	url(r'^browse/(?P<browse_by>[A-Za-z]+)/$', views.browse_by, name='browse_by'),
	url(r'^search/(?P<search_by>[A-Za-z]+)/$', views.search, name='search'),
	url(r'^comic/(?P<series>[A-Za-z ()0-9:]+)/(?P<issue>[0-9]+)/$', views.comic, name='comic'),
	url(r'^review/(?P<series>[A-Za-z ()0-9:]+)/(?P<issue>[0-9]+)/(?P<id>[-0-9]+)/$', views.review, name='review'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^login/e=(?P<error>[0-9])&m=(?P<message>[0-9])/$', views.login_view, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register/e=(?P<error>[0-9])$', views.register, name='register'),
	url(r'^account_request/(?P<type>[A-Za-z]+)/$', views.account_request, name='account_request'),
	url(r'^review/(?P<series>[A-Za-z ()0-9:]+)/(?P<issue>[0-9]+)/(?P<action>[A-Za-z]+)/$', views.ownership, name='ownership'),
	url(r'^collection/$', views.collection, name='collection'),	
	url(r'^collection/(?P<listing>[A-Za-z]+)/$', views.collection_other, name='collection_other'),
	url(r'^rating/(?P<series>[A-Za-z ()0-9:]+)/(?P<issue>[0-9]+)/$', views.rating, name='rating'),
	url(r'^reading/$', views.reading, name='reading'),
)