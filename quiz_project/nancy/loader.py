"""Модуль для загрузки и сохранения тестов из/в JSON файлов.

Предоставляет функции для работы с файловой системой при 
хранении данных тестов и результатов.
"""

import json
import os
from typing import List, Dict, Any


def load_tests(filename: str = "tests.json") -> List[Dict[str, Any]]:
    """Загружает тесты из JSON файла.

    Args:
        filename (str): Имя файла для загрузки. По умолчанию "tests.json".

    Returns:
        List[Dict[str, Any]]: Список тестов, каждый тест представлен словарем.

    Raises:
        JSONDecodeError: Если файл содержит некорректный JSON.
        Exception: При других ошибках чтения файла.
    """
    try:
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден. Создан пустой файл.")
            save_tests([], filename)
            return []
        
        with open(filename, 'r', encoding='utf-8') as file:
            tests = json.load(file)
            print(f"Загружено {len(tests)} тестов")
            return tests
            
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filename} содержит некорректный JSON")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке тестов: {e}")
        return []


def save_tests(tests: List[Dict[str, Any]], filename: str = "tests.json") -> bool:
    """Сохраняет список тестов в JSON файл.

    Args:
        tests (List[Dict[str, Any]]): Список тестов для сохранения.
        filename (str): Имя файла для сохранения. По умолчанию "tests.json".

    Returns:
        bool: True если сохранение успешно, False в случае ошибки.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tests, file, ensure_ascii=False, indent=2)
        print(f"Тесты сохранены в {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении тестов: {e}")
        return False


def save_test(test_data: Dict[str, Any], filename: str = "tests.json") -> bool:
    """Добавляет новый тест в файл с тестами.

    Args:
        test_data (Dict[str, Any]): Данные нового теста.
        filename (str): Имя файла для сохранения. По умолчанию "tests.json".

    Returns:
        bool: True если сохранение успешно, False в случае ошибки.
    """
    try:
        tests = load_tests(filename)
        tests.append(test_data)
        return save_tests(tests, filename)
    except Exception as e:
        print(f"Ошибка при добавлении теста: {e}")
        return False