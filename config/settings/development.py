from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", '13.233.99.194']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
