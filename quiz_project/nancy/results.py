"""Модуль для работы с результатами тестирования.

Предоставляет функции для отображения и сохранения результатов 
тестирования в файлы.
"""

import json
from typing import Dict, Any
import datetime


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


def save_results(results: Dict[str, Any], filename: str = "results.json") -> bool:
    """Сохраняет результаты тестирования в JSON файл.
    
    Args:
        results (Dict[str, Any]): Словарь с результатами теста.
        filename (str): Имя файла для сохранения. По умолчанию "results.json".
        
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