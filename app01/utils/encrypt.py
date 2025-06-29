from django.conf import settings
import hashlib


# 加盐md5加密
def md5(data_string):
    salt = "xjz"
    # 可以调用setting.py中django提供的SECRET_KEY作为”盐“
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
