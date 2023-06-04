import cv2
import numpy as np
import urllib.request
import win32clipboard
from PIL import Image
from io import BytesIO


def copy_image_to_clipboard(img_bgr):
    output = BytesIO()
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)
    img_pil.save(output, format='BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def get_img_for_url(img_url):
    with urllib.request.urlopen(img_url) as response:
        image_data = response.read()

    image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return img
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


