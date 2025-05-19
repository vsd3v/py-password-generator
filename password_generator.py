import tkinter as tk
from tkinter import ttk  # For themed widgets
from tkinter import messagebox
import string
import random
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, root_window):
        self.root_window = root_window
        root_window.title("Password Generator")
        root_window.geometry("450x400")  # Adjusted window size
        root_window.resizable(False, False)  # Make window not resizable

        # --- Style ---
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Using a modern theme

        # --- Variables for UI elements ---
        self.length_var = tk.IntVar(value=16)  # Default password length
        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_chars_var = tk.BooleanVar(value=True)
        self.generated_password_var = tk.StringVar()

        # --- UI Layout ---
        main_frame = ttk.Frame(root_window, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Title ---
        title_label = ttk.Label(main_frame, text="Secure Password Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # --- Length Option ---
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill=tk.X, pady=5)
        ttk.Label(length_frame, text="Password Length:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.length_spinbox = ttk.Spinbox(length_frame, from_=4, to_=128, textvariable=self.length_var, width=5,
                                          font=("Arial", 10))
        self.length_spinbox.pack(side=tk.LEFT)

        # --- Character Type Options ---
        options_frame = ttk.LabelFrame(main_frame, text="Include Character Types", padding="10 10 10 10")
        options_frame.pack(fill=tk.X, pady=10)

        ttk.Checkbutton(options_frame, text="Lowercase Letters (a-z)", variable=self.use_lowercase_var).pack(
            anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Uppercase Letters (A-Z)", variable=self.use_uppercase_var).pack(
            anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.use_digits_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Special Characters (!@#...)", variable=self.use_special_chars_var).pack(
            anchor=tk.W)

        # --- Generate Button ---
        generate_button = ttk.Button(main_frame, text="Generate Password", command=self.generate_and_display_password,
                                     style="Accent.TButton")
        self.style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        generate_button.pack(pady=15, ipadx=10, ipady=5)  # Added padding for button

        # --- Generated Password Display ---
        password_display_frame = ttk.Frame(main_frame)
        password_display_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_display_frame, text="Generated Password:", font=("Arial", 10)).pack(side=tk.LEFT,
                                                                                               pady=(0, 5))
        self.password_entry = ttk.Entry(password_display_frame, textvariable=self.generated_password_var,
                                        state='readonly', font=("Courier", 11))  # Courier for monospace
        self.password_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 5))

        copy_button = ttk.Button(password_display_frame, text="Copy", command=self.copy_to_clipboard, width=6)
        copy_button.pack(side=tk.LEFT)

    def _generate_password_logic(self, length, use_lowercase, use_uppercase, use_digits, use_special_chars):
        """
        Generates a random password based on specified criteria.
        Internal logic function.
        """
        character_pool = ''
        if use_lowercase:
            character_pool += string.ascii_lowercase
        if use_uppercase:
            character_pool += string.ascii_uppercase
        if use_digits:
            character_pool += string.digits
        if use_special_chars:
            # Using a more common set of special characters
            character_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not character_pool:
            return None  # Indicates error

        if length < 1:
            return None  # Indicates error

        # Ensure the password contains at least one of each selected character type if possible
        # This makes the password stronger and meets criteria more reliably if length allows
        password_chars = []

        # Use secrets for cryptographically strong randomness if available (Python 3.6+)
        try:
            import secrets
            choice_method = secrets.choice
        except ImportError:
            choice_method = random.choice  # Fallback to random.choice

        # Add at least one of each required type
        if use_lowercase:
            password_chars.append(choice_method(string.ascii_lowercase))
        if use_uppercase:
            password_chars.append(choice_method(string.ascii_uppercase))
        if use_digits:
            password_chars.append(choice_method(string.digits))
        if use_special_chars:
            password_chars.append(choice_method("!@#$%^&*()_+-=[]{}|;:,.<>?"))

        # Fill the rest of the password length
        remaining_length = length - len(password_chars)
        if remaining_length < 0:  # If length is too short for all selected types
            # Just create from the pool up to the desired length, might not contain all types
            # This scenario is less likely with typical lengths (e.g., 8+)
            password_chars = [choice_method(character_pool) for _ in range(length)]
        else:
            for _ in range(remaining_length):
                password_chars.append(choice_method(character_pool))

        # Shuffle the list to ensure randomness of character positions
        random.shuffle(password_chars)

        return "".join(password_chars)

    def generate_and_display_password(self):
        """
        Handles the password generation and updates the UI.
        """
        length = self.length_var.get()
        use_lowercase = self.use_lowercase_var.get()
        use_uppercase = self.use_uppercase_var.get()
        use_digits = self.use_digits_var.get()
        use_special = self.use_special_chars_var.get()

        if not (use_lowercase or use_uppercase or use_digits or use_special):
            messagebox.showerror("Error", "Please select at least one character type.")
            self.generated_password_var.set("")
            return

        if length < 4 and (use_lowercase + use_uppercase + use_digits + use_special > length):
            messagebox.showwarning("Warning",
                                   "Password length is very short for the selected character types. It might not include all chosen types.")

        generated_pw = self._generate_password_logic(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special_chars=use_special
        )

        if generated_pw:
            self.generated_password_var.set(generated_pw)
        else:
            # This case should ideally be caught by the character type check above
            messagebox.showerror("Error", "Could not generate password. Check settings.")
            self.generated_password_var.set("")

    def copy_to_clipboard(self):
        """
        Copies the generated password to the system clipboard.
        """
        password_to_copy = self.generated_password_var.get()
        if password_to_copy:
            try:
                pyperclip.copy(password_to_copy)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            except pyperclip.PyperclipException:
                messagebox.showwarning("Copy Error",
                                       "Could not copy to clipboard. Make sure you have a copy/paste mechanism installed (e.g., xclip or xsel on Linux).")
        else:
            messagebox.showwarning("Nothing to Copy", "Generate a password first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
