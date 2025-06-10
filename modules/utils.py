import pandas as pd
import os

def safe_export_excel(df, path, sheet_name):
    """Безопасный экспорт DataFrame в Excel"""
    try:
        # Проверка на пустые данные
        if df.empty:
            print(f"[Export] Предупреждение: Попытка экспорта пустого DataFrame в {path}")
            return False
        
        # Создание директории если нужно
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Экспорт
        with pd.ExcelWriter(path) as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return True
    except Exception as e:
        print(f"[Export] Ошибка экспорта: {str(e)}")
        return False
