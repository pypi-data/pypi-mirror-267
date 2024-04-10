from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^get-code/', views.obtain_code_token, name='get-code'),
    re_path('^auth/', views.obtain_auth_token, name='auth'),
    re_path('^refresh/', views.refresh_auth_token, name='refresh'),
    re_path('^verify/', views.verify_auth_token, name='verify'),
]
