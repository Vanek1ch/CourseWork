import webview

class Api:
    def server_function(self):
        print("Сервер запустился*")
        return "Сервер запустился*"

    def orders_function(self):
        print("Обработка заказов выполнена*")
        return "Обработка заказов выполнена*"

    def export_function(self):
        print("Экспорт функций завершен*")
        return "Экспорт функций завершен*"

api = Api()

window = webview.create_window(
    'Система управления заказами',
    url="web_folder/main.html", 
    width=800,
    height=600,
    resizable=False,
    js_api=api
)
