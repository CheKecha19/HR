import os
import sys
import getpass
from ldap3 import Server, Connection, ALL
import pandas as pd
from datetime import datetime

# Для правильного импорта config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AD_CONFIG, PATHS, AD_CREDS

def get_ad_credentials():
    """Получение учетных данных для AD"""
    # Приоритет 1: Переменные окружения
    env_user = os.getenv('AD_USER')
    env_password = os.getenv('AD_PASSWORD')
    
    if env_user and env_password:
        print("[AD] Использую учетные данные из переменных окружения")
        return env_user, env_password
    
    # Приоритет 2: Предустановленные в config
    if AD_CREDS['user'] and AD_CREDS['password']:
        print("[AD] Использую учетные данные из config.py")
        return AD_CREDS['user'], AD_CREDS['password']
    
    # Приоритет 3: Интерактивный ввод
    print("[AD] Требуются учетные данные для подключения к Active Directory")
    user = input("Введите AD username: ")
    password = getpass.getpass("Введите пароль: ")
    return user, password

def get_ad_users():
    """Получение данных о пользователях из Active Directory"""
    try:
        # Получаем учетные данные
        user, password = get_ad_credentials()
        
        print(f"[AD] Подключение к серверу {AD_CONFIG['server']}...")
        server = Server(AD_CONFIG['server'], get_info=ALL)
        conn = Connection(server, 
                         user=user, 
                         password=password, 
                         auto_bind=True)
        
        print(f"[AD] Поиск пользователей в {AD_CONFIG['search_base']}...")
        conn.search(
            search_base=AD_CONFIG['search_base'],
            search_filter='(&(objectClass=user)(objectCategory=person))',
            attributes=AD_CONFIG['attributes']
        )
        
        print(f"[AD] Найдено {len(conn.entries)} пользователей")
        
        # Преобразование результатов
        users = []
        for entry in conn.entries:
            user_data = {attr: entry[attr].value for attr in AD_CONFIG['attributes']}
            users.append(user_data)
        
        return pd.DataFrame(users)
    
    except Exception as e:
        print(f"[AD] Критическая ошибка подключения: {str(e)}")
        return pd.DataFrame()

def export_ad_report(ad_data):
    """Экспорт данных AD в Excel"""
    if ad_data.empty:
        print("[AD] Нет данных для экспорта")
        return None
    
    # Создание имени файла с датой
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ad_report_{date_str}.xlsx"
    output_path = os.path.join(PATHS['output_dir'], filename)
    
    # Экспорт в Excel
    try:
        with pd.ExcelWriter(output_path) as writer:
            ad_data.to_excel(writer, sheet_name='AD Data', index=False)
        print(f"[AD] Отчет сохранен: {output_path}")
        return output_path
    except Exception as e:
        print(f"[AD] Ошибка экспорта: {str(e)}")
        return None
