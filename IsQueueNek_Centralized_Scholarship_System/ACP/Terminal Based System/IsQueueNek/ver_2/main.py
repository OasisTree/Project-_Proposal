from admin.admin_portal import admin_login
from provider.provider_portal import provider_menu
from student.student_portal import student_menu
from utils.validators import get_valid_int

def main_menu():
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("WELCOME TO ISQUEUENEK".center(MENU_WIDTH))
        print("Automated Scholarship Processing System".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        
        print("[1] Student Portal")
        print("[2] Scholarship Provider Portal")
        print("[3] System Administrator")
        print("[0] Exit Application")
        print("-" * MENU_WIDTH)

        choice = get_valid_int("Please select your role: ")

        if choice == 1:
            print("\nRedirecting to Student Portal...")
            student_menu()  
        elif choice == 2:
            print("\nRedirecting to Provider Portal...")
            provider_menu()
        elif choice == 3:
            print("\nRedirecting to Admin Portal...")
            admin_login()
        elif choice == 0:
            print("\n[System] Shutting down IsQueueNek. Have a great day!")
            break
        else:
            print("\n[!] Invalid choice. Please select a number between 0 and 3.")

if __name__ == "__main__":
    main_menu()