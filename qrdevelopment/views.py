from django.shortcuts import render

# Create your views here.
import qrcode
from django.http import HttpResponse
from io import BytesIO

def generate_qr(request, url):
    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
