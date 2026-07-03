import io
import qrcode
from django.core.files.base import ContentFile


def generate_qr(product_id):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(str(product_id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e3a5f", back_color="white")
    with io.BytesIO() as buf:
        img.save(buf, format="PNG")
        return ContentFile(buf.getvalue(), name=f"product_{product_id}.png")
