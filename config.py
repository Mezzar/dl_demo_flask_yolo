import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '325lGjHHR23jhg5j235j235uhkdg9435'

    MAX_CONTENT_LENGTH = 15 * 1024 * 1024  # максимум для загружаемых файлов

    IMG_DOWNSIZE_TO = (2000, 1700)

    IMG_UPLOAD_FOLDER = 'data/img_in'
    IMG_OUTPUT_FOLDER = 'data/img_out'

    ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'bmp', 'gif', 'tif')

    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = True
    
    MAX_CAROUSEL_IMAGES = 7