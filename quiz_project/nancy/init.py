"""Пакет для системы тестирования (Quiz).

Этот пакет предоставляет функциональность для создания, 
загрузки и прохождения тестов через консольное приложение.

Модули:
    loader: Функции для загрузки и сохранения тестов
    engine: Основная логика тестирования
    results: Функции для отображения и сохранения результатов
    commands: Обработчики командной строки
    database: Модели и менеджер базы данных
    database_config: Конфигурация базы данных
"""

from .loader import load_tests, save_test, init_database
from .engine import QuizEngine
from .results import show_results, save_results, show_database_results
from .commands import setup_parser, handle_commands, create_test_interactive
from .database import DatabaseManager, Test, Question, TestResult
from .database_config import get_database_config

__all__ = [
    'load_tests', 'save_test', 'init_database',
    'QuizEngine', 
    'show_results', 'save_results', 'show_database_results',
    'setup_parser', 'handle_commands', 'create_test_interactive',
    'DatabaseManager', 'Test', 'Question', 'TestResult',
    'get_database_config'
]