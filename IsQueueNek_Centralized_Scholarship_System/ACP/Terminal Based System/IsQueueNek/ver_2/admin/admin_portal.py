from config import ADMIN_DB_PATH, PROVIDER_DB_PATH
from database import load_db, save_db
from utils.security  import hash_input, verify_input
from utils.validators import get_valid_int

admins_db = load_db(ADMIN_DB_PATH)

if not admins_db:
    MENU_WIDTH = 50
    print("-" * MENU_WIDTH)
    print("ADMIN REGISTRATION")
    print("-" * MENU_WIDTH)
    username = input("Enter username: ")
    password = input("Enter password: ")
    admins_db[hash_input(username)] = {
        "password": hash_input(password)
    }
    save_db(admins_db, ADMIN_DB_PATH)
    print("[System] Default admin account successfully created and saved.")
       
def admin_login():
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("ADMIN LOGIN".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        
        username = input("Username: ")
        password = input("Passsword: ")
        hashed_username_input = hash_input(username)
        
        if hashed_username_input in admins_db:
            stored_password = admins_db[hashed_username_input]["password"]
            if verify_input(stored_password, password): 
                print("Login Successful. Welcome, Administrator.")
                admin_dashboard()
                break
            else: 
                print("Wrong password. Please try again.")
                user_choice =  get_valid_int("[0] to exit. [1] to continue: ")
                if 0 <= user_choice and user_choice <= 1:
                    if user_choice == 0:
                        break
                    else:
                        continue
                else:
                    print("Please enter only 0 or 1.")
        else:
            print("Wrong username. Please try again.")
            user_choice =  get_valid_int("[0] to exit. [1] to continue: ")
            if 0 <= user_choice and user_choice <= 1:
                if user_choice == 0:
                    break
                else:
                    continue
            else:
                print("Please enter only 0 or 1.")

def admin_dashboard():
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("ADMIN DASHBOARD".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Review Pending Providers")
        print("[2] Logout")

        user_choice = get_valid_int("Enter choice: ")
        if 1 <= user_choice and user_choice <= 2:
            if user_choice == 1:
                review_pending_providers()
            else:
                break
        else:
            print("Please enter only 1 or 2.")

def review_pending_providers():
    MENU_WIDTH = 50
    print("-" * MENU_WIDTH)
    print("PENDING PROVIDERS".center(MENU_WIDTH))
    print("-" * MENU_WIDTH)

    providers_db = load_db(PROVIDER_DB_PATH)
    pending_found = False

    for prov_id, prov_data in providers_db.items():
        if prov_data.get("status") == "pending":
            pending_found = True
            provider = providers_db[prov_id]
            print(f"Provider ID: {prov_id}")
            print(f"Organization: {provider["organization_name"]}")
            print(f"Email: {provider["email"]}")
            user_choice = input(f"Action - [A]pprove, [R]eject, or [S]kip: ").upper()
            if user_choice == "A":
                provider["status"] = "approved"
                print(f"[*] {provider["organization_name"]} has been APPROVED.")
            elif user_choice == "R":
                provider["status"] = "rejected"
                print(f"[*] {provider["organization_name"]} has been REJECTED.")
            else:
                continue
        print()
    if pending_found == True:
        save_db(providers_db, PROVIDER_DB_PATH)
        print("[System] Database updated successfully.")
    else:
        print("[System] There are no pending providers to review at this time.")