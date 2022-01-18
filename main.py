from flask import Flask
from router.index import index_route
from router.result import result_route
from router.upload import upload_route

app = Flask(__name__)
#регистарция роутов
app.register_blueprint(index_route)
app.register_blueprint(result_route)
app.register_blueprint(upload_route)

#Запуск прилодения
if __name__ == "__main__":
    app.run(host='0.0.0.0')

