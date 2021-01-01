# coding =utf-8

from django.conf.urls import url
from . import views
urlpatterns = [
    url('quary', views.quary),
url('listcity', views.listcity),
url('state', views.state),
url('prodict', views.prodict),

]