"""Модуль для глобальной сессии базы данных."""

# Глобальный менеджер БД
db_manager = None

def get_db_manager():
    """Получить глобальный менеджер базы данных."""
    if db_manager is None:
        raise RuntimeError("База данных не инициализирована. Вызовите init_database() сначала.")
    return db_manager

def set_db_manager(manager):
    """Установить глобальный менеджер базы данных."""
    global db_manager
    db_manager = manager