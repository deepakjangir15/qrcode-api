from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import qrcode
from django.http import HttpResponse
from io import BytesIO
from PIL import Image, ImageDraw
import base64
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask

# 1. Uses File Image in Post request
@csrf_exempt
def generate_qr_with_image_file(request):
    basewidth = 100

    if request.method == 'POST':
        url = request.POST.get('url', '')
        image_data = request.FILES.get('image', '')
        QRcolor = request.POST.get('color', '')
        if image_data:
            # Load image
            image = Image.open(image_data)

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            logo = image.resize((basewidth, hsize), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )

            # adding URL or text to QRcode
            QRcode.add_data(url)

            # generating QR code
            QRcode.make()

            # taking color name from user
            # QRcolor = 'Green'

            # adding color to QR code
            QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB')

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)


            # Save image data to buffer
            buffer = BytesIO()
            QRimg.save(buffer, format='PNG')
            image_png = buffer.getvalue()
            buffer.close()

            # Return image as HTTP response
            response = HttpResponse(image_png, content_type="image/png")
            return response
    return HttpResponse(status=405)

# 2. Uses base64 as the input in post request
@csrf_exempt
def generate_qr_with_image(request):
    basewidth = 100

    if request.method == 'POST':
        url = request.POST.get('url', '')
        base64_image = request.POST.get('base64_image','')
        QRcolor = request.POST.get('qrcolor', '')
        BGcolor = request.POST.get('bgcolor', '')

        if base64_image:
            # Load image
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            logo = image.resize((basewidth, hsize), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )

            # adding URL or text to QRcode
            QRcode.add_data(url)

            # generating QR code
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image(fill_color=QRcolor, back_color=BGcolor).convert('RGB')

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)


            # Save image data to buffer
            buffer = BytesIO()
            QRimg.save(buffer, format='PNG')
            image_png = buffer.getvalue()
            buffer.close()

            # Return image as HTTP response
            response = HttpResponse(image_png, content_type="image/png")
            return response
    return HttpResponse(status=405)


def generate_simple_qr(request):
    url = request.GET.get('url', '')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_png = buffer.getvalue()
    buffer.close()
    response = HttpResponse(image_png, content_type="image/png")
    return response