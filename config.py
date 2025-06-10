import os

# Базовые настройки
AD_CONFIG = {
    'server': os.getenv('AD_SERVER', 'ad-server.example.com'),
    'search_base': os.getenv('AD_SEARCH_BASE', 'dc=example,dc=com'),
    'attributes': ['sAMAccountName', 'givenName', 'sn', 'mail', 'department']
}

# Пути
PATHS = {
    'output_dir': r'{HARDCODE}\results'
}

# Для интерактивного ввода
AD_CREDS = {
    'user': None,
    'password': None
}
