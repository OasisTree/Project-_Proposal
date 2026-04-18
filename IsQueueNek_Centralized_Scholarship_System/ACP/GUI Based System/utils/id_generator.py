import datetime

"""ID generators for students, providers, and scholarships."""


def generate_student_id(students_db):
    """Generate sequential student ID."""
    year = datetime.date.today().strftime("%y")
    count = len(students_db) + 1
    return f"{year}-{count:05d}"


def generate_provider_id(providers_db):
    """Generate sequential provider ID."""
    count = len(providers_db) + 1
    return f"PROV-{count:05d}"


def generate_scholarship_id(provider_data):
    """Generate scholarship ID per provider."""
    count = len(provider_data.get("scholarships", {})) + 1
    return f"SCH-{count:05d}"
