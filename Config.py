import os

#Класс для хранения переменных куда сохранять картинки и какой формат поддерживается
class Config:
    UPLOAD_FOLDER = os.getcwd()+'/static/uploads'
    FOLDER = os.getcwd()
    ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg'])