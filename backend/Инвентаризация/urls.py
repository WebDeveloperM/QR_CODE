from django.urls import path
from Инвентаризация.views import *
from .models import register_computer

urlpatterns = [
    path("all_compyuters/", CoreApiView.as_view()),
    path("all_texnology/", TexnologyApiView.as_view()),
    path("get-data-from-agent/", GetTexnologyFromAgent.as_view()),
    path("comp_detail/<slug:slug>", CompDetailApiView.as_view()),
    path("comp_delete/<slug:slug>", CompDeleteApiView.as_view()),
    path("add-compyuter/", AddCompyuterApiView.as_view()),
    path("edit-compyuter/<str:slug>/", EditCompyuterApiView.as_view()),
    path("get-data/", upload_excel, name="upload-excel"),
    path("get-data/<str:ip>/", GetDataByIPApiView.as_view()),
    path("info-comp/", InfoCompyuterApiView.as_view()),
    path("filter-data/", FilterDataByIPApiView.as_view()),
    path("register_computer/", register_computer),
    path('get-mac/', GetComputerWithMac.as_view(), name='get_mac'),


]
