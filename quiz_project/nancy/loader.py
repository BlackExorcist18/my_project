"""Модуль для загрузки и сохранения тестов из/в JSON файлов и базы данных."""

import json
import os
from typing import List, Dict, Any
from .database import DatabaseManager

# Глобальный менеджер БД
db_manager = None

def init_database(database_url: str = None) -> DatabaseManager:
    """Инициализация базы данных.
    
    Args:
        database_url: URL подключения к PostgreSQL.
        
    Returns:
        DatabaseManager: Менеджер базы данных.
    """
    global db_manager
    db_manager = DatabaseManager(database_url)
    db_manager.init_db()
    return db_manager

def load_tests(filename: str = "tests.json", use_database: bool = False) -> List[Dict[str, Any]]:
    """Загружает тесты из JSON файла или базы данных.
    
    Args:
        filename (str): Имя файла для загрузки. По умолчанию "tests.json".
        use_database (bool): Использовать базу данных вместо файла.
        
    Returns:
        List[Dict[str, Any]]: Список тестов.
    """
    if use_database and db_manager:
        tests_data = db_manager.get_all_tests()
        # Преобразуем в формат совместимый с текущей системой
        tests = []
        for test_data in tests_data:
            test = db_manager.get_test_by_name(test_data['name'])
            if test:
                tests.append(test)
        return tests
    else:
        # Старая логика загрузки из файла
        return load_tests_from_file(filename)

def load_tests_from_file(filename: str = "tests.json") -> List[Dict[str, Any]]:
    """Загружает тесты из JSON файла.
    
    Args:
        filename (str): Имя файла для загрузки.
        
    Returns:
        List[Dict[str, Any]]: Список тестов.
    """
    try:
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден. Создан пустой файл.")
            save_tests_to_file([], filename)
            return []
        
        with open(filename, 'r', encoding='utf-8') as file:
            tests = json.load(file)
            print(f"Загружено {len(tests)} тестов из файла")
            return tests
            
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filename} содержит некорректный JSON")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке тестов: {e}")
        return []

def save_test(test_data: Dict[str, Any], filename: str = "tests.json", use_database: bool = False) -> bool:
    """Сохраняет тест в файл или базу данных.
    
    Args:
        test_data (Dict[str, Any]): Данные теста.
        filename (str): Имя файла для сохранения.
        use_database (bool): Использовать базу данных вместо файла.
        
    Returns:
        bool: True если успешно, False в случае ошибки.
    """
    if use_database and db_manager:
        return db_manager.add_test(test_data)
    else:
        return save_test_to_file(test_data, filename)

def save_test_to_file(test_data: Dict[str, Any], filename: str = "tests.json") -> bool:
    """Сохраняет тест в JSON файл.
    
    Args:
        test_data (Dict[str, Any]): Данные теста.
        filename (str): Имя файла для сохранения.
        
    Returns:
        bool: True если успешно, False в случае ошибки.
    """
    try:
        tests = load_tests_from_file(filename)
        tests.append(test_data)
        return save_tests_to_file(tests, filename)
    except Exception as e:
        print(f"Ошибка при добавлении теста: {e}")
        return False

def save_tests_to_file(tests: List[Dict[str, Any]], filename: str = "tests.json") -> bool:
    """Сохраняет список тестов в JSON файл.
    
    Args:
        tests (List[Dict[str, Any]]): Список тестов.
        filename (str): Имя файла для сохранения.
        
    Returns:
        bool: True если успешно, False в случае ошибки.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tests, file, ensure_ascii=False, indent=2)
        print(f"Тесты сохранены в {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении тестов: {e}")
        return False