import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# =========================
# Main Window
# =========================

window = tk.Tk()
window.title("Random Password Generator")
window.geometry("520x650")
window.resizable(False, False)
window.configure(bg="white")


# =========================
# Colors
# =========================

BLUE = "#4F46E5"
BLUE_HOVER = "#4338CA"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F6FA"
BORDER = "#E5E7EB"
TEXT = "#1F2937"
GRAY = "#6B7280"
GREEN = "#16A34A"
ORANGE = "#D97706"


# =========================
# Variables
# =========================

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
exclude_ambiguous_var = tk.BooleanVar(value=False)

password_history = []


# =========================
# Copy Password
# =========================

def copy_password():

    password = password_display.get()

    if password:

        pyperclip.copy(password)

        status_label.config(
            text="✓ Password copied to clipboard",
            fg=GREEN
        )

    else:

        status_label.config(
            text="No password to copy",
            fg=ORANGE
        )


# =========================
# Password Strength
# =========================

def show_strength(password):

    strength = 0

    if len(password) >= 12:
        strength += 1

    if uppercase_var.get():
        strength += 1

    if lowercase_var.get():
        strength += 1

    if numbers_var.get():
        strength += 1

    if symbols_var.get():
        strength += 1

    if strength <= 2:

        strength_label.config(
            text="● Weak",
            fg=ORANGE
        )

    elif strength <= 4:

        strength_label.config(
            text="● Medium",
            fg="#CA8A04"
        )

    else:

        strength_label.config(
            text="● Strong",
            fg=GREEN
        )


# =========================
# Generate Password
# =========================

def generate_password():

    length = int(length_spinbox.get())

    # Count selected character types
    selected_types = 0

    if uppercase_var.get():
        selected_types += 1

    if lowercase_var.get():
        selected_types += 1

    if numbers_var.get():
        selected_types += 1

    if symbols_var.get():
        selected_types += 1

    # Validation
    if selected_types < 2:

        messagebox.showwarning(
            "Invalid Selection",
            "Please select at least 2 character types."
        )

        return

    characters = ""
    password = ""

    ambiguous_characters = "0O1lI"


    # Uppercase
    if uppercase_var.get():

        uppercase_characters = string.ascii_uppercase

        if exclude_ambiguous_var.get():

            uppercase_characters = "".join(
                c for c in uppercase_characters
                if c not in ambiguous_characters
            )

        characters += uppercase_characters

        password += secrets.choice(
            uppercase_characters
        )


    # Lowercase
    if lowercase_var.get():

        lowercase_characters = string.ascii_lowercase

        if exclude_ambiguous_var.get():

            lowercase_characters = "".join(
                c for c in lowercase_characters
                if c not in ambiguous_characters
            )

        characters += lowercase_characters

        password += secrets.choice(
            lowercase_characters
        )


    # Numbers
    if numbers_var.get():

        number_characters = string.digits

        if exclude_ambiguous_var.get():

            number_characters = "".join(
                c for c in number_characters
                if c not in ambiguous_characters
            )

        characters += number_characters

        password += secrets.choice(
            number_characters
        )


    # Symbols
    if symbols_var.get():

        characters += string.punctuation

        password += secrets.choice(
            string.punctuation
        )


    # Fill remaining characters
    remaining_length = length - len(password)

    for i in range(remaining_length):

        password += secrets.choice(characters)


    # Shuffle
    password = list(password)

    secrets.SystemRandom().shuffle(password)

    password = "".join(password)


    # Display password
    password_display.delete(
        0,
        tk.END
    )

    password_display.insert(
        0,
        password
    )


    # Automatic copy
    pyperclip.copy(password)

    status_label.config(
        text="✓ Password generated ",
        fg=GREEN
    )


    # Add to history
    password_history.insert(
        0,
        password
    )

    if len(password_history) > 5:
        password_history.pop()


    # Update history
    history_listbox.delete(
        0,
        tk.END
    )

    for old_password in password_history:

        history_listbox.insert(
            tk.END,
            old_password
        )


    # Strength
    show_strength(password)


# =========================
# Header
# =========================

title_label = tk.Label(
    window,
    text="🔐 Random Password Generator",
    font=("Segoe UI", 20, "bold"),
    bg=WHITE,
    fg=TEXT
)

title_label.pack(
    pady=(20, 3)
)


subtitle_label = tk.Label(
    window,
    text="Create strong and secure passwords",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=GRAY
)

subtitle_label.pack(
    pady=(0, 15)
)


# =========================
# Settings Card
# =========================

settings_card = tk.Frame(
    window,
    bg=LIGHT_GRAY,
    highlightbackground=BORDER,
    highlightthickness=1
)

settings_card.pack(
    padx=45,
    fill="x"
)


settings_inner = tk.Frame(
    settings_card,
    bg=LIGHT_GRAY
)

settings_inner.pack(
    padx=25,
    pady=15
)


# =========================
# Length
# =========================

length_label = tk.Label(
    settings_inner,
    text="PASSWORD LENGTH",
    font=("Segoe UI", 9, "bold"),
    bg=LIGHT_GRAY,
    fg=GRAY
)

length_label.pack(
    anchor="w"
)


length_frame = tk.Frame(
    settings_inner,
    bg=LIGHT_GRAY
)

length_frame.pack(
    fill="x",
    pady=(5, 12)
)


length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=50,
    width=8,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

length_spinbox.pack(
    side="left"
)


length_info = tk.Label(
    length_frame,
    text="8 – 50 characters",
    font=("Segoe UI", 9),
    bg=LIGHT_GRAY,
    fg=GRAY
)

length_info.pack(
    side="left",
    padx=10
)


# =========================
# Character Types
# =========================

options_label = tk.Label(
    settings_inner,
    text="CHARACTER TYPES",
    font=("Segoe UI", 9, "bold"),
    bg=LIGHT_GRAY,
    fg=GRAY
)

options_label.pack(
    anchor="w"
)


def create_checkbox(text, variable):

    checkbox = tk.Checkbutton(
        settings_inner,
        text=text,
        variable=variable,
        font=("Segoe UI", 9),
        bg=LIGHT_GRAY,
        fg=TEXT,
        activebackground=LIGHT_GRAY,
        activeforeground=TEXT,
        selectcolor=WHITE,
        anchor="w"
    )

    checkbox.pack(
        fill="x",
        pady=1
    )


create_checkbox(
    "Uppercase Letters",
    uppercase_var
)

create_checkbox(
    "Lowercase Letters",
    lowercase_var
)

create_checkbox(
    "Numbers",
    numbers_var
)

create_checkbox(
    "Symbols",
    symbols_var
)

create_checkbox(
    "Exclude Ambiguous Characters",
    exclude_ambiguous_var
)


# =========================
# Password Section
# =========================

password_label = tk.Label(
    window,
    text="YOUR PASSWORD",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=GRAY
)

password_label.pack(
    anchor="w",
    padx=65,
    pady=(15, 5)
)


password_display = tk.Entry(
    window,
    width=40,
    font=("Consolas", 13, "bold"),
    justify="center",
    relief="solid",
    bd=1,
    bg=LIGHT_GRAY,
    fg=TEXT
)

password_display.pack(
    ipady=7
)


# =========================
# Strength
# =========================

strength_label = tk.Label(
    window,
    text="● Strength: --",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=GRAY
)

strength_label.pack(
    pady=(6, 2)
)


# =========================
# Status
# =========================

status_label = tk.Label(
    window,
    text="",
    font=("Segoe UI", 8),
    bg=WHITE
)

status_label.pack(
    pady=2
)


# =========================
# History
# =========================

history_label = tk.Label(
    window,
    text="LAST 5 GENERATED PASSWORDS",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=GRAY
)

history_label.pack(
    anchor="w",
    padx=65,
    pady=(6, 4)
)


history_listbox = tk.Listbox(
    window,
    width=43,
    height=4,
    font=("Consolas", 9),
    bg=LIGHT_GRAY,
    fg=TEXT,
    selectbackground=BLUE,
    selectforeground=WHITE,
    relief="solid",
    bd=1
)

history_listbox.pack()


# =========================
# Buttons
# =========================

button_frame = tk.Frame(
    window,
    bg=WHITE
)

button_frame.pack(
    pady=12
)


generate_button = tk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password,
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_HOVER,
    activeforeground=WHITE,
    relief="flat",
    padx=22,
    pady=8,
    cursor="hand2"
)

generate_button.pack(
    side="left",
    padx=4
)


copy_button = tk.Button(
    button_frame,
    text="📋 Copy to Clipboard",
    command=copy_password,
    font=("Segoe UI", 10, "bold"),
    bg=LIGHT_GRAY,
    fg=TEXT,
    activebackground=BORDER,
    activeforeground=TEXT,
    relief="solid",
    bd=1,
    padx=18,
    pady=7,
    cursor="hand2"
)

copy_button.pack(
    side="left",
    padx=4
)


# =========================
# Start Application
# =========================

window.mainloop()