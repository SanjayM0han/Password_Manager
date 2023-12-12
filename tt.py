from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, master_password, file_path='passwords.txt'):
        self.file_path = file_path
        self.passwords = {}
        self.key = None

        # Load existing key from the file or generate a new one
        if os.path.exists('key.key'):
            with open('key.key', 'rb') as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(self.key)
            
        # Load existing passwords from the file
        if os.path.exists(self.file_path):
            self._load_passwords(master_password)

    def _load_passwords(self, master_password):
        with open(self.file_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = self.decrypt_data(encrypted_data, master_password)
        if decrypted_data is not None:
            self.passwords = json.loads(decrypted_data.decode('utf-8'))

    def _encrypt(self, data):
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def decrypt_data(self, encrypted_data, master_password):
        cipher = Fernet(self.key)
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None

    def _save_to_file(self):
        encrypted_data = self._encrypt(json.dumps(self.passwords).encode('utf-8'))
        with open(self.file_path, 'ab') as file:  # Use 'ab' for appending in binary mode
            file.write(encrypted_data + b'\n') 

    def save_password(self, category, website, username, password):
        if category not in self.passwords:
            self.passwords[category] = {}

        self.passwords[category][website] = {'category': category,'website' : website,'username': username, 'password': password}
        self._save_to_file()

    def get_password(self, category, website):
        if category in self.passwords and website in self.passwords[category]:
            return self.passwords[category][website]
        else:
            return None

    def list_categories(self):
        return list(self.passwords.keys())

    def list_websites(self, category):
        if category in self.passwords:
            return list(self.passwords[category].keys())
        else:
            return []

    def print_websites(self, category):
        websites = self.list_websites(category)
        if websites:
            print(f"Websites in '{category}':")
            for website in websites:
                print(website)
        else:
            print(f"No websites found in '{category}'.")

    def add_password(self):
        category = input("Enter the category: ")
        website = input("Enter the website: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        
        self.save_password(category, website, username, password)
        print("Password added successfully!")

    def view_passwords(self):
        if not self.passwords:
            print("No passwords stored.")
            return

        for category, websites in self.passwords.items():
            print(f"\nCategory: {category}")
            for website, credentials in websites.items():
                print(f"Website: {website}")
                print(f"Username: {credentials['username']}")
                print(f"Password: {credentials['password']}")
                print("-" * 20)

# Example usage:

if __name__ == "__main__":
    master_password = input("Enter your master password: ")
    password_manager = PasswordManager(master_password)
    
    while True:
        print("\nMenu:")
        print("1. Add a new password")
        print("2. View existing passwords")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, 3): ")

        if choice == "1":
            password_manager.add_password()
        elif choice == "2":
            password_manager.view_passwords()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    password_manager.save_password('password', 'google.com', 'msh', 'parayulla')
    password_manager.save_password('sports', 'fifa.com', 'nis', 'nokanda')
    password_manager.save_password('songs', 'spotify.com', 'nav', 'pattichea')
    password_manager.save_password('dance', 'americansgottalented.com', 'rev', 'tharoolla')
    
    
    
    # Get a password from category password in google.com website
    retrieved_password = password_manager.get_password('password', 'google.com')
    
    print("Retrieved Password:", retrieved_password)

        # List categories and websites
    print("Categories:", password_manager.list_categories())
    category_to_print = input("Enter the category to list websites: ")
    password_manager.print_websites(category_to_print)
    