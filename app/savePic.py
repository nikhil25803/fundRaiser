import qrcode    
import os

from raiser.settings import MEDIA_ROOT, MEDIA_URL
def saveImg(string, name):
    img = qrcode.make(string)
    img.save(MEDIA_ROOT +f'/{name}.png')