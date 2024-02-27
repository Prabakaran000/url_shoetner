# views.py
import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import ShortenedURL
import random
import string

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for i in range(6))
    return short_code

def generate_qr_code(shortened_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(shortened_url)
    qr.make(fit=True)

    qr_code = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    qr_code.save(buffered)
    qr_code_img_str = base64.b64encode(buffered.getvalue()).decode()

    return qr_code_img_str

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if not original_url:
            return render(request, 'shorten_url.html', {'error': 'Please provide a URL.'})

        existing_url = ShortenedURL.objects.filter(original_url=original_url).first()
        if existing_url:
            qr_code = generate_qr_code(request.build_absolute_uri('/' + existing_url.short_code + '/'))
            return render(request, 'shorten_url.html', {'shortened_url': existing_url.short_code, 'qr_code': qr_code})

        short_code = generate_short_code()
        shortened_url = ShortenedURL.objects.create(original_url=original_url, short_code=short_code)

        qr_code = generate_qr_code(request.build_absolute_uri('/' + shortened_url.short_code + '/'))

        return render(request, 'shorten_url.html', {'shortened_url': shortened_url.short_code, 'qr_code': qr_code})
    return render(request, 'shorten_url.html')

def redirect_original(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    return redirect(shortened_url.original_url)
