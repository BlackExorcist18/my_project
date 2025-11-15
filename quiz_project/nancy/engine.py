import random
from typing import List, Dict, Any, Tuple

class QuizEngine:
    def __init__(self, tests: List[Dict[str, Any]]):
        self.tests = tests
        self.current_test = None
        self.current_questions = []
        self.score = 0
        self.total_questions = 0
        self.current_question_index = 0
    
    def list_tests(self) -> List[str]:
        """Получить список доступных тестов"""
        return [test['name'] for test in self.tests]
    
    def select_test(self, test_name: str) -> bool:
        """Выбор теста по имени"""
        for test in self.tests:
            if test['name'] == test_name:
                self.current_test = test
                self.current_questions = test['questions'].copy()
                return True
        return False
    
    def shuffle_questions(self, count: int = None) -> None:
        """Перемешать вопросы и выбрать указанное количество"""
        random.shuffle(self.current_questions)
        if count and count < len(self.current_questions):
            self.current_questions = self.current_questions[:count]
    
    def start_quiz(self, shuffle: bool = True, question_count: int = None) -> None:
        """Начать тестирование"""
        if not self.current_test:
            raise ValueError("Тест не выбран")
        
        if shuffle:
            self.shuffle_questions(question_count)
        elif question_count:
            self.current_questions = self.current_questions[:question_count]
        
        self.score = 0
        self.total_questions = len(self.current_questions)
        self.current_question_index = 0
        
        print(f"\nНачинаем тест: {self.current_test['name']}")
        print(f"Количество вопросов: {self.total_questions}")
        print("=" * 50)
    
    def get_next_question(self) -> Tuple[str, List[str], int] or None:
        """Получить следующий вопрос"""
        if self.current_question_index >= len(self.current_questions):
            return None
        
        question_data = self.current_questions[self.current_question_index]
        question = question_data['question']
        options = question_data['options']
        correct_answer = question_data['correct_answer']
        
        self.current_question_index += 1
        return question, options, correct_answer
    
    def check_answer(self, user_answer: int, correct_answer: int) -> bool:
        """Проверить ответ пользователя"""
        is_correct = user_answer == correct_answer
        if is_correct:
            self.score += 1
        return is_correct
    
    def get_progress(self) -> Tuple[int, int]:
        """Получить текущий прогресс"""
        return self.current_question_index, self.total_questions
    
    def get_results(self) -> Dict[str, Any]:
        """Получить результаты тестирования"""
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        return {
            'test_name': self.current_test['name'],
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': percentage,
            'passed': percentage >= 70  # 70% для прохождения
        }