from model import Model
from view import View
from datetime import datetime
from decimal import Decimal

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        """ Головний цикл програми """
        self.model.connect()
        if not self.model.conn:
            self.view.show_message("Не вдалося підключитися до бази даних. Програма завершує роботу.")
            return

        while True:
            choice = self.view.show_main_menu()

            if choice == '1':
                self.show_all_users()
            elif choice == '2':
                self.add_new_user()
            elif choice == '3':
                self.update_user()
            elif choice == '4':
                self.delete_user()

            elif choice == '5':
                self.show_all_events()
            elif choice == '6':
                self.add_new_event()
            elif choice == '7':
                self.update_event()
            elif choice == '8':
                self.delete_event()

            elif choice == '9':
                self.show_all_tickets()
            elif choice == '10':
                self.add_new_ticket()
            elif choice == '11':
                self.update_ticket()
            elif choice == '12':
                self.delete_ticket()

            elif choice == '13':
                self.show_all_reservations()
            elif choice == '14':
                self.add_new_reservation()
            elif choice == '15':
                self.update_reservation()
            elif choice == '16':
                self.delete_reservation()

            elif choice == '17':
                self.generate_data_users()
            elif choice == '18':
                self.generate_data_events()
            elif choice == '19':
                self.generate_data_tickets()
            elif choice == '20':
                self.generate_data_reservations()
            elif choice == '21':
                self.clear_tables()

            elif choice == '22':
                self._handle_search_1()
            elif choice == '23':
                self._handle_search_2()
            elif choice == '24':
                self._handle_search_3()
                
            elif choice == '0':
                self.model.close()
                self.view.show_message("До побачення!")
                break
            else:
                self.view.show_message("Невірний вибір. Спробуйте ще раз.")

    def delete_user(self):
        user_id = self.view.get_user_id()
        if user_id is None:
            return 

        user_data = self.model.get_user_by_id(user_id)
        if not user_data:
            self.view.show_message(f"Помилка: Користувача з ID {user_id} не знайдено.")
            return

        if self.view.confirm_delete(user_data):
            success, message = self.model.delete_user_by_id(user_id)
            self.view.show_message(message)
        else:
            self.view.show_message("Видалення скасовано.")

    def update_user(self):
        user_id = self.view.get_user_id()
        if user_id is None:
            return

        user_data = self.model.get_user_by_id(user_id)
        if not user_data:
            self.view.show_message(f"Помилка: Користувача з ID {user_id} не знайдено.")
            return
            
        try:
            name, surname, email, phone = self.view.get_updated_user_data(user_data)

            if not name or not surname or not email or not phone:
                self.view.show_message("Помилка: Всі поля повинні бути заповнені.")
                return
            if len(phone) != 10:
                 self.view.show_message("Помилка: Телефон має містити 10 символів.")
                 return

            success, message = self.model.update_user(user_id, name, surname, email, phone)
            
            self.view.show_message(message)

        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def show_all_users(self):
        users = self.model.get_all_users()
        self.view.show_users(users)

    def add_new_user(self):
        try:
            name, surname, email, phone = self.view.get_new_user_data()
            
            if not name or not surname or not email or not phone:
                self.view.show_message("Помилка: Всі поля повинні бути заповнені.")
                return
            if len(phone) != 10:
                 self.view.show_message("Помилка: Телефон має містити 10 символів.")
                 return

            success = self.model.add_user(name, surname, email, phone)
            
            if success:
                self.view.show_message("Користувача успішно додано!")
            else:
                self.view.show_message("Не вдалося додати користувача.")
        
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def show_all_events(self):
        events = self.model.get_all_events()
        self.view.show_events(events)

    def add_new_event(self):
        try:
            title, event_date_str, place = self.view.get_new_event_data()
            
            if not title or not event_date_str or not place:
                self.view.show_message("Помилка: Всі поля повинні бути заповнені.")
                return

            success, message = self.model.add_event(title, event_date_str, place)
            
            self.view.show_message(message)
        
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def delete_event(self):
        event_id = self.view.get_event_id()
        if event_id is None:
            return 

        event_data = self.model.get_event_by_id(event_id)
        if not event_data:
            self.view.show_message(f"Помилка: Захід з ID {event_id} не знайдено.")
            return

        if self.view.confirm_delete_event(event_data):
            success, message = self.model.delete_event_by_id(event_id)
            self.view.show_message(message)
        else:
            self.view.show_message("Видалення скасовано.")

    def update_event(self):
        event_id = self.view.get_event_id()
        if event_id is None:
            return

        event_data = self.model.get_event_by_id(event_id)
        if not event_data:
            self.view.show_message(f"Помилка: Захід з ID {event_id} не знайдено.")
            return
            
        try:
            title, event_date_str, place = self.view.get_updated_event_data(event_data)

            if not title or not event_date_str or not place:
                self.view.show_message("Помилка: Всі поля повинні бути заповнені.")
                return

            success, message = self.model.update_event(event_id, title, event_date_str, place)
            
            self.view.show_message(message)

        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def show_all_tickets(self):
        tickets = self.model.get_all_tickets()
        self.view.show_tickets(tickets)

    def add_new_ticket(self):
        try:
            price, place, status, event_id = self.view.get_new_ticket_data()
            
            if not self.model.get_event_by_id(event_id):
                self.view.show_message(f"Помилка: Захід з ID {event_id} не існує. Створіть захід перед додаванням квитка.")
                return

            success, message = self.model.add_ticket(price, place, status, event_id)
            
            self.view.show_message(message)
        
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def delete_ticket(self):
        ticket_id = self.view.get_ticket_id()
        if ticket_id is None:
            return 
        ticket_data = self.model.get_ticket_by_id(ticket_id)
        if not ticket_data:
            self.view.show_message(f"Помилка: Квиток з ID {ticket_id} не знайдено.")
            return

        if self.view.confirm_delete_ticket(ticket_data):
            success, message = self.model.delete_ticket_by_id(ticket_id)
            self.view.show_message(message)
        else:
            self.view.show_message("Видалення скасовано.")

    def update_ticket(self):
        ticket_id = self.view.get_ticket_id()
        if ticket_id is None:
            return

        ticket_data = self.model.get_ticket_by_id(ticket_id)
        if not ticket_data:
            self.view.show_message(f"Помилка: Квиток з ID {ticket_id} не знайдено.")
            return
            
        try:
            price, place, status, event_id = self.view.get_updated_ticket_data(ticket_data)

            if event_id != ticket_data[4]:
                if not self.model.get_event_by_id(event_id):
                    self.view.show_message(f"Помилка: Захід з ID {event_id} не існує.")
                    return

            success, message = self.model.update_ticket(ticket_id, price, place, status, event_id)
            
            self.view.show_message(message)

        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def show_all_reservations(self):
        reservations = self.model.get_all_reservations()
        self.view.show_reservations(reservations)

    def add_new_reservation(self):
        try:
            res_date, user_id, ticket_id = self.view.get_new_reservation_data()
            
            if not self.model.get_user_by_id(user_id):
                self.view.show_message(f"Помилка: Користувач з ID {user_id} не існує.")
                return

            ticket_data = self.model.get_ticket_by_id(ticket_id)
            if not ticket_data:
                self.view.show_message(f"Помилка: Квиток з ID {ticket_id} не існує.")
                return
            
            if not ticket_data[3]: 
                self.view.show_message(f"Помилка: Квиток з ID {ticket_id} вже заброньований.")
                return

            success, message = self.model.add_reservation(res_date, user_id, ticket_id)
            
            self.view.show_message(message)
        
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def delete_reservation(self):
        reservation_id = self.view.get_reservation_id()
        if reservation_id is None:
            return 

        reservation_data = self.model.get_reservation_by_id(reservation_id)
        if not reservation_data:
            self.view.show_message(f"Помилка: Бронювання з ID {reservation_id} не знайдено.")
            return

        full_details = self.model.get_all_reservations() 
        details_to_show = next((r for r in full_details if r[0] == reservation_id), None)

        if self.view.confirm_delete_reservation(details_to_show):
            ticket_id_to_release = reservation_data[3] 
            success, message = self.model.delete_reservation_by_id(reservation_id, ticket_id_to_release)
            self.view.show_message(message)
        else:
            self.view.show_message("Видалення скасовано.")

    def update_reservation(self):
        reservation_id = self.view.get_reservation_id()
        if reservation_id is None:
            return

        old_reservation_data = self.model.get_reservation_by_id(reservation_id)
        if not old_reservation_data:
            self.view.show_message(f"Помилка: Бронювання з ID {reservation_id} не знайдено.")
            return
            
        old_ticket_id = old_reservation_data[3] 
            
        try:
            new_date, new_user_id, new_ticket_id = self.view.get_updated_reservation_data(old_reservation_data)

            if not self.model.get_user_by_id(new_user_id):
                self.view.show_message(f"Помилка: Новий Користувач з ID {new_user_id} не існує.")
                return
            
            if new_ticket_id != old_ticket_id:
                new_ticket_data = self.model.get_ticket_by_id(new_ticket_id)
                if not new_ticket_data:
                    self.view.show_message(f"Помилка: Новий Квиток з ID {new_ticket_id} не існує.")
                    return
                if not new_ticket_data[3]: 
                    self.view.show_message(f"Помилка: Новий Квиток з ID {new_ticket_id} вже заброньований.")
                    return

            success, message = self.model.update_reservation(
                reservation_id, new_date, new_user_id, new_ticket_id, old_ticket_id
            )
            
            self.view.show_message(message)

        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка: {e}")

    def clear_tables(self):
        if self.view.confirm_clear_tables():
            success, message = self.model.clear_all_tables()
            self.view.show_message(message)
        else:
            self.view.show_message("Очищення скасовано.")

    def generate_data_users(self):
        count = self.view.get_generation_count()
        if count:
            success, message = self.model.generate_users(count)
            self.view.show_message(message)

    def generate_data_events(self):
        count = self.view.get_generation_count()
        if count:
            success, message = self.model.generate_events(count)
            self.view.show_message(message)

    def generate_data_tickets(self):
        if self.model._check_table_empty("event"):
            self.view.show_message("Помилка: Неможливо згенерувати квитки, оскільки немає жодного заходу.")
            self.view.show_message("Будь ласка, спочатку згенеруйте 'Заходи' (пункт 18).")
            return
            
        count = self.view.get_generation_count()
        if count:
            success, message = self.model.generate_tickets(count)
            self.view.show_message(message)

    def generate_data_reservations(self):
        if self.model._check_table_empty("user"):
            self.view.show_message("Помилка: Неможливо згенерувати бронювання, оскільки немає жодного користувача.")
            self.view.show_message("Будь ласка, спочатку згенеруйте 'Користувачів' (пункт 17).")
            return
            
        available_tickets = self.model._get_available_tickets_count()
        if available_tickets == 0:
            self.view.show_message("Помилка: Неможливо згенерувати бронювання, оскільки немає вільних квитків.")
            self.view.show_message("Будь ласка, спочатку згенеруйте 'Квитки' (пункт 19).")
            return
            
        count = self.view.get_generation_count()
        if not count:
            return 
            
        if count > available_tickets:
            self.view.show_message(f"Помилка: Ви хочете згенерувати {count} бронювань, але є лише {available_tickets} вільних квитків.")
            self.view.show_message("Будь ласка, введіть меншу кількість або згенеруйте більше квитків.")
            return
        success, message = self.model.generate_reservations(count)
        self.view.show_message(message)

    def _handle_search_1(self):
        try:
            params = self.view.get_search_1_params()
            
            results, exec_time, error = self.model.search_query_1(*params)
            
            if error:
                self.view.show_message(error)
            else:
                self.view.show_search_1_results(results, exec_time)
                
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка контролера: {e}")

    def _handle_search_2(self):
        try:
            params = self.view.get_search_2_params()
            results, exec_time, error = self.model.search_query_2(*params)
            
            if error:
                self.view.show_message(error)
            else:
                self.view.show_search_2_results(results, exec_time)
                
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка контролера: {e}")

    def _handle_search_3(self):
        try:
            params = self.view.get_search_3_params()
            results, exec_time, error = self.model.search_query_3(*params)
            
            if error:
                self.view.show_message(error)
            else:
                self.view.show_search_3_results(results, exec_time)
                
        except Exception as e:
            self.view.show_message(f"Сталася неочікувана помилка контролера: {e}")

