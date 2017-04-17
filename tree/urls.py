from django.conf.urls import url
from tree import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^generate$', views.generate, name='generate'),
	url(r'^delete$', views.delete, name='delete'),
	url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'),
]
