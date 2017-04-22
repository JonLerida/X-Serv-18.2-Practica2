from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Start, name='Start'),
    url(r'^(\d+)$', views.Petition, name='Petition'),
    url(r'^.*$', views.NoMatch, name='Start'),
]
