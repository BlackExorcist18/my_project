"""Модуль обработки командной строки.

Содержит функции для настройки парсера аргументов и обработки 
пользовательских команд.
"""

import argparse
import json
from typing import List
from .loader import load_tests, save_test
from .engine import QuizEngine
from .results import show_results, save_results


def create_test_interactive() -> dict:
    """Интерактивно создает новый тест через ввод пользователя.
    
    Returns:
        dict: Словарь с данными нового теста.
    """
    print("\nСоздание нового теста")
    print("=" * 30)
    
    test_name = input("Название теста: ")
    test_description = input("Описание теста: ")
    
    questions = []
    
    while True:
        print(f"\nВопрос #{len(questions) + 1}")
        question_text = input("Текст вопроса: ")
        
        if not question_text:
            break
        
        options = []
        for i in range(4):
            option = input(f"Вариант ответа {i + 1}: ")
            if option:
                options.append(option)
        
        if len(options) < 2:
            print("Нужно как минимум 2 варианта ответа!")
            continue
        
        try:
            correct = int(input(f"Номер правильного ответа (1-{len(options)}): ")) - 1
            if correct < 0 or correct >= len(options):
                print("Неверный номер правильного ответа!")
                continue
        except ValueError:
            print("Введите число!")
            continue
        
        questions.append({
            'question': question_text,
            'options': options,
            'correct_answer': correct
        })
        
        add_more = input("Добавить еще вопрос? (y/n): ").lower()
        if add_more != 'y':
            break
    
    return {
        'name': test_name,
        'description': test_description,
        'questions': questions
    }


def handle_commands(args) -> None:
    """Обрабатывает команды пользователя из командной строки.
    
    Args:
        args: Аргументы командной строки, полученные от argparse.
    """
    tests = load_tests()
    quiz = QuizEngine(tests)
    
    # Исправляем проверку атрибутов
    if hasattr(args, 'command'):
        if args.command == 'list':
            print("\nДоступные тесты:")
            for i, test_name in enumerate(quiz.list_tests(), 1):
                print(f"{i}. {test_name}")
        
        elif args.command == 'create':
            new_test = create_test_interactive()
            if new_test['questions']:
                if save_test(new_test):
                    print(f"Тест '{new_test['name']}' успешно создан!")
                else:
                    print("Ошибка при сохранении теста")
            else:
                print("Тест не создан - нет вопросов")
        
        elif args.command == 'run':
            if not quiz.list_tests():
                print("Нет доступных тестов!")
                return
            
            test_name = args.run_test
            if not quiz.select_test(test_name):
                print(f"Тест '{test_name}' не найден!")
                print("Доступные тесты:", ", ".join(quiz.list_tests()))
                return
            
            # Начинаем тестирование
            quiz.start_quiz(shuffle=not args.no_shuffle, question_count=args.questions)
            
            # Проходим все вопросы
            while True:
                question_data = quiz.get_next_question()
                if not question_data:
                    break
                
                question, options, correct_answer = question_data
                current, total = quiz.get_progress()
                
                print(f"\nВопрос {current}/{total}: {question}")
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                
                while True:
                    try:
                        user_choice = int(input("\nВаш ответ (1-4): ")) - 1
                        if 0 <= user_choice < len(options):
                            break
                        else:
                            print("Пожалуйста, введите число от 1 до", len(options))
                    except ValueError:
                        print("Пожалуйста, введите число")
                
                is_correct = quiz.check_answer(user_choice, correct_answer)
                if is_correct:
                    print("✅ Правильно!")
                else:
                    print(f"❌ Неправильно! Правильный ответ: {options[correct_answer]}")
            
            # Показываем результаты
            results = quiz.get_results()
            show_results(results)
            
            if args.save_results:
                save_results(results, args.save_results)
        
        elif args.command == 'results':
            try:
                results_file = args.file if hasattr(args, 'file') else 'results.json'
                with open(results_file, 'r', encoding='utf-8') as file:
                    all_results = json.load(file)
                
                print(f"\nИстория результатов ({results_file}):")
                print("=" * 50)
                for result in all_results[-10:]:
                    print(f"Тест: {result['test_name']}")
                    print(f"Результат: {result['score']}/{result['total_questions']} ({result['percentage']:.1f}%)")
                    print(f"Время: {result['timestamp'][:19]}")
                    print("-" * 30)
                    
            except FileNotFoundError:
                print(f"Файл {results_file} не найден")
            except Exception as e:
                print(f"Ошибка при загрузке результатов: {e}")


def setup_parser() -> argparse.ArgumentParser:
    """Настраивает парсер аргументов командной строки.
    
    Returns:
        argparse.ArgumentParser: Настроенный парсер аргументов.
    """
    parser = argparse.ArgumentParser(description='Система тестирования (Quiz)')
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды', title='команды')
    
    # Команда list
    list_parser = subparsers.add_parser('list', help='Показать список тестов')
    
    # Команда create
    create_parser = subparsers.add_parser('create', help='Создать новый тест')
    
    # Команда run
    run_parser = subparsers.add_parser('run', help='Запустить тест')
    run_parser.add_argument('run_test', help='Название теста для запуска')
    run_parser.add_argument('--questions', '-q', type=int, help='Количество вопросов')
    run_parser.add_argument('--no-shuffle', action='store_true', help='Не перемешивать вопросы')
    run_parser.add_argument('--save-results', help='Файл для сохранения результатов')
    
    # Команда results
    results_parser = subparsers.add_parser('results', help='Показать историю результатов')
    results_parser.add_argument('--file', default='results.json', help='Файл с результатами')
    
    return parser