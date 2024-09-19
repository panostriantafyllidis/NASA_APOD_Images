import ctypes
import json
import os

# APOD_API_KEY = "yjdOU0OzXE53lNYoaWZQ6H5Fodjy8gJs4APnZW4r"


# Define the path to the config file
CONFIG_FILE = "src/api_config.json"


# Function to get the API key from the config.json file
def get_api_key():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            api_key = config.get("APOD_API_KEY")

            # Ensure the API key exists and is valid (not None or empty)
            if api_key and isinstance(api_key, str):
                return api_key
            else:
                print("API key is missing or invalid in config.json.")
                return None
    else:
        print("config.json file not found.")
        return None


# Function to set the API key in the config.json file
def set_api_key(api_key_input: str):
    """Set the APOD API key in the config file."""
    if not isinstance(api_key_input, str) or not api_key_input:
        print("Invalid API key provided. Please enter a valid API key.")
        return

    with open(CONFIG_FILE, "w") as file:
        json.dump({"APOD_API_KEY": api_key_input}, file, indent=4)
    print(f"API Key set to: {api_key_input}")


# Now, retrieve the API key whenever needed
APOD_API_KEY = get_api_key()

# Constant to work with Windows
SPI_SETDESKWALLPAPER = 20

SERVICE_NAME = "NASA Wallpaper"


# Function to change the background
def changeBG(path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
