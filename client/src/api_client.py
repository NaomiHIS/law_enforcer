import requests
from PyQt5.QtCore import QObject, pyqtSignal

class APIClient(QObject):
    error_occurred = pyqtSignal(str)
    
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        """Установка токена авторизации"""
        self.token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get_servers(self):
        """Получение списка серверов"""
        try:
            response = self.session.get(f"{self.base_url}/api/servers")
            if response.status_code == 200:
                return response.json()
            else:
                self.error_occurred.emit(f"Ошибка {response.status_code}: {response.text}")
        except Exception as e:
            self.error_occurred.emit(f"Сетевая ошибка: {str(e)}")
        return []

    def get_laws(self, server_id):
        """Получение законов для сервера"""
        try:
            response = self.session.get(f"{self.base_url}/api/laws/{server_id}")
            if response.status_code == 200:
                return response.json()
            else:
                self.error_occurred.emit(f"Ошибка {response.status_code}: {response.text}")
        except Exception as e:
            self.error_occurred.emit(f"Сетевая ошибка: {str(e)}")
        return []

    # Добавьте другие методы API по аналогии