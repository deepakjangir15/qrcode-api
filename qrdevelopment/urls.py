from django.urls import path,re_path
from .views import generate_qr

urlpatterns = [
    re_path(r'^generate_qr/$', generate_qr, name='generate_qr'),
]
