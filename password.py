import getpass
import bcrypt
import csv
import re

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def reset_password(users):
    email = input("Enter your registered email: ")
    if email not in users:
        print("Email not found.")
        return

    security_answer = getpass.getpass("Enter the answer to your security question: ")
    if not bcrypt.checkpw(security_answer.encode('utf-8'), users[email]['security_answer'].encode('utf-8')):
        print("Incorrect answer.")
        return

    new_password = getpass.getpass("Enter a new password (at least 8 characters and 1 special character): ")
    if len(new_password) < 8 or not re.search(r'[!@#$%^&*]', new_password):
        print("Password does not meet the criteria.")
        return

    users[email]['password'] = hash_password(new_password)
    
    save_users(users)
    print("Password reset successfully!")

def save_users(users):
    with open('userdata.csv', mode='w', newline='') as file:
        fieldnames = ['email', 'password', 'security_question', 'security_answer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)
