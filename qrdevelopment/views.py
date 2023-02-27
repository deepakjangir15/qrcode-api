from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

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

        QR_data = request.POST.get('QR_data', '')
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

            wpercent = int(int(box_size) * 3.5)

            logo = image.resize((wpercent,wpercent), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)


            # adding QR_data or text to QRcode
            QRcode.add_data(QR_data)

            # generating QR code
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image(fill_color=QRcolor, back_color=BGcolor).convert('RGB')

            width, height = QRimg.size
            print( width, height)

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
        QR_data = request.POST.get('QR_data', '')
        base64_image = request.POST.get('base64_image','')
        QRcolor = request.POST.get('qrcolor', 'black')
        BGcolor = request.POST.get('bgcolor', 'White')
        box_size = request.POST.get('QR_size', 10)
        border_size = request.POST.get('spacing', 2)
        mask_me = request.POST.get('circular_logo', 1)
        force_download = request.POST.get('download_file',0)

        cache_key = 'qr_code_' + QR_data + '_' + QRcolor + '_' + BGcolor + '_' + str(box_size) + '_' + str(border_size) + '_' + str(mask_me)
        image_png = cache.get(cache_key)

        if image_png:
            # Return cached image as HTTP response
            response = HttpResponse(image_png, content_type="image/png")
            if force_download:
                response['Content-Disposition'] = 'attachment; filename=qr_code.png'
            return response

        if base64_image:
            # Load image
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

            wpercent = int(int(box_size) * 3.5)

            logo = image.resize((wpercent,wpercent), Image.ANTIALIAS)

            QRcode = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)

            # adding QR_data or text to QRcode
            QRcode.add_data(QR_data)

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

            # Add image to cache
            cache.set(cache_key, image_png, timeout=3600)


            # Return image as HTTP response
            response = HttpResponse(image_png, content_type="image/png")

            if force_download:
                response['Content-Disposition'] = 'attachment; filename=qr_code.png'

            return response
    return HttpResponse(status=405)

# 3. Generate simple QR code
@csrf_exempt
def generate_simple_qr(request):

    QR_data = request.GET.get('QR_data', '')
    box_size = request.GET.get('QR_size', 10)
    border_size = request.GET.get('spacing', 2)
    force_download = request.GET.get('download_file',0)

    cache_key = 'qr_code_' + QR_data + '_' + str(box_size) + '_' + str(border_size) + '_' + str(force_download)
    image_png = cache.get(cache_key)

    if image_png:
        print('Cache found : ', cache_key)
        response = HttpResponse(image_png, content_type="image/png")
        if force_download:
            response['Content-Disposition'] = 'attachment; filename=qr_code.png'
        return response
    
    else:
        # Generate a new QR Code and cache it
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)
        qr.add_data(QR_data)
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        image_png = buffer.getvalue()
        buffer.close()
        # Add image to cache
        cache.set(cache_key, image_png, timeout=3600)
        
        response = HttpResponse(image_png, content_type="image/png")
        if force_download:
            response['Content-Disposition'] = 'attachment; filename=qr_code.png'
        return response

@csrf_exempt
def generate_colored_qr(request):
    QR_data = request.GET.get('QR_data', '')
    box_size = request.GET.get('QR_size', 10)
    border_size = request.GET.get('spacing', 2)
    QRcolor = request.GET.get('qrcolor', 'black')
    BGcolor = request.GET.get('bgcolor', 'White')
    force_download = request.GET.get('download_file',0)

    cache_key = 'qr_code_' + QR_data + '_' + str(box_size) + '_' + str(border_size) + '_' + str(QRcolor) + '_' + str(BGcolor) 

    image_png = cache.get(cache_key)

    if image_png:
        response = HttpResponse(image_png, content_type="image/png")
        if force_download:
            response['Content-Disposition'] = 'attachment; filename=qr_code.png'
        return response
    
    else:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border = border_size)
        qr.add_data(QR_data)
        qr.make()
        img = qr.make_image(fill_color=QRcolor, back_color=BGcolor)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        image_png = buffer.getvalue()
        buffer.close()
        # Add image to cache
        cache.set(cache_key, image_png, timeout=3600)
        response = HttpResponse(image_png, content_type="image/png")
        return response