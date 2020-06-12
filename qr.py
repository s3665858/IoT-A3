import qrcode
def generateQR(id,name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = {'id': id,'name':name,'type':5}
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('1.jpg')

generateQR(0,"rock")
from pyzbar.pyzbar import decode
from PIL import Image
import ast
data = ast.literal_eval(decode(Image.open('1.jpg'))[0].data.decode('UTF-8')) 

print(data)