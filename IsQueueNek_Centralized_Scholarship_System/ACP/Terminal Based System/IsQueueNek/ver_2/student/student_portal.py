from config import STUDENT_DB_PATH, PROVIDER_DB_PATH
from database import load_db, save_db
from utils.id_generator import generate_student_id
from utils.security import hash_input, verify_input
from utils.validators import get_valid_int, get_valid_float, get_current_date

def student_menu():
    while True:
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("STUDENT PORTAL".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Login")
        print("[2] Register")
        print("[0] Go Back")

        user_choice = get_valid_int("Enter choice: ")
        if 0 <= user_choice and user_choice <= 2:
            if user_choice == 0:
                break
            elif user_choice == 1:
                student_login()
            else:
                student_registration()
        else:
                print("Please enter only between 0 - 2.")

def student_login():
    while True:
        MENU_WIDTH = 50
        print("-" * MENU_WIDTH)
        print("STUDENT LOGIN".center(MENU_WIDTH))
        print("-" * MENU_WIDTH)

        student_id = input("Student ID: ")
        student_password = input("Password: ").strip()
        students_db = load_db(STUDENT_DB_PATH)

        if student_id in students_db:
            stored_password = students_db[student_id]["password"]
            if verify_input(stored_password, student_password):
                print(f"Login successful! Welcome, {students_db[student_id]['name']}")
                student_dashboard(student_id)
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
            print("Wrong Student ID. Please try again.")
            user_choice = get_valid_int("[0] to exit. [1] to continue: ")
            if 0 <= user_choice and user_choice <= 1:
                if user_choice == 0:
                    break
                else:
                    continue
            else:
                print("Please enter only 0 or 1.")

def student_registration():
    MENU_WIDTH = 50
    print("-" * MENU_WIDTH)
    print("STUDENT REGISTRATION".center(MENU_WIDTH))
    print("-" * MENU_WIDTH)

    print("\nPlease enter your details carefully. This Master Profile will be used to automatically check your eligibility for all future scholarships!")

    student_data = {
        "name": input("Name: "),
        "age": get_valid_int("Age: "),
        "gwa": get_valid_float("GWA Last Semester: "),
        "annual_family_income": get_valid_int("Family Annual Income: "),
        "address": input("Address: ")
    }

    students_db = load_db(STUDENT_DB_PATH)

    student_id = generate_student_id(students_db)

    print(f"[System] Your Student ID is: {student_id}")
    print("[!] Please save this ID. You will use it to log in.")
    password = hash_input(input("Enter password: ").strip())

    student_data["student_id"] = student_id
    student_data["password"] = password

    students_db[student_id] = student_data
    save_db(students_db, STUDENT_DB_PATH)

    print("[System] Registration successful!")

def student_dashboard(student_id):
    while True: 
        MENU_WIDTH = 70
        print("=" * MENU_WIDTH)
        print("STUDENT DASHBOARD".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)

        students_db = load_db(STUDENT_DB_PATH)
        student = students_db[student_id]

        print(f"Welcome, {student['name']}!")
        print("-" * MENU_WIDTH)
        print("[1] View and Apply Scholarship")
        print("[2] View My Profile")
        print("[0] Go Back")
        
        user_choice = get_valid_int("Enter choice: ")
        if 0 <= user_choice and user_choice <= 2:
            if user_choice == 0:
                break
            elif user_choice == 1:
                view_and_apply_scholarships(student_id)
            else:
                view_profile(student_id)
        else:
            print("Please enter only between 0 - 2.")     

def view_and_apply_scholarships(student_id):
    students_db = load_db(STUDENT_DB_PATH)
    student = students_db[student_id]
    student_gwa = student["gwa"]
    student_income = student["annual_family_income"]
    student_location = student["address"]

    providers_db = load_db(PROVIDER_DB_PATH)

    MENU_WIDTH = 50
    print("=" * MENU_WIDTH)
    print("AVAILABLE SCHOLARSHIPS".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)
    print("[System] Auto-filtering based on your Master Profile:")
    print(f"[System] Your GWA: {student_gwa} | Income: PHP {student_income} | Location: {student_location}")
    print("-" * MENU_WIDTH)

    print()
    available_scholarships = {}
    schl_counter = 1

    for provider_id, provider_data in providers_db.items():
        for schl_id, schl_data in provider_data.get("scholarships", {}).items():
            current_date = get_current_date()
            if schl_data["slots"] <= 0 or schl_data["deadline"] <= current_date:
                continue
            provider = provider_data["organization_name"]
            schl_loc = schl_data["location"]
            schl_req_gwa = schl_data["min_gwa"]
            schl_req_income = schl_data["max_income"]

            location_match = (schl_loc.lower() == "any" or 
                            student_location.lower() in schl_loc.lower() or
                            schl_loc.lower() in student_location.lower() or
                            schl_loc.lower() == "philippines")
                
            qualifies = (student_gwa <= schl_req_gwa and student_income <= schl_req_income)

            if qualifies and location_match: 
                available_scholarships[str(schl_counter)] = {
                    "provider_name": provider,
                    "provider_id": provider_id,
                    "schl_id": schl_id,
                    "schl_data": schl_data
                }
                schl_counter += 1

    if not available_scholarships:
        print("\nThere are no scholarships available for your profile at the moment.")
        return

    for choice_num, schl_info in available_scholarships.items():
        data = available_scholarships[choice_num]["schl_data"]
        print(f"[{choice_num}] Scholarship: {data['scholarship_name']}")
        print(f"Provider: {schl_info['provider_name']}")
        print(f"Location: {data['location']}")
        print(f"Grant Amount: PHP {data['grant_amount']}")
        print(f"Requirements: Max Income: PHP {data['max_income']} | Min GWA: {data['min_gwa']:.2f}")
        print(f"Slots Remaining: {data['slots']}")
        print(f"Deadline: {data['deadline']}")
        print("-" * MENU_WIDTH)

    while True:
        user_choice = str(get_valid_int("\n[Enter the number of the scholarship to apply, or 0 to go back] Enter choice: "))

        if user_choice == "0":
            return

        if user_choice not in available_scholarships:
            print("[!] Invalid choice. Please try again.")
            continue

        selected_schl = available_scholarships[user_choice]
        prov_id = selected_schl["provider_id"]
        schl_id = selected_schl["schl_id"]

        if "applications" not in student:
            student["applications"] = []
        
        application_ref = f"{prov_id}_{schl_id}"

        if application_ref in student["applications"]:
            print(f"\n[!] You have already applied for this scholarship. Please choose again.")
            continue
        
        student["applications"].append(application_ref)

        schl_entry = providers_db[prov_id]["scholarships"][schl_id]

        if "applicants" not in schl_entry:
            schl_entry["applicants"] = {} 

        schl_entry["applicants"][student_id] = "pending"

        save_db(students_db, STUDENT_DB_PATH)
        save_db(providers_db, PROVIDER_DB_PATH)

        print(f"\n[*] Success! You have applied to {selected_schl['schl_data']['scholarship_name']}.")
        break

def view_profile(student_id):
    MENU_WIDTH = 50
    print("=" * MENU_WIDTH)
    print("STUDENT PROFILE".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    students_db = load_db(STUDENT_DB_PATH)
    providers_db = load_db(PROVIDER_DB_PATH)
    student = students_db[student_id]

    print(f"Student ID: {student_id}")
    print(f"Name: {student['name']}") 
    print(f"Age: {student['age']} yrs old")
    print(f"GWA: {student['gwa']}")
    print(f"Annual Income: {student['annual_family_income']}")
    print("=" * MENU_WIDTH)

    print()

    print("=" * MENU_WIDTH)
    print("MY SCHOLARSHIP APPLICATIONS".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    applications = student.get("applications", [])

    if not applications:
        print("You have not applied to any scholarships yet.")
        print("-" * MENU_WIDTH)

    else:
        for i, app_ref in enumerate(applications, start=1):
            ids = app_ref.split('_')
            prov_id = ids[0]
            sch_id = ids[1]
            provider = providers_db[prov_id]
            
            status = provider['scholarships'][sch_id]['applicants'][student_id].upper()

            print(f"[{i}] {provider['scholarships'][sch_id]['scholarship_name']}")
            print(f"Provider: {provider['organization_name']}")
            print(f"Deadline: {provider['scholarships'][sch_id]['deadline']}")
            print(f"Status: {status}") 
            print()
            
    print("=" * MENU_WIDTH)
    print(f"Total Applications: {len(applications)}") 
    print("=" * MENU_WIDTH)     

    while True:
        choice = get_valid_int("\nEnter [0] to go back to Dashboard: ")   
        if choice == 0:
            break
        else:
            print("[!] Please enter 0 to go back.")