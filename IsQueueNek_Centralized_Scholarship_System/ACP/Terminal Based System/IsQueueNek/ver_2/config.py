import os

# Gets the path where config.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Gets the path where each database lives
STUDENT_DB_PATH = os.path.join(BASE_DIR, 'data', 'students.json')
PROVIDER_DB_PATH = os.path.join(BASE_DIR, 'data', 'providers.json')
ADMIN_DB_PATH = os.path.join(BASE_DIR, 'data', 'admin.json')