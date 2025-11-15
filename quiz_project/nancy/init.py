"""Пакет для системы тестирования (Quiz).

Этот пакет предоставляет функциональность для создания, 
загрузки и прохождения тестов через консольное приложение.

Модули:
    loader: Функции для загрузки и сохранения тестов
    engine: Основная логика тестирования
    results: Функции для отображения и сохранения результатов
    commands: Обработчики командной строки
"""

from .loader import load_tests, save_test
from .engine import QuizEngine
from .results import show_results, save_results
from .commands import setup_parser, handle_commands

__all__ = ['load_tests', 'save_test', 'QuizEngine', 'show_results', 
           'save_results', 'setup_parser', 'handle_commands']