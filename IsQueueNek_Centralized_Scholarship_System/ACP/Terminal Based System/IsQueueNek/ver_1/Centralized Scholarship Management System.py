import datetime
import json
import os

STUDENT_DB_FILE = "students_database.json"
SCHOLARSHIP_PROVIDER_DB_FILE = "scholarship_providers_database.json"

def load_db(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return json.load(file)
    
def save_db(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

students_db = load_db(STUDENT_DB_FILE)
scholarship_providers_db = load_db(SCHOLARSHIP_PROVIDER_DB_FILE)
#------------------------------------------------------#
#MAIN MENU#
#------------------------------------------------------#
def main_menu():
    MENU_WIDTH = 70
    while True:
        print("=" * MENU_WIDTH)
        print("ISQUEUENEK: CENTRALIZED SCHOLARSHIP MANAGEMENT SYSTEM".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Student Login/Register")
        print("[2] Scholarship Provider Login/Register")
        print("[3] Exit")
        print("=" * MENU_WIDTH)
        try:
            user_choice = int(input("Enter choice: "))
            match user_choice:
                case 1:
                    student_menu()
                case 2:
                    scholarship_provider_menu()
                case 3:
                    print("Exiting Program....")
                    break
                case _:
                    print("\n[!] Invalid choice. Please input a number between 1 and 3.\n")
        except ValueError:
            print("\n[!] Invalid input. Please enter a numerical value (1-3).\n")

#------------------------------------------------------#
#STUDENT MODULE#
#------------------------------------------------------#   
def student_menu():
    MENU_WIDTH = 60
    while True:
        print("=" * MENU_WIDTH)
        print("STUDENT MENU".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Login")
        print("[2] Register")
        print("[3] Back to Main Menu")
        print("=" * MENU_WIDTH)
        try:
            user_choice = int(input("Enter choice: "))
            match user_choice:
                case 1:
                    student_login()
                case 2:
                    student_registration()
                case 3:
                    print("Returning to main menu....")
                    break
                case _:
                    print("\n[!] Invalid choice. Please input a number between 1 and 3.\n")
        except ValueError:
            print("\n[!] Invalid input. Please enter a numerical value (1-3).\n")

def student_login():
    MENU_WIDTH = 50
    while True:
        print("-" * MENU_WIDTH)
        print("STUDENT LOGIN".center(MENU_WIDTH))
        print("-" * MENU_WIDTH)

        student_id = input("Enter Student ID: ")
        password = input("Enter Password: ")

        if student_id in students_db:
            if students_db[student_id]["password"] == password:
                print("Login successfull")
                student_dashboard(student_id)
                break
            else:
                print("Incorrect password.")
        else:
            print("Student ID not found.")
        

def student_registration():
    MENU_WIDTH = 50
    while True:
        print("-" * MENU_WIDTH)
        print("STUDENT REGISTRATION".center(MENU_WIDTH))
        print("Please enter your details to create your Master Profile:")
        student_profile = {
            "name": input("Name: "),
            "age": int(input("Age: ")),
            "gwa": float(input("GWA: ")),
            "annual_income": int(input("Annual Family Income: ")),
            "address": input("Address / City of Residence: ")
        }
        print("-" * MENU_WIDTH)

        student_id = generate_student_id(students_db)             
        student_profile["student_id"] = student_id
        
        print(f"\nYour Unique Student ID is: {student_id}")
        print("Kindly remember your student ID for login.")

        password = input("Enter a password: ")
        student_profile["password"] = password

        students_db[student_id] = student_profile
        save_db(students_db, STUDENT_DB_FILE)

        print()
        print("\nStudent profile successfully created! You can login now.")
        print("-" * MENU_WIDTH)
        break

def generate_student_id(database):
    current_year = datetime.date.today().strftime("%y")
    count = len(database) + 1
    return f"{current_year}-{count:05d}"
    
def student_dashboard(student_id):
    MENU_WIDTH = 60
    while True:
        print("=" * MENU_WIDTH)
        print("STUDENT DASHBOARD".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print(f"Welcome, {students_db[student_id]["name"]}!")
        print("[1] View and Apply to Available Scholarships")
        print("[2] My Profile and Applications")
        print("[3] Logout")
        print("=" * MENU_WIDTH)
        try:
            user_choice = int(input("Enter choice: "))
            match user_choice:
                case 1:
                    view_and_apply_scholarships(student_id)
                case 2:
                    view_profile_and_applications(student_id)
                case 3:
                    print("Returning to student menu....")
                    break
                case _:
                    print("\n[!] Invalid choice. Please input a number between 1 and 3.\n")
        except ValueError:
            print("\n[!] Invalid input. Please enter a numerical value (1-3).\n")    

def view_and_apply_scholarships(student_id):
    MENU_WIDTH = 60
    student = students_db[student_id]
    student_gwa = student.get("gwa", 5.0)
    student_address = student.get("address", "").lower().strip()
    student_annual_income = student.get("annual_income", 9999999999999999)


    print("=" * MENU_WIDTH)
    print("AVAILABLE SCHOLARSHIPS".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    available_scholarships = {}
    scholarship_counter = 1

    for provider_id, provider_data in scholarship_providers_db.items():
        scholarships = provider_data.get("scholarships", {})
        for schl_id, schl_data in scholarships.items():
            schl_location = schl_data.get("location", "").lower().strip()
            schl_req_gwa = schl_data.get("min_gwa", 1.0)
            schl_req_income = schl_data.get("max_income", 0)

            location_match = (schl_location == "philippines" or
                              schl_location == "any" or
                              schl_location in student_address)
            
            qualifies = (student_annual_income <= schl_req_income) and (student_gwa <= schl_req_gwa)

            if location_match and qualifies:
                available_scholarships[str(scholarship_counter)] = {
                    "provider_name": provider_data.get("organization_name", "Unknown Provider"),
                    "provider_id": provider_id,
                    "schl_id": schl_id,
                    "schl_data": schl_data
                }
                scholarship_counter += 1            

    if not available_scholarships:
        print("\nThere are no scholarships available for your profile at the moment.")
        return

    for choice_num, schl_info in available_scholarships.items():
        data = available_scholarships[choice_num]["schl_data"]
        print(f"[{choice_num}] {data['scholarship_name']}")
        print(f"Provider: {schl_info['provider_name']}")
        print(f"Location: {data['location']}")
        print(f"Grant Amount: PHP{data['grant_amount']}")
        print(f"Requirements: Min GWA: {data['min_gwa']:.2f} | Max Family Annual Income: {data['max_income']}")
        print(f"Slots/Deadline: | {data['deadline']}")
        print("-" * MENU_WIDTH)
    
    print("[Enter 'B to go back to Dashboard]")
    print("-" * MENU_WIDTH)
    
    
    while True:
        choice = input("Enter the number of the Scholarship to apply: ").upper().strip()

        if choice == 'B':
            return

        elif choice not in available_scholarships:
            print("[!] Invalid choice. Please try again.")
            continue

        if choice in available_scholarships:
            selected_schl = available_scholarships[choice]
            prov_id = selected_schl["provider_id"]
            schl_id = selected_schl["schl_id"]

        if "applications" not in student:
            student["applications"] = []
        
        application_ref = f"{prov_id}_{schl_id}"

        if application_ref in student["applications"]:
            print(f"\n[!] You have already applied for this scholarship. Please choose again.")
            continue
        
        student["applications"].append(application_ref)

        schl_entry = scholarship_providers_db[prov_id]["scholarships"][schl_id]
        if "applications" not in schl_entry:
            schl_entry["applications"] = []
        schl_entry["applications"].append(student_id)

        save_db(students_db, STUDENT_DB_FILE)
        save_db(scholarship_providers_db, SCHOLARSHIP_PROVIDER_DB_FILE)

        print(f"\nSuccess! You have applied to {selected_schl['schl_data']['scholarship_name']}.")
        break

def view_profile_and_applications(student_id):
    MENU_WIDTH = 60
    
    print("=" * MENU_WIDTH)
    print("STUDENT PROFILE".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    student = students_db[student_id]
    print(f"Student ID: {student_id}")
    print(f"Name: {student["name"]}")
    print(f"Age: {student["age"]} yrs old")
    print(f"GWA: {student['gwa']}")
    print(f"Annual Income: {student['annual_income']}")
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
        schl_counter = 1
        for app_ref in applications:
            ids = app_ref.split('_')
            prov_id = ids[0]
            sch_id = ids[1]
            provider = scholarship_providers_db[prov_id]

            print(f"[{schl_counter}] {provider['scholarships'][sch_id]['scholarship_name']}")
            print(f"Provider: {provider['organization_name']}")
            print(f"Deadline: {provider['scholarships'][sch_id]['deadline']}")
            print()
            schl_counter += 1
    print("=" * MENU_WIDTH)
    print(f"Total Applications: {schl_counter}")
    print("=" * MENU_WIDTH)     

    choice = int(input("[1] Back to Dashboard"))   
    if choice == 1:
        return

#------------------------------------------------------#
#SCHOLARSHIP PROVIDER MODULE#
#------------------------------------------------------#   
def scholarship_provider_menu():
    MENU_WIDTH = 60
    while True:
        print("=" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER MENU".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print("[1] Login")
        print("[2] Register")
        print("[3] Back to Main Menu")
        print("=" * MENU_WIDTH)
        try:
            user_choice = int(input("Enter choice: "))
            match user_choice:
                case 1:
                    scholarship_provider_login()
                case 2:
                    scholarship_provider_register()
                case 3:
                    print("Returning to main menu....")
                    break
                case _:
                    print("\n[!] Invalid choice. Please input a number between 1 and 3.\n")
        except ValueError:
            print("\n[!] Invalid input. Please enter a numerical value (1-3).\n")

def scholarship_provider_login():
    MENU_WIDTH = 50
    while True:
        print("-" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER LOGIN".center(MENU_WIDTH))
        print("-" * MENU_WIDTH)

        scholarship_provider_id = input("Enter Provider ID: ")
        password = input("Enter Password: ")

        if scholarship_provider_id in scholarship_providers_db:
            if scholarship_providers_db[scholarship_provider_id]["password"] == password:
                print("Login successfull!")
                scholarship_provider_dashboard(scholarship_provider_id)
                break
            else:
                print("Incorrect password.")
        else:
            print("Provider ID not found.")

def scholarship_provider_register():
    MENU_WIDTH = 50
    while True:
        print("-" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER REGISTRATION".center(MENU_WIDTH))
        print("Please enter your organization details:")
        scholarship_provider_profile = {
            "organization_name": input("Organization Name: "),
            "email": input("Email: "),
            "contact_number": input("Contact Number: "),
            "office_address": input("Office Address: "),
            "website": input("Website: ")
        }
        print("-" * MENU_WIDTH)

        scholarship_provider_id = generate_scholarship_provider_id(scholarship_providers_db)             
        scholarship_provider_profile["scholarship_provider_id"] = scholarship_provider_id
        
        print(f"\nYour Provider ID is: {scholarship_provider_id}")
        print("Please save this ID for login.")

        password = input("Enter a password: ")
        scholarship_provider_profile["password"] = password

        scholarship_providers_db[scholarship_provider_id] = scholarship_provider_profile
        save_db(scholarship_providers_db, SCHOLARSHIP_PROVIDER_DB_FILE)

        print()
        print("\nRegistration Successful! You can now log in.")
        print("-" * MENU_WIDTH)        
        break

def generate_scholarship_provider_id(scholarship_provider_db):
    count = len(scholarship_provider_db) + 1
    return f"PROV-{count:05d}"

def scholarship_provider_dashboard(scholarship_provider_id):
    MENU_WIDTH = 60
    while True:
        print("=" * MENU_WIDTH)
        print("SCHOLARSHIP PROVIDER DASHBOARD".center(MENU_WIDTH))
        print("=" * MENU_WIDTH)
        print(f"Welcome, {scholarship_providers_db[scholarship_provider_id]["organization_name"]}!")
        print("[1] Create Scholarship")
        print("[2] View Applicants")
        print("[3] Logout")
        print("=" * MENU_WIDTH)
        try:
            user_choice = int(input("Enter choice: "))
            match user_choice:
                case 1:
                    create_scholarship(scholarship_provider_id)
                case 2:
                    view_applicants(scholarship_provider_id)
                case 3:
                    print("Returning to scholarship provider menu....")
                    break
                case _:
                    print("\n[!] Invalid choice. Please input a number between 1 and 3.\n")
        except ValueError:
            print("\n[!] Invalid input. Please enter a numerical value (1-3).\n")

def create_scholarship(scholarship_provider_id):
    MENU_WIDTH = 60
    
    provider = scholarship_providers_db[scholarship_provider_id]

    if "scholarships" not in provider:
        provider["scholarships"] = {}

    print("-" * MENU_WIDTH)
    print("CREATE SCHOLARSHIP".center(MENU_WIDTH))
    print("-" * MENU_WIDTH)

    scholarships = {
        "scholarship_name": input("Scholarship Name: "),
        "description": input("Description: "),
        "min_gwa": float(input("Minimum GWA: ")),
        "max_income": int(input("Maximum Annual Income: ")),
        "location": input("Location (or Any): "),
        "grant_amount": int(input("Grant Amount: ")),
        "slots": int(input("Number of Slots: ")),
        "deadline": input("Deadline (YYYY-MM-DD): ")
    }

    scholarship_id = generate_scholarship_id(provider)
    provider["scholarships"][scholarship_id] = scholarships

    save_db(scholarship_providers_db, SCHOLARSHIP_PROVIDER_DB_FILE)

    print(f"\nScholarship {scholarship_id} created successfully!")
    print("-" * MENU_WIDTH)

def generate_scholarship_id(provider_data):
    count = len(provider_data.get("scholarships", {})) + 1
    return f"SCH-{count:05d}"

def view_applicants(scholarship_provider_id):
    MENU_WIDTH = 60

    print("=" * MENU_WIDTH)
    print("SCHOLARSHIP APPLICANTS DASHBOARD".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)

    provider = scholarship_providers_db.get(scholarship_provider_id, {})
    print(f"Organization: {provider['organization_name']}")
    print(f"Provider ID: {scholarship_provider_id}")
    print("=" * MENU_WIDTH)

    scholarships = provider.get("scholarships", {})

    if not scholarships:
        print("\nYou have not created any scholarships yet.")
        return
    else:
        schl_counter =  1
        
        for schl_id, schl_data in scholarships.items():
            print(f"[{schl_counter}] {schl_data['scholarship_name']} ({schl_id})")
            print("-" * MENU_WIDTH)

            applicants = schl_data.get("applications", [])

            if not applicants:
                print("No one has applied for your scholarship yet.")

            else:
                stu_counter = 1
                for student_id in applicants:
                    student = students_db.get(student_id, {})
                    student = students_db.get(student_id, {})
                    print(f"  [{stu_counter}] Student ID: {student_id}")
                    print(f"      Name          : {student.get('name', 'N/A')}")
                    print(f"      Age           : {student.get('age', 'N/A')} yrs old")
                    print(f"      Address       : {student.get('address', 'N/A')}")
                    print(f"      GWA           : {student.get('gwa', 'N/A')}")
                    print(f"      Annual Income : PHP {student.get('annual_income', 'N/A')}")
                    print("      " + "-" * 40)
                    stu_counter += 1

    print("\n" + "=" * MENU_WIDTH)
    
    # Navigation loop
    while True:
        choice = input("[Enter 'B' to go back to Dashboard]: ").strip().upper()
        if choice == 'B':
            return
        else:
            print("[!] Invalid input. Please enter 'B'.")
            

if __name__ == "__main__":
    main_menu()