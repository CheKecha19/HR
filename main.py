import os
import argparse
from modules import ad
from config import PATHS, AD_CREDS

def main():
    print("="*50)
    print("Проверка данных сотрудников")
    print("="*50)
    
    # Обработка аргументов командной строки
    parser = argparse.ArgumentParser(description='Скрипт проверки данных сотрудников')
    parser.add_argument('--user', help='AD username')
    parser.add_argument('--password', help='AD password (не рекомендуется передавать напрямую)')
    args = parser.parse_args()
    
    # Передача учетных данных если указаны
    if args.user:
        AD_CREDS['user'] = args.user
    if args.password:
        AD_CREDS['password'] = args.password
    
    # Создание директории для отчетов
    if not os.path.exists(PATHS['output_dir']):
        os.makedirs(PATHS['output_dir'])
        print(f"Создана директория: {PATHS['output_dir']}")
    
    # Шаг 1: Получение данных из AD
    print("\n[Этап 1] Получение данных из Active Directory")
    ad_users = ad.get_ad_users()
    
    if not ad_users.empty:
        # Шаг 2: Экспорт данных AD в Excel
        print("\n[Этап 2] Экспорт данных AD")
        report_path = ad.export_ad_report(ad_users)
        
        if report_path:
            print(f"\n✓ Отчет AD создан: {report_path}")
            print(f"✓ Записей экспортировано: {len(ad_users)}")
        else:
            print("\n✗ Не удалось создать отчет AD")
    else:
        print("\n✗ Прерывание: Нет данных из AD")

if __name__ == "__main__":
    main()
