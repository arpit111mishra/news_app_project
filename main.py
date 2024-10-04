import logging
from auth import load_users, login, add_new_user, delete_user
from password import reset_password
from news import fetch_news

logging.basicConfig(
    filename='app.log',  
    filemode='a',        
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO    
)

def user_session(users):  
    while True:
        print("\n--- User Session ---")
        print("1. Fetch News")
        print("2. Logout")
        print("3. Delete Account") 
        choice = input("Enter your choice: ")

        if choice == '1':
            fetch_news()
            logging.info("User fetched news.")
        elif choice == '2':
            print("Logging out...")
            logging.info("User logged out.")
            break
        elif choice == '3':  
            delete_user(users)
            logging.info("User deleted account.")
        else:
            print("Invalid choice. Please try again.")
            logging.warning("Invalid choice during user session.")

def main_menu():
    users = load_users()
    while True:
        print("\n--- Welcome to News App ---")
        print("1. Login")
        print("2. Reset Password")
        print("3. Register New User")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            if login(users):
                logging.info("User logged in.")
                user_session(users)  
            else:
                logging.warning("Failed login attempt.")
        elif choice == '2':
            reset_password(users)
        elif choice == '3':
            add_new_user(users)
            logging.info("New user registered.")
        elif choice == '4':
            print("Exiting application.")
            logging.info("Application exited.")
            break
        else:
            print("Invalid choice. Please try again.")
            logging.warning("Invalid choice in main menu.")

if __name__ == '__main__':
    main_menu()
