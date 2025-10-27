from model import Model
from view import View
from controller import Controller

if __name__ == "__main__":  
    DB_NAME = 'neschetna'     
    DB_USER = 'postgres'   
    DB_PASS = 'Qwertyasd111' 
    DB_HOST = 'localhost'  
    DB_PORT = '5432'       

    try:
        model_instance = Model(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)
        
        view_instance = View()
        
        controller_instance = Controller(model_instance, view_instance)
        
        controller_instance.run()

    except ImportError:
        print("Помилка: не вдалося знайти бібліотеку 'psycopg'.")
        print("Будь ласка, встановіть її: pip install psycopg")
    except Exception as e:
        print(f"Сталася непередбачувана помилка при запуску: {e}")
