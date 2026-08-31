import random
import string

while True:

    # Ask for password length
    while True:
        try:
            length = int(input("Enter password length (minimum 8): "))

            if length >= 8:
                break
            else:
                print("Password length must be at least 8 characters. Please try again.")

        except ValueError:
            print("Please enter a valid number.")

    # Ask for character types
    while True:
        include_uppercase = input("Include uppercase letters? (y/n): ").lower()
        include_lowercase = input("Include lowercase letters? (y/n): ").lower()
        include_numbers = input("Include numbers? (y/n): ").lower()
        include_symbols = input("Include symbols? (y/n): ").lower()

        selected_types = 0

        if include_uppercase == "y":
            selected_types += 1

        if include_lowercase == "y":
            selected_types += 1

        if include_numbers == "y":
            selected_types += 1

        if include_symbols == "y":
            selected_types += 1

        if selected_types == 0:
            print("Please select at least one character type.")
        elif selected_types < 2:
            print("Please select at least 2 character types.")
        else:
            break

    # Create character collection
    characters = ""
    password = ""

    if include_uppercase == "y":
        characters += string.ascii_uppercase
        password += random.choice(string.ascii_uppercase)

    if include_lowercase == "y":
        characters += string.ascii_lowercase
        password += random.choice(string.ascii_lowercase)

    if include_numbers == "y":
        characters += string.digits
        password += random.choice(string.digits)

    if include_symbols == "y":
        characters += string.punctuation
        password += random.choice(string.punctuation)

    # Fill remaining characters
    remaining_length = length - len(password)

    for i in range(remaining_length):
        password += random.choice(characters)

    # Shuffle password
    password = list(password)
    random.shuffle(password)
    password = "".join(password)

    print("Generated Password:", password)

    # Ask to generate another password
    again = input("Generate another password? (y/n): ").lower()

    if again != "y":
        print("Thank you for using the Random Password Generator!")
        break