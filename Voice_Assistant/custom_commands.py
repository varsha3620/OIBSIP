import webbrowser


def execute_custom_command(command):

    command = command.lower().strip()

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    elif "open my portfolio" in command or "open portfolio" in command:
        webbrowser.open("YOUR_PORTFOLIO_URL")
        return "Opening your portfolio."

    else:
        return "Sorry, I don't know that custom command yet."