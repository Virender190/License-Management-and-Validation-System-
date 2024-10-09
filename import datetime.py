import datetime
import json
import hashlib
import os

# Secret key used for hashing, should be stored securely (e.g., in environment variables)
SECRET_KEY = "your_secure_secret_key"

# License duration in days (example: 365 days for 1 year)
LICENSE_DURATION = 365

# Ensure the licenses directory exists
if not os.path.exists("licenses"):
    os.makedirs("licenses")

# Function to generate a license key for a client
def generate_license(client_name, client_email):
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=LICENSE_DURATION)
    license_data = f"{client_name}|{client_email}|{expiry_date.strftime('%Y-%m-%d')}|{SECRET_KEY}"
    license_key = hashlib.sha256(license_data.encode()).hexdigest()
    
    # License details to be stored for reference
    license_details = {
        'client_name': client_name,
        'client_email': client_email,
        'expiry_date': expiry_date.strftime('%Y-%m-%d'),
        'license_key': license_key
    }

    # Save the license details to a JSON file (database substitute for this example)
    with open(f"licenses/{client_email}.json", "w") as file:
        json.dump(license_details, file)

    return license_key

# Function to validate a license
def validate_license(client_email, provided_license_key):
    try:
        # Load the stored license details from JSON file
        with open(f"licenses/{client_email}.json", "r") as file:
            license_details = json.load(file)

        # Convert stored expiry_date string back to a datetime object
        expiry_date = datetime.datetime.strptime(license_details['expiry_date'], '%Y-%m-%d')
        current_date = datetime.datetime.now()

        # Check if the license is expired
        if current_date > expiry_date:
            return False, "License has expired."

        # Check if the provided license key matches the stored one
        if provided_license_key != license_details['license_key']:
            return False, "Invalid license key."

        return True, "License is valid."

    except FileNotFoundError:
        return False, "License not found for the provided email."

# Usage example

# Generating a license
client_name = "John Doe"
client_email = "johndoe@example.com"
license_key = generate_license(client_name, client_email)
print(f"Generated License Key: {license_key}")

# Validating a license
is_valid, message = validate_license(client_email, license_key)
print(f"License Validation: {message}")