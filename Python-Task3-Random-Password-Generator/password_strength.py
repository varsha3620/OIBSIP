def calculate_strength(password, selected_types):
    """Calculate password strength based on length and character diversity."""

    strength = 0

    if len(password) >= 12:
        strength += 1

    strength += selected_types

    if strength <= 2:
        return "Weak"

    elif strength <= 4:
        return "Medium"

    else:
        return "Strong"