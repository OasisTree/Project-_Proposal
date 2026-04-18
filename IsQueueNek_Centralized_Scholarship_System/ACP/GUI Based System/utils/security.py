import hashlib

"""Simple hashing utilities for secure input storage and verification."""


def hash_input(input_str):
    """Return SHA-256 hash of input string."""
    return hashlib.sha256(input_str.encode()).hexdigest()


def verify_input(stored_hash, provided_input):
    """Check if provided input matches stored hash."""
    return stored_hash == hash_input(provided_input)
