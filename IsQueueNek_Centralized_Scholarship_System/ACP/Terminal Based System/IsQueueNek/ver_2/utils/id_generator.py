import datetime

# This generates an ID like: 26-00001
def generate_student_id(students_db):
    current_year = datetime.date.today().strftime("%y")
    count = len(students_db) + 1
    # :05d forces the number to be 5 digits long, filling empty space with zeros
    return f"{current_year}-{count:05d}"

# This generates an ID like: PROV-00001
def generate_provider_id(providers_db):
    count = len(providers_db) + 1
    return f"PROV-{count:05d}"

# This generates an ID like: SCH-00001
def generate_scholarship_id(provider_data):
    count = len(provider_data.get("scholarships", {})) + 1
    return f"SCH-{count:05d}"