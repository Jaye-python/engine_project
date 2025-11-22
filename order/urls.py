from django.urls import path

from . import views

urlpatterns = [
    path("rules/check/", views.CheckRulesView.as_view(), name="check_rules"),
]
