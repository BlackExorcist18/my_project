"""Настройки базы данных."""

import os
from dotenv import load_dotenv

load_dotenv()

# URL подключения к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://quiz_user:quiz_password@localhost:5432/quiz_system')

# Настройки подключения
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'quiz_system'),
    'user': os.getenv('DB_USER', 'quiz_user'),
    'password': os.getenv('DB_PASSWORD', 'quiz_password')
}