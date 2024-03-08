import sqlite3
from datetime import date

# Подключение к базе данных
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Создание таблиц в базе данных
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    teacher TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY,
    number  INTEGER,
    capacity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY,
    subject_name STRING,
    teacher TEXT,
    classroom_id INTEGER,
    date DATE,
    status TEXT DEFAULT 'active'
    
)
''')

# Добавление предмета в расписание
def add_subject(name, teacher):
    cursor.execute('INSERT INTO subjects (name, teacher) VALUES (?, ?)', (name, teacher))
    conn.commit()

# Добавление кабинета
def add_classroom(number,capacity):
    cursor.execute('INSERT INTO classrooms (number, capacity) VALUES (?,?)', (number,capacity,))
    conn.commit()

# Получение идентификатора предмета по его названию
def get_subject_id_by_name(name):
    cursor.execute('SELECT id FROM subjects WHERE name = ?', (name,))
    subject_id = cursor.fetchone()
    if subject_id:
        return subject_id[0]
    else:
        return None

# Добавление урока в расписание
def add_lesson(subject_name, teacher, classroom_id, date):
    if subject_name:
        cursor.execute('INSERT INTO schedule (subject_name, teacher, classroom_id, date) VALUES (?, ?, ?, ?)', (subject_name, teacher, classroom_id, date))
        conn.commit()
        print("Урок успешно добавлен в расписание.")
    else:
        print("Предмет с таким названием не найден.")

# Просмотр расписания на сегодня
def view_schedule_today():
    today = date.today()

    cursor.execute('''
    SELECT subject_name, teacher, classroom_id, date, id
    FROM schedule
    WHERE date = ? AND status = 'active'
    ''', (today,))
    schedule = cursor.fetchall()

    return schedule
# Проверка ввода
def validate_record_id(record_id):
    cursor.execute('SELECT id FROM schedule WHERE id = ? AND status = "active"', (record_id,))
    record = cursor.fetchone()
    return record is not None
# Проверка ввода
def validate_classroom(classroom_id):
    cursor.execute('SELECT id FROM classrooms WHERE number= ?', (classroom_id,))
    classroom = cursor.fetchone()
    return classroom is not None

# Проверка ввода
def validate_subject(subject):
    cursor.execute('SELECT id FROM subjects WHERE name= ?', (subject,))
    subject = cursor.fetchone()
    return subject is not None

# Получить список всех кабинетов
def get_classroom():
    cursor.execute('''
    SELECT id, number, capacity from classrooms
    ''')
    classroom = cursor.fetchall()
    return classroom

# Скрыть запись в расписании
def hide_schedule_record(record_id):
    cursor.execute('UPDATE schedule SET status = "hidden" WHERE id = ?', (record_id,))
    conn.commit()

# Закрытие соединения с базой данных
def close_connection():
    conn.close()
