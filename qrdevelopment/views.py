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


def mask_images(logo):
    # Create circular mask for image
    mask = Image.new("L", logo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)

    # Apply mask to image
    logo.putalpha(mask)

    return logo

# 1. Uses File Image in Post request
@csrf_exempt
def generate_qr_with_image_file(request):
    basewidth = 40

    if request.method == 'POST':

        qr_data = request.POST.get('qr_data', '')
        image_data = request.FILES.get('image', '')
        QRcolor = request.POST.get('qrcolor', 'black')
        BGcolor = request.POST.get('bgcolor', 'White')
        box_size = request.POST.get('QR_size', 10)
        border_size = request.POST.get('spacing', 2)
        mask_me = request.POST.get('circular_logo', 1)
        force_download = request.POST.get('download_file',0)


        if image_data:
            # Load image
            image = Image.open(image_data)

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            logo = image.resize((basewidth, hsize), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)


            # adding qr_data or text to QRcode
            QRcode.add_data(qr_data)

            # generating QR code
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image(fill_color=QRcolor, back_color=BGcolor).convert('RGB')

            logo = mask_images(logo)

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos,mask=logo if int(mask_me) else None)


            # Save image data to buffer
            buffer = BytesIO()
            QRimg.save(buffer, format='PNG')
            image_png = buffer.getvalue()
            buffer.close()

            # Return image as HTTP response with Content-Disposition header set to force download
            response = HttpResponse(image_png, content_type="image/png")

            if force_download:
                response['Content-Disposition'] = 'attachment; filename=qr_code.png'

            return response
        
    return HttpResponse(status=405)

# 2. Uses base64 as the input in post request
@csrf_exempt
def generate_qr_with_image(request):
    basewidth = 40

    if request.method == 'POST':
        qr_data = request.POST.get('qr_data', '')
        base64_image = request.POST.get('base64_image','')
        QRcolor = request.POST.get('qrcolor', 'black')
        BGcolor = request.POST.get('bgcolor', 'White')
        box_size = request.POST.get('QR_size', 10)
        border_size = request.POST.get('spacing', 2)
        mask_me = request.POST.get('circular_logo', 1)
        force_download = request.POST.get('download_file',0)

        if base64_image:
            # Load image
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            logo = image.resize((basewidth, hsize), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)

            # adding qr_data or text to QRcode
            QRcode.add_data(qr_data)

            # generating QR code
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image(fill_color=QRcolor, back_color=BGcolor).convert('RGB')

            logo = mask_images(logo)

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos,mask=logo if int(mask_me) else None)


            # Save image data to buffer
            buffer = BytesIO()
            QRimg.save(buffer, format='PNG')
            image_png = buffer.getvalue()
            buffer.close()

            # Return image as HTTP response
            response = HttpResponse(image_png, content_type="image/png")

            if force_download:
                response['Content-Disposition'] = 'attachment; filename=qr_code.png'

            return response
    return HttpResponse(status=405)


def generate_simple_qr(request):
    qr_data = request.GET.get('qr_data', '')
    box_size = request.GET.get('QR_size', 10)
    border_size = request.GET.get('spacing', 2)
    force_download = request.POST.get('download_file',0)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)
    qr.add_data(qr_data)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_png = buffer.getvalue()
    buffer.close()
    response = HttpResponse(image_png, content_type="image/png")
    if force_download:
        response['Content-Disposition'] = 'attachment; filename=qr_code.png'
    return response


def generate_colored_qr(request):
    qr_data = request.GET.get('qr_data', '')
    box_size = request.GET.get('QR_size', 10)
    border_size = request.GET.get('spacing', 2)
    QRcolor = request.POST.get('qrcolor', 'black')
    BGcolor = request.POST.get('bgcolor', 'White')

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)
    qr.add_data(qr_data)
    qr.make()
    img = qr.make_image(fill_color=QRcolor, back_color=BGcolor)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_png = buffer.getvalue()
    buffer.close()
    response = HttpResponse(image_png, content_type="image/png")
    return response