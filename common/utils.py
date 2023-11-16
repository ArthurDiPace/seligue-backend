import base64
from collections import namedtuple
from io import BytesIO

import qrcode
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from weasyprint import HTML


def render_pdf(template_path, base_url, context):
    try:
        pdf_in_memory = BytesIO()
        html_string = render_to_string(template_path, context)
        html = HTML(string=html_string, base_url=base_url)
        html.write_pdf(target=pdf_in_memory)
        return HttpResponse(pdf_in_memory.getvalue(), content_type="application/pdf")
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


def generate_qr_code(url):
    try:
        qr = BytesIO()
        img = qrcode.make(url)
        img.save(qr)
        image_stream = qr.getvalue()
        qr_b64 = base64.b64encode(image_stream)
        return qr_b64.decode("utf-8")
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
