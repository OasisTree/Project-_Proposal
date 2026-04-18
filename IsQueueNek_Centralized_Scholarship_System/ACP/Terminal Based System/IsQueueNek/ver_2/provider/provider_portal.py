from config import STUDENT_DB_PATH, PROVIDER_DB_PATH
from database import load_db, save_db
from utils.id_generator import generate_scholarship_id, generate_provider_id
from utils.security import hash_input, verify_input
from utils.validators import get_valid_int, get_valid_float

def provider_menu():
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER PORTAL".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Login")
        print("[2] Register as Provider")
        print("[0] Go Back")

        user_choice = get_valid_int("Enter choice: ")
        if 0 <= user_choice and user_choice <= 2:
            if user_choice == 0:
                break
            elif user_choice == 1:
                provider_login()
            else:
                provider_registration()
        else:
            print("Please enter only between 0 - 2.")

def provider_login():
    while True:
        MENU_WIDTH = 50
        print("-" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER LOGIN".center(MENU_WIDTH))
        print("-" * MENU_WIDTH)

        provider_id = input("Provider ID: ")
        provider_password = input("Password: ").strip()
        providers_db = load_db(PROVIDER_DB_PATH)
                
        if provider_id in providers_db:
            status = providers_db[provider_id]["status"]
            stored_password = providers_db[provider_id]["password"]
            if status == "approved":
                if verify_input(stored_password, provider_password):
                    print(f"Login successful! Welcome, {providers_db[provider_id]["organization_name"]}")
                    provider_dashboard(provider_id)
                    break
                else:
                    print("Wrong password. Please try again.")
                    user_choice = get_valid_int("[0] to exit. [1] to continue: ")
                    if 0 <= user_choice and user_choice <= 1:
                        if user_choice == 0:
                            break
                        else:
                            continue          
                    else:
                        print("Please enter only 0 or 1.")
            else:
                print("[!] Access Denied: Your account is still waiting for Admin approval. Please try again later.")
                user_choice = get_valid_int("[0] to exit. [1] to continue: ")
                if 0 <= user_choice and user_choice <= 1:
                    if user_choice == 0:
                        break
                    else:
                        continue          
                else:
                    print("Please enter only 0 or 1.")                    
        else:
            print("Wrong Provider ID. Please try again.")
            user_choice = get_valid_int("[0] to exit. [1] to continue: ")
            if 0 <= user_choice and user_choice <= 1:
                if user_choice == 0:
                    break
                else:
                    continue
            else:
                print("Please enter only 0 or 1.")

def provider_registration():
    MENU_WIDTH = 50
    print("-" * MENU_WIDTH)
    print("SCHOLARSHIP PROVIDER REGISTRATION".center(MENU_WIDTH))
    print("-" * MENU_WIDTH)

    providers_data = {
        "organization_name": input("Organization name: "),
        "email": input("Email: "),
        "contact_number": input("Contact number: "),
        "office_address": input("Office addres: "),
        "website": input("Website: ")
    }

    providers_db = load_db(PROVIDER_DB_PATH)

    provider_id = generate_provider_id(providers_db)
    print(f"[System] Your Provider ID is: {provider_id}. Please don't forget your id as you will use it to login.")
    password = hash_input(input("Enter password: "))

    providers_data["provider_id"] = provider_id
    providers_data["password"] = password
    providers_data["status"] = "pending"

    providers_db[provider_id] = providers_data
    save_db(providers_db, PROVIDER_DB_PATH)

    print("[System] Registration successful!")
    print("[!] Please note: Your account is currently PENDING. You must wait for Admin approval before logging in.")

def provider_dashboard(provider_id):
    while True: 
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER DASHBOARD".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)

        providers_db = load_db(PROVIDER_DB_PATH)
        provider = providers_db[provider_id]

        print(f"Welcome, {provider['organization_name']}!")
        print("-" * MENU_WIDTH)
        print("[1] Create Scholarship")
        print("[2] View and Assess Applicants")
        print("[0] Go Back")
        
        user_choice = get_valid_int("Enter choice: ")
        if 0 <= user_choice and user_choice <= 2:
            if user_choice == 0:
                break
            elif user_choice == 1:
                post_scholarship(provider_id)
            else:
                view_and_assess_applicants_menu(provider_id)
        else:
            print("Please enter only between 0 - 2.")        

def post_scholarship(provider_id):
    MENU_WIDTH = 50
    print("=" * MENU_WIDTH)
    print("CREATE SCHOLARSHIP".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    scholarship_info = {
        "scholarship_name": input("Scholarship Name: "),
        "description": input("Description: "),
        "location": input('Location (or "Any"): '),
        "min_gwa": get_valid_float("Minimum GWA requied: "),
        "max_income": get_valid_int("Maximum Family Income (PHP): "),
        "grant_amount": get_valid_int("Grant Amount (PHP): "),
        "slots": get_valid_int("Number of Slots available: "), 
        "deadline": input("Deadline (YYYY-MM-DD): ") 
    }
    
    providers_db = load_db(PROVIDER_DB_PATH)
    provider_data = providers_db[provider_id]
    
    if "scholarships" not in provider_data:
        provider_data["scholarships"] = {}

    scholarship_id = generate_scholarship_id(provider_data)
    provider_data["scholarships"][scholarship_id] = scholarship_info

    save_db(providers_db, PROVIDER_DB_PATH)

    print("[System] Scholarship created successfully!")
    print(f"[System] Scholarship ID: {scholarship_id} has been posted.")

def view_and_assess_applicants_menu(provider_id):
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("SCHOLARSHIP APPLICANTS".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] View Approved Applicants")
        print("[2] Assess New Applicants")
        print("[0] Go Back")

        user_choice = get_valid_int("Enter choice: ")
        if 0 <= user_choice and user_choice <= 2:
            if user_choice == 0:
                break
            elif user_choice == 1:
                view_approved_applicants(provider_id)
            else:
                assess_new_applicants(provider_id)
        else:
            print("Please enter only between 0 - 2.") 

def view_approved_applicants(provider_id):
    MENU_WIDTH = 50
    print("=" * MENU_WIDTH)
    print("APPROVED APPLICANTS".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    students_db = load_db(STUDENT_DB_PATH)
    providers_db = load_db(PROVIDER_DB_PATH)
    provider = providers_db[provider_id]
    
    if "scholarships" not in provider:
        print("You have no scholarships yet. Go create one!")
        return
    else:
        for schl_id, schl_data in provider["scholarships"].items():
            if "applicants" not in schl_data:
                print("No one has applied for this scholarship yet.")
                continue
            else:
                print()
                applicant_counter = 1
                print(f"[ Scholarship: {schl_data["scholarship_name"]} | ID: {schl_id}]")
                for applicant, status in schl_data["applicants"].items():
                    if status == "approved":
                        student = students_db[applicant]
                        print(f"Applicant {applicant_counter}:")
                        print(f"Student ID: {applicant}")
                        print(f"Name: {student['name']}")
                        print(f"Age: {student['age']}")
                        print(f"GWA: {student['gwa']}")
                        print(f"Annual Income: {student['annual_family_income']}")
                        print()
                        applicant_counter += 1
                    else:
                        continue
                print(f"\nSlots left: {schl_data['slots']}")

def assess_new_applicants(provider_id):
    while True:
        MENU_WIDTH = 50
        print("=" * MENU_WIDTH)
        print("ASSESS NEW APPLICANTS".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)

        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)
        provider = providers_db[provider_id]

        if "scholarships" not in provider:
            print("You have no scholarships yet. Go create one!")
            return

        any_pending_global = False

        for schl_id, schl_data in provider["scholarships"].items():
            print(f"\n[ Scholarship: {schl_data['scholarship_name']} | ID: {schl_id}]")

            if "applicants" not in schl_data:
                print("No one has applied for this scholarship yet.")
                continue

            applicant_counter = 1
            pending_found = False

            for applicant, status in schl_data["applicants"].items():

                if schl_data["slots"] <= 0:
                    print("No slots left.")
                    break

                if status == "pending":
                    pending_found = True
                    any_pending_global = True

                    student = students_db[applicant]

                    print(f"\nApplicant {applicant_counter}:")
                    print(f"Student ID: {applicant}")
                    print(f"Name: {student['name']}")
                    print(f"Age: {student['age']}")
                    print(f"GWA: {student['gwa']}")
                    print(f"Annual Income: {student['annual_family_income']}")

                    applicant_counter += 1

                    # decision
                    while True:
                        action = input("Action - [A]pprove or [R]eject: ").strip().upper()
                        if action in ["A", "R"]:
                            break
                        print("Please enter only A or R.")

                    if action == "A":
                        schl_data["applicants"][applicant] = "approved"
                        schl_data["slots"] -= 1
                        print("[*] Applicant Approved!")
                        print(f"Slots left: {schl_data['slots']}")
                    else:
                        schl_data["applicants"][applicant] = "rejected"
                        print("[*] Applicant Rejected!")

                    while True:
                        choice = get_valid_int("[0] Exit | [1] Continue: ")
                        if choice == 0:
                            save_db(providers_db, PROVIDER_DB_PATH)
                            return
                        elif choice == 1:
                            break
                        else:
                            print("Please enter only 0 or 1.")

            if not pending_found:
                print("No pending applicants to review for this scholarship.")

        if not any_pending_global:
            return

        save_db(providers_db, PROVIDER_DB_PATH)
        print("\n[System] Assessment cycle complete and saved.")

        while True:
            choice = get_valid_int("[0] Exit | [1] Refresh: ")
            if choice == 0:
                return
            elif choice == 1:
                break
            else:
                print("Please enter only 0 or 1.")