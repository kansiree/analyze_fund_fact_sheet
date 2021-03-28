from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('fund', views.fund, name='fund'),
    path('fundByStatus', views.fundByStatus, name='fundByStatus'),
]