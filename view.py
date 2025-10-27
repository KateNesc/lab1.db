from datetime import datetime
from decimal import Decimal, InvalidOperation

class View:
    def show_main_menu(self):
        """ Показує головне меню і повертає вибір користувача """
        print("\n--- Система Резервування Квитків ---")
        print("--- Меню Користувачів (User) ---")
        print("1. Показати всіх користувачів")
        print("2. Додати нового користувача")
        print("3. Редагувати користувача")
        print("4. Видалити користувача")
        print("--- Меню Заходів (Event) ---")
        print("5. Показати всі заходи")
        print("6. Додати новий захід")
        print("7. Редагувати захід")
        print("8. Видалити захід")
        print("--- Меню Квитків (Ticket) ---")
        print("9. Показати всі квитки")
        print("10. Додати новий квиток")
        print("11. Редагувати квиток")
        print("12. Видалити квиток")
        print("--- Меню Бронювань (Reservation) ---")
        print("13. Показати всі бронювання")
        print("14. Додати нове бронювання")
        print("15. Редагувати бронювання")
        print("16. Видалити бронювання")
        print("--- Інструменти ---")
        print("17. Згенерувати користувачів")
        print("18. Згенерувати заходи")
        print("19. Згенерувати квитки")
        print("20. Згенерувати бронювання")
        print("21. ❗️ ОЧИСТИТИ ВСІ ТАБЛИЦІ ❗️")
        print("--- Пошук (РГР) ---")
        print("22. Пошук 1: Доступні квитки на заходи")
        print("23. Пошук 2: Активність та витрати користувачів")
        print("24. Пошук 3: Деталізовані бронювання (Захід/Користувач/Місце)")
        print("---------------------------------")
        print("0. Вихід")
        return input("Оберіть опцію: ")

    def show_users(self, users):
        if not users:
            print("Користувачів не знайдено.")
            return
        
        print("\n--- Список Користувачів ---")
        for user in users:
            print(f"ID: {user[0]}, Ім'я: {user[1]} {user[2]}, Email: {user[3]}, Тел: {user[4]}")

    def get_new_user_data(self):
        print("\n--- Додавання Нового Користувача ---")
        name = input("Введіть ім'я: ")
        surname = input("Введіть прізвище: ")
        email = input("Введіть email: ")
        phone = input("Введіть телефон (10 символів): ")
        return name, surname, email, phone

    def get_user_id(self):
        """ Запитує ID користувача для операції """
        try:
            user_id = int(input("Введіть ID користувача: "))
            return user_id
        except ValueError:
            print("Помилка: ID має бути числом.")
            return None

    def confirm_delete(self, user):
        print(f"\n--- Підтвердження Видалення ---")
        print(f"Ви збираєтеся видалити користувача:")
        print(f"ID: {user[0]}, Ім'я: {user[1]} {user[2]}, Email: {user[3]}")
        choice = input("Ви впевнені? (так/ні): ").strip().lower()
        return choice == 'так'

    def get_updated_user_data(self, user):
        print(f"\n--- Редагування Користувача (ID: {user[0]}) ---")
        print("Введіть нові дані. Натисніть Enter, щоб залишити поточне значення.")
        
        current_name = user[1]
        current_surname = user[2]
        current_email = user[3]
        current_phone = user[4]

        name = input(f"Ім'я ({current_name}): ") or current_name
        surname = input(f"Прізвище ({current_surname}): ") or current_surname
        email = input(f"Email ({current_email}): ") or current_email
        phone = input(f"Телефон ({current_phone}): ") or current_phone
        
        return name, surname, email, phone

    def show_events(self, events):
        if not events:
            print("Заходів не знайдено.")
            return
        
        print("\n--- Список Заходів ---")
        for event in events:
            formatted_date = event[2].strftime('%Y-%m-%d')
            print(f"ID: {event[0]}, Назва: {event[1]}, Дата: {formatted_date}, Місце: {event[3]}")

    def get_new_event_data(self):
        print("\n--- Додавання Нового Заходу ---")
        title = input("Введіть назву заходу: ")
        
        while True:
            event_date_str = input("Введіть дату заходу (у форматі РРРР-ММ-ДД): ")
            try:
                datetime.strptime(event_date_str, '%Y-%m-%d')
                break 
            except ValueError:
                print("Помилка: Невірний формат дати. Спробуйте ще раз.")
                
        place = input("Введіть місце проведення: ")
        return title, event_date_str, place

    def get_event_id(self):
        try:
            event_id = int(input("Введіть ID заходу: "))
            return event_id
        except ValueError:
            print("Помилка: ID має бути числом.")
            return None

    def confirm_delete_event(self, event):
        print(f"\n--- Підтвердження Видалення Заходу ---")
        print(f"Ви збираєтеся видалити захід:")
        formatted_date = event[2].strftime('%Y-%m-%d')
        print(f"ID: {event[0]}, Назва: {event[1]}, Дата: {formatted_date}")
        choice = input("Ви впевнені? (так/ні): ").strip().lower()
        return choice == 'так'

    def get_updated_event_data(self, event):
        print(f"\n--- Редагування Заходу (ID: {event[0]}) ---")
        print("Введіть нові дані. Натисніть Enter, щоб залишити поточне значення.")
        
        current_title = event[1]
        current_date_str = event[2].strftime('%Y-%m-%d')
        current_place = event[3]

        title = input(f"Назва ({current_title}): ") or current_title
        
        while True:
            date_str = input(f"Дата ({current_date_str}): ") or current_date_str
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Помилка: Невірний формат дати. Спробуйте ще раз.")
                
        place = input(f"Місце ({current_place}): ") or current_place
        
        return title, date_str, place

    def show_tickets(self, tickets):
        if not tickets:
            print("Квитків не знайдено.")
            return
        
        print("\n--- Список Квитків ---")
        for ticket in tickets:
            status_str = "Доступний" if ticket[3] else "Проданий"
            print(f"ID: {ticket[0]}, Ціна: {ticket[1]:.2f} грн, Місце: {ticket[2]}, Статус: {status_str}, Захід: '{ticket[4]}' (ID: {ticket[5]})")

    def _get_validated_decimal(self, prompt):
        while True:
            price_str = input(prompt)
            try:
                price = Decimal(price_str)
                if price < 0:
                    print("Помилка: Ціна не може бути від'ємною.")
                else:
                    return price
            except InvalidOperation:
                print("Помилка: Введіть коректне число (напр., 150.50).")
    
    def _get_validated_int(self, prompt):
        while True:
            id_str = input(prompt)
            try:
                return int(id_str)
            except ValueError:
                print("Помилка: Введіть ціле число.")

    def _get_validated_bool(self, prompt):
        while True:
            status_str = input(prompt + " (так/ні): ").strip().lower()
            if status_str == 'так':
                return True
            elif status_str == 'ні':
                return False
            else:
                print("Помилка: Введіть 'так' або 'ні'.")

    def get_new_ticket_data(self):
        print("\n--- Додавання Нового Квитка ---")
        price = self._get_validated_decimal("Введіть ціну (напр., 250.00): ")
        place = self._get_validated_int("Введіть номер місця: ")
        status = self._get_validated_bool("Квиток доступний?")
        event_id = self._get_validated_int("Введіть ID заходу, до якого належить квиток: ")
        
        return price, place, status, event_id

    def get_ticket_id(self):
        return self._get_validated_int("Введіть ID квитка: ")

    def confirm_delete_ticket(self, ticket):
        print(f"\n--- Підтвердження Видалення Квитка ---")
        print(f"Ви збираєтеся видалити квиток:")
        status_str = "Доступний" if ticket[3] else "Проданий"
        print(f"ID: {ticket[0]}, Ціна: {ticket[1]} грн, Місце: {ticket[2]}, Статус: {status_str}, Захід: '{ticket[5]}'")
        choice = input("Ви впевнені? (так/ні): ").strip().lower()
        return choice == 'так'

    def get_updated_ticket_data(self, ticket):
        print(f"\n--- Редагування Квитка (ID: {ticket[0]}) ---")
        print("Введіть нові дані. Натисніть Enter, щоб залишити поточне значення.")
        
        current_price = ticket[1]
        current_place = ticket[2]
        current_status = ticket[3]
        current_event_id = ticket[4]
        
        while True:
            price_str = input(f"Ціна ({current_price}): ") or str(current_price)
            try:
                price = Decimal(price_str)
                if price < 0:
                    print("Помилка: Ціна не може бути від'ємною.")
                else:
                    break
            except InvalidOperation:
                print("Помилка: Введіть коректне число.")
        
        while True:
            place_str = input(f"Місце ({current_place}): ") or str(current_place)
            try:
                place = int(place_str)
                break
            except ValueError:
                print("Помилка: Введіть ціле число.")

        current_status_str = 'так' if current_status else 'ні'
        while True:
            status_str = input(f"Доступний ({current_status_str}): ") or current_status_str
            status_str = status_str.strip().lower()
            if status_str == 'так':
                status = True
                break
            elif status_str == 'ні':
                status = False
                break
            else:
                print("Помилка: Введіть 'так' або 'ні'.")

        while True:
            event_id_str = input(f"ID Заходу ({current_event_id}): ") or str(current_event_id)
            try:
                event_id = int(event_id_str)
                break
            except ValueError:
                print("Помилка: Введіть ціле число.")

        return price, place, status, event_id

    def _get_validated_date(self, prompt, default_date_str=None):
        if default_date_str:
            prompt_with_default = f"{prompt} ({default_date_str}): "
        else:
            prompt_with_default = prompt + ": "
            
        while True:
            date_str = input(prompt_with_default)
            if not date_str and default_date_str:
                date_str = default_date_str
            
            try:
                res_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                return res_date
            except ValueError:
                print("Помилка: Невірний формат дати. Потрібен РРРР-ММ-ДД.")

    def show_reservations(self, reservations):
        if not reservations:
            print("Бронювань не знайдено.")
            return
        
        print("\n--- Список Бронювань ---")
        for res in reservations:
            formatted_date = res[1].strftime('%Y-%m-%d')
            print(f"ID: {res[0]} | Дата: {formatted_date} | Користувач: {res[2]} {res[3]}")
            print(f"  └ Квиток ID: {res[4]} | Захід: '{res[5]}' (Місце: {res[6]})")
            print("-" * 20) 

    def get_new_reservation_data(self):
        print("\n--- Додавання Нового Бронювання ---")
        today_str = datetime.now().strftime('%Y-%m-%d')
        res_date = self._get_validated_date("Введіть дату бронювання", default_date_str=today_str)
        
        user_id = self._get_validated_int("Введіть ID користувача: ")
        ticket_id = self._get_validated_int("Введіть ID квитка для бронювання: ")
        
        return res_date, user_id, ticket_id

    def get_reservation_id(self):
        return self._get_validated_int("Введіть ID бронювання: ")

    def confirm_delete_reservation(self, reservation_details):
        print(f"\n--- Підтвердження Видалення Бронювання ---")
        print(f"Ви збираєтеся видалити бронювання ID: {reservation_details[0]}")
        print(f"Це звільнить Квиток ID: {reservation_details[4]} (Захід: '{reservation_details[5]}')")
        choice = input("Ви впевнені? (так/ні): ").strip().lower()
        return choice == 'так'

    def get_updated_reservation_data(self, reservation):
        print(f"\n--- Редагування Бронювання (ID: {reservation[0]}) ---")
        print("Введіть нові дані. Натисніть Enter, щоб залишити поточне значення.")
        
        current_date = reservation[1]
        current_date_str = current_date.strftime('%Y-%m-%d')
        current_user_id = reservation[2]
        current_ticket_id = reservation[3]

        res_date = self._get_validated_date("Дата", default_date_str=current_date_str)
        
        while True:
            user_id_str = input(f"ID Користувача ({current_user_id}): ") or str(current_user_id)
            try:
                user_id = int(user_id_str)
                break
            except ValueError:
                print("Помилка: Введіть ціле число.")
        
        while True:
            ticket_id_str = input(f"ID Квитка ({current_ticket_id}): ") or str(current_ticket_id)
            try:
                ticket_id = int(ticket_id_str)
                break
            except ValueError:
                print("Помилка: Введіть ціле число.")

        return res_date, user_id, ticket_id

    def get_generation_count(self) -> int | None:
        try:
            count = int(input("Введіть кількість записів для генерації (напр., 1000): "))
            if count <= 0:
                print("Помилка: Кількість має бути > 0.")
                return None
            return count
        except ValueError:
            print("Помилка: Введіть ціле число.")
            return None

    def confirm_clear_tables(self) -> bool:
        print("\n" + "!"*40)
        print("❗️ УВАГА! ЦЯ ДІЯ НЕЗВОРОТНЬО ВИДАЛИТЬ ❗️")
        print("❗️    ВСІ ДАНІ З УСІХ ТАБЛИЦЬ!    ❗️")
        print("!"*40)
        choice = input("Введіть 'ОЧИСТИТИ' для підтвердження: ")
        return choice == 'ОЧИСТИТИ'

    def _get_optional_date(self, prompt):
        date_str = input(prompt + " (РРРР-ММ-ДД, або Enter щоб пропустити): ").strip()
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Помилка: Невірний формат дати. Фільтр не буде застосовано.")
            return None

    def _get_optional_decimal(self, prompt):
        num_str = input(prompt + " (або Enter щоб пропустити): ").strip()
        if not num_str:
            return None
        try:
            return Decimal(num_str)
        except InvalidOperation:
            print("Помилка: Невірний формат числа. Фільтр не буде застосовано.")
            return None

    def _get_optional_int(self, prompt):
        num_str = input(prompt + " (або Enter щоб пропустити): ").strip()
        if not num_str:
            return None
        try:
            return int(num_str)
        except ValueError:
            print("Помилка: Невірний формат числа. Фільтр не буде застосовано.")
            return None

    def _get_optional_like_pattern(self, prompt):
        pattern = input(prompt + " (шаблон, або Enter щоб пропустити): ").strip()
        if not pattern:
            return None
        if '%' not in pattern and '_' not in pattern:
            return f"%{pattern}%"
        return pattern

    def _get_optional_bool(self, prompt):
        choice = input(prompt + " (так/ні, або Enter щоб пропустити): ").strip().lower()
        if choice == 'так':
            return True
        if choice == 'ні':
            return False
        return None

    def get_search_1_params(self):
        print("\n--- Пошук 1: Доступні квитки на заходи ---")
        print("Введіть фільтри (натисніть Enter, щоб пропустити фільтр)")
        
        date_start = self._get_optional_date("Дата заходу (ВІД)")
        date_end = self._get_optional_date("Дата заходу (ДО)")
        place_pattern = self._get_optional_like_pattern("Місце проведення (шаблон)")
        price_min = self._get_optional_decimal("Ціна квитка (ВІД)")
        price_max = self._get_optional_decimal("Ціна квитка (ДО)")
        status_bool = self._get_optional_bool("Квиток доступний?")
        
        return date_start, date_end, place_pattern, price_min, price_max, status_bool
        
    def show_search_1_results(self, results, exec_time):
        print("\n--- Результати Пошуку 1 ---")
        if not results:
            print("Нічого не знайдено.")
        
        for row in results:
            print(f"Захід: {row[0]} ({row[1].strftime('%Y-%m-%d')})")
            print(f"  Місце: {row[2]}")
            print(f"  Знайдено квитків (за фільтром): {row[3]}")
            print("-" * 20)
            
        print(f"\nЗнайдено рядків: {len(results)}")
        print(f"Час виконання запиту: {exec_time:.2f} мс")

    def get_search_2_params(self):
        print("\n--- Пошук 2: Активність та витрати користувачів ---")
        print("Введіть фільтри (натисніть Enter, щоб пропустити фільтр)")
        
        email_pattern = self._get_optional_like_pattern("Email користувача (шаблон)")
        res_date_start = self._get_optional_date("Дата бронювання (ВІД)")
        res_date_end = self._get_optional_date("Дата бронювання (ДО)")
        
        return email_pattern, res_date_start, res_date_end
        
    def show_search_2_results(self, results, exec_time):
        print("\n--- Результати Пошуку 2 ---")
        if not results:
            print("Нічого не знайдено.")
            
        for row in results:
            print(f"Користувач: {row[0]} {row[1]} ({row[2]})")
            print(f"  Всього бронювань (за фільтром): {row[3]}")
            print(f"  Всього витрачено (за фільтром): {row[4]:.2f} грн")
            print("-" * 20)
            
        print(f"\nЗнайдено рядків: {len(results)}")
        print(f"Час виконання запиту: {exec_time:.2f} мс")

    def get_search_3_params(self):
        print("\n--- Пошук 3: Деталізовані бронювання ---")
        print("Введіть фільтри (натисніть Enter, щоб пропустити фільтр)")
        
        event_title_pattern = self._get_optional_like_pattern("Назва заходу (шаблон)")
        user_phone_pattern = self._get_optional_like_pattern("Телефон користувача (шаблон)")
        place_min = self._get_optional_int("Номер місця (ВІД)")
        place_max = self._get_optional_int("Номер місця (ДО)")
        
        return event_title_pattern, user_phone_pattern, place_min, place_max
        
    def show_search_3_results(self, results, exec_time):
        print("\n--- Результати Пошуку 3 ---")
        if not results:
            print("Нічого не знайдено.")
            
        for row in results:
            print(f"Захід: {row[0]}")
            print(f"  Користувач: {row[1]} {row[2]} (Тел: {row[3]})")
            print(f"  Кількість бронювань (за фільтром): {row[4]}")
            print("-" * 20)
            
        print(f"\nЗнайдено рядків: {len(results)}")
        print(f"Час виконання запиту: {exec_time:.2f} мс")

    def show_message(self, message):
        print(message)
