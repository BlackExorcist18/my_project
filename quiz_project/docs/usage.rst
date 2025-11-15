Руководство пользователя
=========================

Обзор
-----

Система тестирования - это консольное приложение для создания и прохождения тестов.

Основные команды
----------------

Показать список тестов
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py list

Создать новый тест
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py create

Запустить тест
~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py run "Название теста"

С параметрами:

.. code-block:: bash

   python main.py run "Основы Python" --questions 5 --no-shuffle --save-results my_results.json

Показать результаты
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py results

Структура теста
---------------

Тесты хранятся в формате JSON:

.. code-block:: json

   [
     {
       "name": "Основы Python",
       "description": "Тест по основам Python",
       "questions": [
         {
           "question": "Вопрос?",
           "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
           "correct_answer": 0
         }
       ]
     }
   ]