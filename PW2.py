# Практическая работа 2 - Полная версия
# Декораторы в Python

# ===== 1. ДЕКОРАТОР ЛОГИРОВАНИЯ =====

def logger(func):
    def wrapper(*args, **kwargs):
        # Перед вызовом функции
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        
        # Выполнение функции
        result = func(*args, **kwargs)
        
        # После выполнения функции
        print(f"Функция {func.__name__} вернула {result}")
        
        return result
    return wrapper

# Функции с декоратором логирования
@logger
def add(a, b):
    """Возвращает сумму двух чисел"""
    return a + b

@logger
def divide(a, b):
    """Возвращает результат деления"""
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b

@logger
def greet(name):
    """Выводит приветствие"""
    return f"Привет, {name}!"

# ===== 2. ДЕКОРАТОР ДОСТУПА =====

def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.get('role') in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"Доступ запрещён пользователю {user['name']}")
                return None
        return wrapper
    return decorator

# Функции с декоратором доступа
@require_role(['admin'])
def delete_database(user):
    print(f"База данных удалена пользователем {user['name']}")

@require_role(['admin', 'manager'])
def edit_settings(user):
    print(f"Настройки изменены пользователем {user['name']}")

@require_role(['user', 'admin', 'manager'])
def view_data(user):
    print(f"Данные просмотрены пользователем {user['name']}")

# ===== ТЕСТИРОВАНИЕ =====

def main():
    print("=" * 50)
    print("ПРАКТИЧЕСКАЯ РАБОТА 2 - ДЕКОРАТОРЫ")
    print("=" * 50)
    
    # Тестирование декоратора логирования
    print("\n1. ТЕСТИРОВАНИЕ ДЕКОРАТОРА ЛОГИРОВАНИЯ")
    print("-" * 40)
    
    print("Функция add(5, 3):")
    add(5, 3)
    
    print("\nФункция divide(10, 2):")
    divide(10, 2)
    
    print("\nФункция divide(10, 0):")
    divide(10, 0)
    
    print("\nФункция greet('Анна'):")
    greet("Анна")
    
    # Тестирование декоратора доступа
    print("\n2. ТЕСТИРОВАНИЕ ДЕКОРАТОРА ДОСТУПА")
    print("-" * 40)
    
    # Создание пользователей с разными ролями
    users = [
        {'name': 'Иван', 'role': 'admin'},
        {'name': 'Мария', 'role': 'manager'},
        {'name': 'Петр', 'role': 'user'},
        {'name': 'Анна', 'role': 'guest'}
    ]
    
    for user in users:
        print(f"\nПользователь: {user['name']} (роль: {user['role']})")
        print("Действия:")
        delete_database(user)
        edit_settings(user)
        view_data(user)
    
    # Демонстрация комбинирования декораторов
    print("\n3. КОМБИНИРОВАНИЕ ДЕКОРАТОРОВ")
    print("-" * 40)
    
    @logger
    @require_role(['admin'])
    def secure_operation(user):
        print(f"Безопасная операция выполнена пользователем {user['name']}")
        return "Успешно"
    
    admin_user = {'name': 'Администратор', 'role': 'admin'}
    regular_user = {'name': 'Обычный пользователь', 'role': 'user'}
    
    print("Администратор выполняет безопасную операцию:")
    secure_operation(admin_user)
    
    print("\nОбычный пользователь пытается выполнить безопасную операцию:")
    secure_operation(regular_user)

if __name__ == "__main__":
    main()