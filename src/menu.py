import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

from src.API_utility import get_api_key, set_api_key

# Create the main window (root)
root = tk.Tk()
root.title("NASA APOD Wallpaper Setter")

# File where the API key is stored
CONFIG_FILE = "src/api_config.json"

# Process/thread to manage the auto and manual wallpaper setters
auto_setter_thread = None
manual_setter_thread = None

# Output Panel for Terminal Logs (read-only, positioned at the bottom of the window)
output_panel = tk.Text(
    root,
    bg="#f7f7f7",
    fg="green",
    height=10,
    borderwidth=2,
    relief="solid",
    state=tk.DISABLED,
)


# Load API key from JSON file
def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("APOD_API_KEY")
    else:
        return None


# Save API key to JSON file
def save_api_key(api_key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"APOD_API_KEY": api_key}, f, indent=4)
    set_api_key(api_key)  # Update the global key in API_utility.py


# Function to launch the manual wallpaper setter in a separate thread
def launch_manual_wallpaper_setter():
    global manual_setter_thread

    # Define the function that will start the manual wallpaper setter
    def run_manual_wallpaper_setter():
        subprocess.run(["python", "-m", "src.manual_wallpaper_setter"])

    # Start the manual wallpaper setter in a new thread
    manual_setter_thread = threading.Thread(target=run_manual_wallpaper_setter)
    manual_setter_thread.start()


# Function to launch the auto wallpaper setter in a separate thread
def launch_auto_wallpaper_setter():
    global auto_setter_thread

    # Define the function that will start the auto wallpaper setter
    def run_auto_wallpaper_setter():
        subprocess.run(["python", "-m", "src.wallpaper_setter"])

    # Start the auto wallpaper setter in a new thread
    auto_setter_thread = threading.Thread(target=run_auto_wallpaper_setter)
    auto_setter_thread.start()


# Function to close the wallpaper setters when the menu closes
def on_menu_close():
    global manual_setter_thread, auto_setter_thread
    if manual_setter_thread and manual_setter_thread.is_alive():
        print("Manual wallpaper setter is still running. Closing...")
        manual_setter_thread.join(timeout=1)
    if auto_setter_thread and auto_setter_thread.is_alive():
        print("Auto wallpaper setter is still running. Closing...")
        auto_setter_thread.join(timeout=1)
    root.destroy()


# Bind the on_menu_close function to the close button of the menu
root.protocol("WM_DELETE_WINDOW", on_menu_close)


def create_widgets(api_key=None):
    # Clear the window first except the output panel
    for widget in root.winfo_children():
        if widget != output_panel:
            widget.destroy()

    # Banner Label
    banner_label = tk.Label(
        root, text=print_banner(), font=("Courier", 12), justify=tk.LEFT
    )
    banner_label.pack(pady=10)

    # If no API key, show input prompt for API key, hide buttons
    if api_key is None:
        api_key_label = tk.Label(
            root, text="Enter your APOD API Key for the program to work:"
        )
        api_key_label.pack()

        api_key_entry = tk.Entry(root, show="*", width=40)
        api_key_entry.pack(pady=10)

        def on_submit():
            api_key_input = api_key_entry.get()
            if check_api_key(api_key_input):
                save_api_key(api_key_input)
                messagebox.showinfo("Success", "API Key accepted!")
                write_output(f"API Key set to: {api_key_input}")
                create_widgets(api_key_input)  # Rebuild widgets with the new API key
            else:
                messagebox.showwarning("Invalid", "Please enter a valid API key!")
                write_output("Invalid API Key entered.")

        submit_button = tk.Button(root, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

    # If API key exists, show the wallpaper action buttons and the change key option
    else:
        auto_button = tk.Button(
            root,
            text="Auto Wallpaper Set Today's Image",
            command=launch_auto_wallpaper_setter,
        )
        auto_button.pack(pady=10)

        manual_button = tk.Button(
            root, text="Manual Wallpaper Set", command=launch_manual_wallpaper_setter
        )
        manual_button.pack(pady=10)

        def change_api_key():
            create_widgets(api_key=None)  # Rebuild widgets to prompt for new API key

        change_key_button = tk.Button(
            root, text="Change API Key", command=change_api_key
        )
        change_key_button.pack(pady=10)

    # Repack the output panel at the bottom to ensure it stays there
    output_panel.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)


def print_banner() -> str:
    banner = """
     █████╗ ██████╗  ██████╗ ██████╗     ██╗███╗   ███╗ █████╗  ██████╗ ███████╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔════╝
    ███████║██████╔╝██║   ██║██║  ██║    ██║██╔████╔██║███████║██║  ███╗█████╗  ███████╗
    ██╔══██║██╔═══╝ ██║   ██║██║  ██║    ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ╚════██║
    ██║  ██║██║     ╚██████╔╝██████╔╝    ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗███████║
    ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═════╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═════╝ ╚══════╝╚══════╝
    """
    return banner


def check_api_key(api_key_input):
    return bool(api_key_input) and " " not in api_key_input


# Function to write output to the panel
def write_output(message):
    output_panel.config(state=tk.NORMAL)
    output_panel.insert(tk.END, message + "\n")
    output_panel.see(tk.END)  # Auto scroll to the bottom
    output_panel.config(state=tk.DISABLED)  # Make the panel read-only


# Redirect stdout to the output panel
class StdoutRedirector:
    def write(self, message):
        write_output(message.strip())

    def flush(self):  # Add flush method to prevent 'flush' errors
        pass


sys.stdout = StdoutRedirector()

if __name__ == "__main__":
    # Load the API key from the config file
    api_key = load_api_key()

    # Create widgets based on whether the API key is None or not
    if api_key and api_key != "None":
        create_widgets(api_key)
    else:
        create_widgets(None)

    root.mainloop()
