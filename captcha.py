import random
import string

def generate_captcha():
    captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    print(f"CAPTCHA: {captcha}")
    return captcha

def verify_captcha():
    captcha = generate_captcha()
    user_input = input("Enter the CAPTCHA: ")
    return user_input == captcha
