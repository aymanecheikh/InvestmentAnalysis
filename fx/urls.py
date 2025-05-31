from django.urls import path
from fx import views

urlpatterns = [path("", views.consuming_tiingo_api, name="consuming_tiingo_api")]
