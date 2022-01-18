from flask import Blueprint, render_template, Response
import json
import io
import random
from collections import namedtuple
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from math import *

result_route = Blueprint('result', __name__)
sys.path.append('static/uploads')


@result_route.route('/result/<filename>/<funcSC>/<znach_func>')
def result(filename, funcSC, znach_func):
# Рендер страницы с результатом
    return render_template('result.html',
                           title='Результат',
                           picture='uploads/'+filename,
                           funcSC=funcSC,
                           znach_func=znach_func
                           )


@result_route.route('/figure.png/<filedir>/<filename>/<funcSC>/<znach_func>')
def figure_png(filedir, filename, funcSC, znach_func):
#Создание изображения которое вызывется в момент загрузки страницы
    fig = create_figure(filedir, filename, funcSC, znach_func)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(filedir, filename, funcSC, znach_func):
#Функция получения изображения
    name_file = 'static/'+filedir+'/'+filename
    image = Image.open(name_file)
    image_old_in_array = np.asarray(image, dtype='uint8')
    #Умножение изображения на sin или cos
    array_znach_v_rad = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
    znach_func = int(znach_func)

    if(funcSC=="cos"):

        image_new_in_array = image_old_in_array * round(cos(array_znach_v_rad[znach_func]), 1)
        # RGB int приведение цветов к int
        image_new_in_array = image_new_in_array.astype(int)
        # Преобразование массива в изображение
        image_convert_new = Image.fromarray(np.uint8(image_new_in_array))
    elif(funcSC=="sin"):

        image_new_in_array = image_old_in_array * round(sin(array_znach_v_rad[znach_func]), 1)
        # RGB int приведение цветов к int
        image_new_in_array = image_new_in_array.astype(int)
        # Преобразование массива в изображение
        image_convert_new = Image.fromarray(np.uint8(image_new_in_array))
    #Вывод занчений в файл
    #np.savetxt('temp', image_new[1])
    #np.savetxt('temp_new', image_test[1])
    #print(image_test)
    #np.savetxt("array_1.csv", image_new[2], delimiter=",", fmt="%.3f")
    #np.savetxt("array_2.csv", image_test[2], delimiter=",", fmt="%.3f")

    Point = namedtuple('Point', ('coords', 'n', 'ct'))
    Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

    def get_points(img):
    #Получение пикселей изображения
        points = []
        w, h = img.size
        for count, color in img.getcolors(w * h):
            points.append(Point(color, 3, count))
        return points

    rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

    def colorz(filename, n=3):
    # Главаня функция в которой происходит обработка изображения
        img = filename
        img.thumbnail((200, 200))
        w, h = img.size

        points = get_points(img)
        clusters = kmeans(points, n, 1)
        rgbs = [map(int, c.center.coords) for c in clusters]
        return map(rtoh, rgbs)

    def euclidean(p1, p2):
    #Евклидово преобразование
        return sqrt(sum([
            (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
        ]))

    def calculate_center(points, n):
    #Определение центра изображения
        vals = [0.0 for i in range(n)]
        plen = 0
        for p in points:
            plen += p.ct
            for i in range(n):
                vals[i] += (p.coords[i] * p.ct)
        return Point([(v / plen) for v in vals], n, 1)

    def kmeans(points, k, min_diff):
    #Усреднение
        if len(points) < 3:
            k = 1

        clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

        while 1:
            plists = [[] for i in range(k)]

            for p in points:
                smallest_distance = float('Inf')
                for i in range(k):
                    distance = euclidean(p, clusters[i].center)
                    if distance < smallest_distance:
                        smallest_distance = distance
                        idx = i
                plists[idx].append(p)

            diff = 0
            for i in range(k):
                old = clusters[i]
                center = calculate_center(plists[i], old.n)
                new = Cluster(plists[i], center, old.n)
                clusters[i] = new
                diff = max(diff, euclidean(old.center, new.center))

            if diff < min_diff:
                break

        return clusters

    # задаем пространство для размещения графиков
    fig_ = plt.figure(figsize=(9, 7))
    # отображаем исходный файл
    viewer_1 = fig_.add_subplot(2, 2, 1)
    # отображаем измененный файл
    viewer_2 = fig_.add_subplot(2, 2, 2)
    # отображаем график распределения исходного файла
    viewer_3 = fig_.add_subplot(2, 2, 3)
    # отображаем график распределения изменного файл
    viewer_4 = fig_.add_subplot(2, 2, 4)

    # Оформление изображений
    viewer_1.imshow(image_old_in_array)
    viewer_1.axis('off')
    viewer_1.set_title('Исходное изображение')
    viewer_2.imshow(image_new_in_array)

    # Оформление изображений
    viewer_2.axis('off')
    viewer_2.set_title('Измененное изображение')

    # Оформление изображений
    color_old_img = list(colorz(image))
    count_color_old_img = [1, 1, 1]
    viewer_3.bar(color_old_img, count_color_old_img, color=color_old_img)
    viewer_3.axes.yaxis.set_visible(False)
    viewer_3.set_title('Распределение цветов в исходном изображении')
    color_new_img = list(colorz(image_convert_new))
    
    # Оформление изображений
    viewer_4.bar(color_new_img, count_color_old_img, color=color_new_img)
    viewer_4.axes.yaxis.set_visible(False)
    viewer_4.set_title('Распределение цветов в новом изображении')
    fig_.subplots_adjust(wspace=1.0,
                         hspace=0)
    return fig_