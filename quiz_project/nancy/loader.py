import json
import os
from typing import List, Dict, Any

def load_tests(filename: str = "tests.json") -> List[Dict[str, Any]]:
    """
    Загрузка тестов из JSON файла
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
    """
    Сохранение тестов в JSON файл
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
    """
    Добавление нового теста в файл
    """
    try:
        tests = load_tests(filename)
        tests.append(test_data)
        return save_tests(tests, filename)
    except Exception as e:
        print(f"Ошибка при добавлении теста: {e}")
        return False