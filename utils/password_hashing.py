import bcrypt

# Function to hash a password
def hash_password(password):
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # Return the hashed password
    return hashed_password

# Function to verify a password
def verify_password(password, stored_hashed_password):
    # Verify the entered password with the stored hashed password
    return bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password)
