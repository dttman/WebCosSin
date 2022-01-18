from flask import Blueprint, render_template
index_route = Blueprint('index', __name__)

#Роут главной страницы
@index_route.route('/')
def index():
#Рендер главной страницы
    return render_template('index.html',
                           title='Главная')