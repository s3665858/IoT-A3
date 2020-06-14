.. _qr:

QR Object Detection
===================
*Directory: /qr.py*

This module utilizes the qrcode Python package for QR code generation

generateQR(id, name)
--------------
This function is used to generated the QR Code with parameters to specify the size and border
as well as error correction.

The QR is saved as a JPG file using qr.make_image() which contains the id and name of engineer and then
decoded to read the QR data.
