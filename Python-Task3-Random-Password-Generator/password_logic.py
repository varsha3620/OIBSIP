import secrets
import string


def generate_secure_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
    exclude_ambiguous
):
    """Generate a secure password based on the selected options."""

    ambiguous_characters = "0O1lI"

    characters = ""
    password = ""

    # Uppercase letters
    if use_uppercase:
        uppercase_characters = string.ascii_uppercase

        if exclude_ambiguous:
            uppercase_characters = "".join(
                c for c in uppercase_characters
                if c not in ambiguous_characters
            )

        characters += uppercase_characters
        password += secrets.choice(uppercase_characters)

    # Lowercase letters
    if use_lowercase:
        lowercase_characters = string.ascii_lowercase

        if exclude_ambiguous:
            lowercase_characters = "".join(
                c for c in lowercase_characters
                if c not in ambiguous_characters
            )

        characters += lowercase_characters
        password += secrets.choice(lowercase_characters)

    # Numbers
    if use_numbers:
        number_characters = string.digits

        if exclude_ambiguous:
            number_characters = "".join(
                c for c in number_characters
                if c not in ambiguous_characters
            )

        characters += number_characters
        password += secrets.choice(number_characters)

    # Symbols
    if use_symbols:
        characters += string.punctuation
        password += secrets.choice(string.punctuation)

    # Fill remaining characters
    remaining_length = length - len(password)

    for _ in range(remaining_length):
        password += secrets.choice(characters)

    # Securely shuffle the password
    password = list(password)
    secrets.SystemRandom().shuffle(password)

    return "".join(password)