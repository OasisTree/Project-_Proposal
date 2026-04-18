import os

"""Centralized file paths for JSON databases."""

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file paths
STUDENT_DB_PATH = os.path.join(BASE_DIR, "data", "students.json")
PROVIDER_DB_PATH = os.path.join(BASE_DIR, "data", "providers.json")
ADMIN_DB_PATH = os.path.join(BASE_DIR, "data", "admin.json")
