from django.urls import path,re_path
from .views import generate_qr_with_image

# urlpatterns = [
#     re_path(r'^generate_qr_with_image/$', generate_qr_with_image, name='generate_qr'),
# ]


urlpatterns = [
    path('generate_qr_with_image/', generate_qr_with_image, name='generate_qr_with_image'),
]

