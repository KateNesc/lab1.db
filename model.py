import psycopg
from datetime import date
from decimal import Decimal
import time

class Model:
    def __init__(self, dbname, user, password, host, port):
        self.conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg.connect(self.conn_string)
            print("Підключення до бази даних успішне!")
        except psycopg.OperationalError as e:
            print(f"Помилка підключення до бази даних: {e}")
            self.conn = None 

    def close(self):
        if self.conn:
            self.conn.close()
            print("З'єднання з базою даних закрито.")

    def get_user_by_id(self, user_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return None
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM "user" WHERE id = %s', (user_id,))
                return cur.fetchone() 
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні користувача: {e}")
            self.conn.rollback()
            return None
            
    def delete_user_by_id(self, user_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('DELETE FROM "user" WHERE id = %s', (user_id,))
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Користувача з ID {user_id} не знайдено."
            return True, "Користувача успішно видалено."
            
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, "Помилка: Неможливо видалити користувача, оскільки у нього є активні бронювання."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при видаленні користувача: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def update_user(self, user_id, name, surname, email, phone):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'UPDATE "user" SET name = %s, surname = %s, email = %s, phone = %s WHERE id = %s',
                    (name, surname, email, phone, user_id)
                )
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Користувача з ID {user_id} не знайдено."
            return True, "Дані користувача успішно оновлено."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при оновленні користувача: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def add_user(self, name, surname, email, phone):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "user" (name, surname, email, phone) VALUES (%s, %s, %s, %s)',
                    (name, surname, email, phone)
                )
                self.conn.commit()
            return True
        except psycopg.Error as e:
            print(f"Помилка бази даних при додаванні користувача: {e}")
            self.conn.rollback() 
            return False

    def get_all_users(self):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return []
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM "user" ORDER BY id ASC')
                return cur.fetchall()
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні користувачів: {e}")
            self.conn.rollback()
            return []

    def add_event(self, title, event_date, place):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "event" (title, date, place) VALUES (%s, %s, %s)',
                    (title, event_date, place)
                )
                self.conn.commit()
            return True, "Захід успішно додано."
        except psycopg.Error as e:
            print(f"Помилка бази даних при додаванні заходу: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def get_all_events(self):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return []
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM "event" ORDER BY id ASC')
                return cur.fetchall() 
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні заходів: {e}")
            self.conn.rollback()
            return []

    def get_event_by_id(self, event_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return None
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM "event" WHERE id = %s', (event_id,))
                return cur.fetchone()
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні заходу: {e}")
            self.conn.rollback()
            return None
            
    def delete_event_by_id(self, event_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('DELETE FROM "event" WHERE id = %s', (event_id,))
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Захід з ID {event_id} не знайдено."
            return True, "Захід успішно видалено."
            
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, "Помилка: Неможливо видалити захід, оскільки на нього існують квитки."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при видаленні заходу: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def update_event(self, event_id, title, event_date, place):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'UPDATE "event" SET title = %s, date = %s, place = %s WHERE id = %s',
                    (title, event_date, place, event_id)
                )
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Захід з ID {event_id} не знайдено."
            return True, "Дані заходу успішно оновлено."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при оновленні заходу: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def add_ticket(self, price: Decimal, place: int, status: bool, event_id: int):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "ticket" (price, place, status, event_id) VALUES (%s, %s, %s, %s)',
                    (price, place, status, event_id)
                )
                self.conn.commit()
            return True, "Квиток успішно додано."
        
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, f"Помилка: Неможливо додати квиток. Захід з ID {event_id} не існує."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при додаванні квитка: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def get_all_tickets(self):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return []
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT t.id, t.price::numeric, t.place, t.status, e.title AS event_title, t.event_id
                    FROM "ticket" t
                    JOIN "event" e ON t.event_id = e.id
                    ORDER BY t.id ASC
                ''')
                return cur.fetchall()
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні квитків: {e}")
            self.conn.rollback()
            return []

    def get_ticket_by_id(self, ticket_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return None
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT t.id, t.price::numeric, t.place, t.status, t.event_id, e.title
                    FROM "ticket" t
                    JOIN "event" e ON t.event_id = e.id
                    WHERE t.id = %s
                ''', (ticket_id,))
                return cur.fetchone()
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні квитка: {e}")
            self.conn.rollback()
            return None
            
    def delete_ticket_by_id(self, ticket_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('DELETE FROM "ticket" WHERE id = %s', (ticket_id,))
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Квиток з ID {ticket_id} не знайдено."
            return True, "Квиток успішно видалено."
            
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, "Помилка: Неможливо видалити квиток, оскільки на нього є активні бронювання."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при видаленні квитка: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def update_ticket(self, ticket_id: int, price: Decimal, place: int, status: bool, event_id: int):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'UPDATE "ticket" SET price = %s, place = %s, status = %s, event_id = %s WHERE id = %s',
                    (price, place, status, event_id, ticket_id)
                )
                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Квиток з ID {ticket_id} не знайдено."
            return True, "Дані квитка успішно оновлено."
        
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, f"Помилка: Неможливо оновити квиток. Захід з ID {event_id} не існує."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при оновленні квитка: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def add_reservation(self, res_date: date, user_id: int, ticket_id: int):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "reservation" (date, user_id, ticket_id) VALUES (%s, %s, %s)',
                    (res_date, user_id, ticket_id)
                )
                
                cur.execute(
                    'UPDATE "ticket" SET status = false WHERE id = %s',
                    (ticket_id,)
                )
                
                self.conn.commit()
            return True, "Бронювання успішно створено (квиток зарезервовано)."
        
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback() 
            return False, "Помилка: Користувач або Квиток з вказаними ID не існують."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при бронюванні: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def get_all_reservations(self):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return []
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT 
                        r.id AS reservation_id, 
                        r.date AS reservation_date,
                        u.name, u.surname,
                        t.id AS ticket_id, e.title AS event_title, t.place AS ticket_place
                    FROM "reservation" r
                    JOIN "user" u ON r.user_id = u.id
                    JOIN "ticket" t ON r.ticket_id = t.id
                    JOIN "event" e ON t.event_id = e.id
                    ORDER BY r.id ASC
                ''')
                return cur.fetchall()
        except psycopg.Error as e:
            print(f"Помилка бази даних при отриманні бронювань: {e}")
            self.conn.rollback()
            return []

    def get_reservation_by_id(self, reservation_id):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return None
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT id, date, user_id, ticket_id 
                    FROM "reservation" 
                    WHERE id = %s
                ''', (reservation_id,))
                return cur.fetchone()
        except psycopg.Error as e:
            print(f"Помилка бази даних: {e}")
            self.conn.rollback()
            return None
            
    def delete_reservation_by_id(self, reservation_id: int, ticket_id_to_release: int):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute('DELETE FROM "reservation" WHERE id = %s', (reservation_id,))
                
                cur.execute(
                    'UPDATE "ticket" SET status = true WHERE id = %s',
                    (ticket_id_to_release,)
                )
                
                self.conn.commit()
                
                if cur.rowcount == 0:
                    return False, f"Помилка: Бронювання видалено, але квиток {ticket_id_to_release} не знайдено."
            
            return True, "Бронювання успішно видалено (квиток знову доступний)."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних при видаленні бронювання: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def update_reservation(self, reservation_id: int, res_date: date, user_id: int, new_ticket_id: int, old_ticket_id: int):
        if not self.conn:
            print("Немає з'єднання з БД.")
            return False, "Немає з'єднання з БД."
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'UPDATE "reservation" SET date = %s, user_id = %s, ticket_id = %s WHERE id = %s',
                    (res_date, user_id, new_ticket_id, reservation_id)
                )
                
                if new_ticket_id != old_ticket_id:
                    cur.execute(
                        'UPDATE "ticket" SET status = true WHERE id = %s',
                        (old_ticket_id,)
                    )
                    cur.execute(
                        'UPDATE "ticket" SET status = false WHERE id = %s',
                        (new_ticket_id,)
                    )

                self.conn.commit()
                if cur.rowcount == 0:
                    return False, f"Помилка: Бронювання з ID {reservation_id} не знайдено."
            
            return True, "Бронювання успішно оновлено."
        
        except psycopg.errors.ForeignKeyViolation as e:
            print(f"Помилка цілісності: {e}")
            self.conn.rollback()
            return False, "Помилка: Новий User ID або Ticket ID не існує."
            
        except psycopg.Error as e:
            print(f"Помилка бази даних: {e}")
            self.conn.rollback()
            return False, f"Помилка бази даних: {e}"

    def _check_table_empty(self, table_name: str) -> bool:
        if not self.conn:
            return True
        try:
            with self.conn.cursor() as cur:
                cur.execute(f'SELECT 1 FROM "{table_name}" LIMIT 1')
                return cur.fetchone() is None
        except psycopg.Error as e:
            print(f"Помилка перевірки таблиці {table_name}: {e}")
            return True

    def _get_available_tickets_count(self) -> int:
        if not self.conn:
            return 0
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM "ticket" WHERE status = true')
                return cur.fetchone()[0]
        except psycopg.Error as e:
            print(f"Помилка отримання кількості квитків: {e}")
            return 0

    def clear_all_tables(self):

        if not self.conn:
            return False, "Немає з'єднання з БД."
        try:
            with self.conn.cursor() as cur:
                cur.execute('TRUNCATE "reservation", "ticket", "user", "event" RESTART IDENTITY CASCADE')
                self.conn.commit()
            return True, "Всі таблиці успішно очищено. Лічильники ID скинуто."
        except psycopg.Error as e:
            self.conn.rollback()
            print(f"Помилка очищення таблиць: {e}")
            return False, f"Помилка очищення таблиць: {e}"


    def generate_users(self, count: int):
        if not self.conn:
            return False, "Немає з'єднання з БД."
        
        sql = """
            INSERT INTO "user" (name, surname, email, phone)
            SELECT 
                -- 1. Отримуємо кириличне Ім'я
                (array['Іван', 'Петро', 'Анна', 'Марія', 'Сергій', 'Олена', 'Олександр', 'Тетяна'])[idx.name_idx],
                
                -- 2. Отримуємо кириличне Прізвище
                (array['Шевченко', 'Ковальчук', 'Петренко', 'Сидоренко', 'Мельник', 'Бондаренко', 'Лисенко'])[idx.surname_idx],
                
                -- 3. Будуємо email
                lower(
                    -- Беремо латинське Ім'я
                    (array['Ivan', 'Petro', 'Anna', 'Maria', 'Sergiy', 'Olena', 'Oleksandr', 'Tetiana'])[idx.name_idx] || '.' ||
                    -- Беремо латинське Прізвище
                    (array['Shevchenko', 'Kovalchuk', 'Petrenko', 'Sydorenko', 'Melnyk', 'Bondarenko', 'Lysenko'])[idx.surname_idx] ||
                    trunc(random()*100)::text
                ) || '@' || (array['gmail.com', 'ukr.net', 'lll.kpi.ua'])[trunc(random()*3+1)::int],
                
                -- 4. Будуємо телефон
                '0' || (array['50','67','93','95','66'])[trunc(random()*5+1)::int] || 
                    lpad(trunc(random()*10000000)::text, 7, '0')
            
            FROM (
                -- Цей підзапит генерує випадкові індекси N разів
                SELECT 
                    trunc(random()*8+1)::int AS name_idx,
                    trunc(random()*7+1)::int AS surname_idx
                FROM generate_series(1, %s)
            ) AS idx;
        """
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (count,)) 
                self.conn.commit()
            return True, f"Успішно згенеровано {count} користувачів."
        except psycopg.Error as e:
            self.conn.rollback()
            return False, f"Помилка генерації користувачів: {e}"

    def generate_events(self, count: int):
        if not self.conn:
            return False, "Немає з'єднання з БД."
        
        sql = """
            INSERT INTO "event" (title, date, place)
            SELECT 
                (array['Концерт', 'Фестиваль', 'Вистава', 'Матч', 'Виставка'])[trunc(random()*5+1)::int] || ' ' || 
                (array['"Мрія"', '"Надія"', '"Перемога"', '"Весна"', '"Україна"'])[trunc(random()*5+1)::int],
                (timestamp '2025-11-01' + random() * (timestamp '2026-05-30' - timestamp '2025-11-01'))::date,
                (array['Палац Спорту, Київ', 'НСК Олімпійський, Київ', 'Театр ім. Франка, Київ', 'Arena Lviv, Львів', 'Stereoplaza, Київ'])[trunc(random()*5+1)::int]
            FROM generate_series(1, %s);
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (count,))
                self.conn.commit()
            return True, f"Успішно згенеровано {count} заходів."
        except psycopg.Error as e:
            self.conn.rollback()
            return False, f"Помилка генерації заходів: {e}"

    def generate_tickets(self, count: int):
        if not self.conn:
            return False, "Немає з'єднання з БД."
        
        sql = """
            WITH event_data AS (
                -- 1. Збираємо всі існуючі ID заходів в один масив
                --    та отримуємо їх загальну кількість.
                SELECT array_agg(id) AS ids, count(id) AS total_count
                FROM "event"
            )
            INSERT INTO "ticket" (price, place, status, event_id)
            SELECT
                trunc(random() * 1900 + 100)::numeric, -- Ціна від 100 до 2000
                trunc(random() * 200 + 1)::int,       -- Місце від 1 до 200
                true,                                 -- Статус (доступний)
                
                -- 2. Для КОЖНОГО рядка вибираємо випадковий ID з масиву
                e.ids[ trunc(random() * e.total_count + 1)::int ]
                
            FROM generate_series(1, %s) -- Сюди підставляється 'count'
            CROSS JOIN event_data e; -- Приєднуємо масив ID до кожної згенерованої строки
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (count,))
                self.conn.commit()
            return True, f"Успішно згенеровано {count} квитків."
        except psycopg.errors.NotNullViolation as e:
             self.conn.rollback()
             return False, "Помилка: Неможливо згенерувати квитки. Таблиця 'event' порожня."
        except psycopg.Error as e:
            self.conn.rollback()
            return False, f"Помилка генерації квитків: {e}"
            
    def generate_reservations(self, count: int):
        if not self.conn:
            return False, "Немає з'єднання з БД."

        sql = """
            WITH user_data AS (
                -- 1. Збираємо всі існуючі ID користувачів в один масив
                SELECT array_agg(id) AS ids, count(id) AS total_count
                FROM "user"
            ),
            tickets_to_book AS (
                -- 2. Вибираємо N випадкових ВІЛЬНИХ квитків
                SELECT id 
                FROM "ticket" 
                WHERE status = true 
                ORDER BY random() 
                LIMIT %s -- Ліміт дорівнює 'count'
            ), 
            new_reservations AS (
                -- 3. Вставляємо бронювання, вибираючи випадкового користувача
                INSERT INTO "reservation" (date, user_id, ticket_id)
                SELECT 
                    (timestamp '2025-10-01' + random() * (timestamp '2025-10-27' - timestamp '2025-10-01'))::date,
                    
                    -- 3a. Для КОЖНОГО рядка вибираємо випадковий user_id з масиву
                    u.ids[ trunc(random() * u.total_count + 1)::int ],
                    
                    t.id
                FROM tickets_to_book t
                CROSS JOIN user_data u -- Приєднуємо масив ID користувачів
                RETURNING ticket_id -- Повертаємо ID квитків, які ми забронювали
            )
            -- 4. Оновлюємо статус цих квитків
            UPDATE "ticket"
            SET status = false
            WHERE id IN (SELECT ticket_id FROM new_reservations);
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (count,))
                self.conn.commit()
            return True, f"Успішно згенеровано {count} бронювань (квитки оновлено)."
        except psycopg.errors.NotNullViolation as e:
             self.conn.rollback()
             return False, "Помилка: Неможливо згенерувати бронювання. Таблиця 'user' порожня."
        except psycopg.Error as e:
            self.conn.rollback()
            return False, f"Помилка генерації бронювань: {e}"

    def search_query_1(self, date_start, date_end, place_pattern, price_min, price_max, status_bool):
        if not self.conn:
            return [], 0.0, "Немає з'єднання з БД."
            
        sql_base = """
            SELECT e.title, e.date, e.place, COUNT(t.id) as tickets_count
            FROM "event" e
            JOIN "ticket" t ON e.id = t.event_id
        """
        where_clauses = []
        params = []
        
        if date_start:
            where_clauses.append("e.date >= %s")
            params.append(date_start)
        if date_end:
            where_clauses.append("e.date <= %s")
            params.append(date_end)
        if place_pattern:
            where_clauses.append("e.place ILIKE %s") # ILIKE - нечутливий до регістру
            params.append(place_pattern)
        if price_min is not None:
            where_clauses.append("t.price::numeric >= %s")
            params.append(price_min)
        if price_max is not None:
            where_clauses.append("t.price::numeric <= %s")
            params.append(price_max)
        if status_bool is not None:
            where_clauses.append("t.status = %s")
            params.append(status_bool)

        sql_full = sql_base
        if where_clauses:
            sql_full += " WHERE " + " AND ".join(where_clauses)
            
        sql_full += " GROUP BY e.id, e.title, e.date, e.place ORDER BY e.date"
        
        try:
            with self.conn.cursor() as cur:
                start_time = time.perf_counter()
                cur.execute(sql_full, tuple(params))
                results = cur.fetchall()
                end_time = time.perf_counter()
                
                execution_time_ms = (end_time - start_time) * 1000
                return results, execution_time_ms, None # (results, time, error)
                
        except psycopg.Error as e:
            self.conn.rollback()
            return [], 0.0, f"Помилка виконання запиту: {e}"

    def search_query_2(self, email_pattern, res_date_start, res_date_end):
        if not self.conn:
            return [], 0.0, "Немає з'єднання з БД."
            
        sql_base = """
            SELECT 
                u.name, u.surname, u.email,
                COUNT(r.id) as total_bookings,
                SUM(t.price::numeric) as total_spent
            FROM "user" u
            JOIN "reservation" r ON u.id = r.user_id
            JOIN "ticket" t ON r.ticket_id = t.id
        """
        where_clauses = []
        params = []
        
        if email_pattern:
            where_clauses.append("u.email ILIKE %s")
            params.append(email_pattern)
        if res_date_start:
            where_clauses.append("r.date >= %s")
            params.append(res_date_start)
        if res_date_end:
            where_clauses.append("r.date <= %s")
            params.append(res_date_end)
            
        sql_full = sql_base
        if where_clauses:
            sql_full += " WHERE " + " AND ".join(where_clauses)
            
        sql_full += " GROUP BY u.id, u.name, u.surname, u.email ORDER BY total_spent DESC"
        
        try:
            with self.conn.cursor() as cur:
                start_time = time.perf_counter()
                cur.execute(sql_full, tuple(params))
                results = cur.fetchall()
                end_time = time.perf_counter()
                
                execution_time_ms = (end_time - start_time) * 1000
                return results, execution_time_ms, None
                
        except psycopgError as e:
            self.conn.rollback()
            return [], 0.0, f"Помилка виконання запиту: {e}"

    def search_query_3(self, event_title_pattern, user_phone_pattern, place_min, place_max):
        if not self.conn:
            return [], 0.0, "Немає з'єднання з БД."
            
        sql_base = """
            SELECT 
                e.title,
                u.name, u.surname, u.phone,
                COUNT(r.id) as bookings_count
            FROM "reservation" r
            JOIN "user" u ON r.user_id = u.id
            JOIN "ticket" t ON r.ticket_id = t.id
            JOIN "event" e ON t.event_id = e.id
        """
        where_clauses = []
        params = []
        
        if event_title_pattern:
            where_clauses.append("e.title ILIKE %s")
            params.append(event_title_pattern)
        if user_phone_pattern:
            where_clauses.append("u.phone LIKE %s") 
            params.append(user_phone_pattern)
        if place_min is not None:
            where_clauses.append("t.place >= %s")
            params.append(place_min)
        if place_max is not None:
            where_clauses.append("t.place <= %s")
            params.append(place_max)
            
        sql_full = sql_base
        if where_clauses:
            sql_full += " WHERE " + " AND ".join(where_clauses)
            
        sql_full += " GROUP BY e.id, e.title, u.id, u.name, u.surname, u.phone ORDER BY e.title, bookings_count DESC"
        
        try:
            with self.conn.cursor() as cur:
                start_time = time.perf_counter()
                cur.execute(sql_full, tuple(params))
                results = cur.fetchall()
                end_time = time.perf_counter()
                
                execution_time_ms = (end_time - start_time) * 1000
                return results, execution_time_ms, None
                
        except psycopg.Error as e:
            self.conn.rollback()
            return [], 0.0, f"Помилка виконання запиту: {e}"
