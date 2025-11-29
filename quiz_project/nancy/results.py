"""Модуль для работы с результатами тестирования."""

import json
from typing import Dict, Any
import datetime
from .database import db_manager

def show_results(results: Dict[str, Any]) -> None:
    """Отображает результаты тестирования в консоли.
    
    Args:
        results (Dict[str, Any]): Словарь с результатами теста.
    """
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    print(f"Тест: {results['test_name']}")
    print(f"Правильных ответов: {results['score']} из {results['total_questions']}")
    print(f"Процент правильных ответов: {results['percentage']:.1f}%")
    
    if results['passed']:
        print("✅ ТЕСТ ПРОЙДЕН!")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
    print("=" * 50)

def save_results(results: Dict[str, Any], filename: str = "results.json", use_database: bool = False) -> bool:
    """Сохраняет результаты тестирования.
    
    Args:
        results (Dict[str, Any]): Словарь с результатами теста.
        filename (str): Имя файла для сохранения.
        use_database (bool): Использовать базу данных вместо файла.
        
    Returns:
        bool: True если сохранение успешно, False в случае ошибки.
    """
    if use_database and db_manager:
        return db_manager.save_test_result(results)
    else:
        return save_results_to_file(results, filename)

def save_results_to_file(results: Dict[str, Any], filename: str = "results.json") -> bool:
    """Сохраняет результаты тестирования в JSON файл.
    
    Args:
        results (Dict[str, Any]): Словарь с результатами теста.
        filename (str): Имя файла для сохранения.
        
    Returns:
        bool: True если сохранение успешно, False в случае ошибки.
    """
    try:
        # Загружаем существующие результаты
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                all_results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_results = []
        
        # Добавляем timestamp
        results_with_time = results.copy()
        results_with_time['timestamp'] = datetime.datetime.now().isoformat()
        
        all_results.append(results_with_time)
        
        # Сохраняем обратно
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(all_results, file, ensure_ascii=False, indent=2)
        
        print(f"Результаты сохранены в {filename}")
        return True
        
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")
        return False

def show_database_results(test_name: str = None, limit: int = 10) -> None:
    """Показывает результаты из базы данных.
    
    Args:
        test_name (str): Фильтр по названию теста.
        limit (int): Максимальное количество результатов.
    """
    if not db_manager:
        print("База данных не инициализирована")
        return
    
    results = db_manager.get_test_results(test_name, limit)
    
    print(f"\nИстория результатов (база данных):")
    print("=" * 60)
    for result in results:
        status = "✅ ПРОЙДЕН" if result['passed'] else "❌ НЕ ПРОЙДЕН"
        print(f"Тест: {result['test_name']}")
        print(f"Пользователь: {result['user_name']}")
        print(f"Результат: {result['score']}/{result['total_questions']} ({result['percentage']}%) - {status}")
        print(f"Время: {result['completed_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)