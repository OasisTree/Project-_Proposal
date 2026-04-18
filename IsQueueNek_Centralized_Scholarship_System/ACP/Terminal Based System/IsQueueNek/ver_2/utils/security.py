import hashlib

# This ensures that the password is encrypted in the database and to prevent attackers from reading user credentials if a database is compromised
def hash_input(input):
    return hashlib.sha256(input.encode()).hexdigest()

# Checks if the provided password matches the stored hash password
def verify_input(stored_hash, provided_input):
    return stored_hash == hash_input(provided_input)
    