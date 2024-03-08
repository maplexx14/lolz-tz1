# Ипорт функций из файла с управлением базой данных
import database


# Главная функция
def main():
    # Зацикливание программы
    while True:
        print("\nВыберите действие:")
        print("1. Добавить предмет")
        print("2. Добавить кабинет")
        print("3. Добавить урок")
        print("4. Просмотреть расписание на сегодня")
        print("5. Скрыть запись в расписании")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1': # Добавление предмета
            name = input("Введите название предмета: ")

            teacher = input("Введите имя преподавателя: ")
            database.add_subject(name, teacher)
        elif choice == '2': # Добавление кабинета

            while True:
                capacity = int(input("Введите вместимость кабинета: "))
                if not capacity <=0:
                    print("Вместимость не может быть отрицательной")
                    break

            while True:
                number = int(input("Введите номер кабинета (от 1 до 150): "))
                if not 1 <= number <= 150:
                    print('Введен неверный номер кабинета')
                    continue
                break


            database.add_classroom(number, capacity)
        elif choice == '3':# Добавление урока
            # Проверка ввода предмета
            # Если в базе есть такой предмет, то проходит дальше, если нет, то происходит повторный ввод
            while True:
                subject_name = input("Введите название предмета: ")

                if not database.validate_subject(subject_name):
                    print("Некорректное название предмета")
                    continue
                break


            classes = database.get_classroom()
            # Вывод информации о кабинетах
            for room in classes:
                print(f'Номер кабинета {room[1]}\n'
                      f'Вместимость кабинета {room[2]}\n')
            # Проверка ввода номера кабинета
            # Если в базе есть такой номер, то проходит дальше, если нет, то происходит повторный ввод
            while True:
                try:
                    classroom = int(input('Выберите кабинет: '))

                    if not database.validate_classroom(classroom):
                        print('Некорректный номер кабинета. Пожалуйста, выберите из списка.')
                        continue
                    break


                except:
                    print("Неверный ввод")

            date = input("Введите дату урока (ГГГГ-ММ-ДД): ")
            teacher = input("Введите имя преподавателя: ")
            if not database.validate_teacher_schedule(teacher, date):
                print("Преподаватель проводит уже 5 уроков в этот день. Выберите другую дату или преподавателя.")
                continue
            # Добавление
            database.add_lesson(subject_name, teacher, classroom, date)
        elif choice == '4': # Вывод расписания на сегодняшний день
            schedule = database.view_schedule_today()
            # Если расписание есть, то вывод
            if not schedule:
                print("На сегодня расписания нет.")
                continue

            print("\nРасписание на сегодня:")
            for lesson in schedule:
                print("ID урока:", lesson[4])
                print("Предмет:", lesson[0])
                print("Преподаватель:", lesson[1])
                print("Кабинет:", lesson[2])
                print("Вместимость кабинета:", lesson[3])
                print()
        elif choice == '5':# Скрытие записи
            record_id = int(input("Введите ID записи, которую хотите скрыть: "))
            if database.validate_record_id(record_id):
                database.hide_schedule_record(record_id)
                print("Запись успешно скрыта.")
            else:
                print("Некорректный ID записи.")
        elif choice == '6':# Выход из программы
            database.close_connection()
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")

# Если запуск произошел с главного файла
if __name__ == "__main__":
    main()

