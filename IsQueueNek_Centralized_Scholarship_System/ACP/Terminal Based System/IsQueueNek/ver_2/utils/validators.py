import datetime
# Repeatedly asks the user to input a whole number or float like for getting age, gwa, etc.
def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a whole number.")

def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a number/decimal.")

def get_current_date():
    return datetime.date.today().strftime("%Y-%m-%d")