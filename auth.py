import bcrypt
import csv
import re
import getpass
from captcha import verify_captcha
from password import reset_password  # Import the reset_password function

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def load_users():
    users = {}
    try:
        with open('userdata.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['email']] = row
        return users
    except FileNotFoundError:
        print("User file not found, starting with no users.")
        return users

def save_users(users):
    with open('userdata.csv', mode='w', newline='') as file:
        fieldnames = ['email', 'password', 'security_question', 'security_answer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

def add_new_user(users):
    email = input("Enter your email: ")
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        print("Invalid email format.")
        return
    if email in users:
        print("Email is already registered.")
        return

    password = getpass.getpass("Enter a password (at least 8 characters and 1 special character): ")
    if len(password) < 8 or not re.search(r'[!@#$%^&*]', password):
        print("Password does not meet the criteria.")
        return

    security_question = input("Enter a security question for password recovery: ")
    security_answer = getpass.getpass("Enter the answer to your security question: ")

    users[email] = {
        'email': email,
        'password': hash_password(password).decode('utf-8'),
        'security_question': security_question,
        'security_answer': hash_password(security_answer).decode('utf-8')
    }

    save_users(users)
    print("New user registered successfully!")

def delete_user(users):
    email = input("Enter your registered email to delete your account: ")
    if email not in users:
        print("Email not found.")
        return
    
    confirmation = input("Are you sure you want to delete your account? This action cannot be undone. (y/n): ")
    if confirmation.lower() == 'y':
        del users[email]
        save_users(users)
        print("Account deleted successfully.")
    else:
        print("Account deletion canceled.")

def login(users):
    email = input("Enter email: ")
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        print("Invalid email format.")
        return False
    if email not in users:
        print("Email not registered.")
        return False

    if not verify_captcha():
        print("Incorrect CAPTCHA. Please try again.")
        return False

    for attempt in range(5):
        password = getpass.getpass("Enter password: ")
        if check_password(users[email]['password'], password):
            print("Login successful!")
            return True
        else:
            print(f"Incorrect password. Attempts remaining: {4 - attempt}")
            if attempt < 4:  # Prompt to reset password if not the last attempt
                reset_choice = input("Would you like to reset your password? (y/n): ")
                if reset_choice.lower() == 'y':
                    reset_password(users)
                    return False  # Exit after resetting

    print("Too many failed attempts.")
    return False
