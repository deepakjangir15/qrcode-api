from django.urls import path,re_path
from .views import generate_qr_with_image,generate_simple_qr,generate_qr_with_image_file,generate_colored_qr

# urlpatterns = [
#     re_path(r'^generate_qr_with_image/$', generate_qr_with_image, name='generate_qr'),
# ]


urlpatterns = [
    path('generate_qr_with_image/', generate_qr_with_image, name='generate_qr_with_image'),
    path('generate_qr_with_image_file/', generate_qr_with_image_file, name='generate_qr_with_image_file'),
    path('generate_simple_qr/', generate_simple_qr, name='generate_simple_qr'),
    path('generate_colored_qr/', generate_colored_qr, name='generate_colored_qr'),
]

