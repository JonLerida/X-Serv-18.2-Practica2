from django.conf.urls import url

from . import views

urlpatterns = [
    # /acorta/
    url(r'^$', views.Start, name='Start'),
    # /acorta/[numero]
    url(r'^(\d+)$', views.Petition, name='Petition'),
    # /acorta/cualquiercosa
    url(r'^.*$', views.NoMatch, name='NoMatch'),
]
