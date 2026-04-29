import json
import os

SETTINGS_FILE = "config/settings.json"


def load_settings():
    os.makedirs("config", exist_ok=True)

    default_settings = {
        "dark_mode": False,
        "window_geometry": "1100x650",
        "maximized": False,
        "font_family": "Arial",
        "font_size": 11,
        "default_start_page": "Dashboard",
        "auto_backup": True
    }

    if not os.path.exists(SETTINGS_FILE):
        return default_settings

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        return {**default_settings, **settings}

    except Exception:
        return default_settings


def save_settings(settings):
    os.makedirs("config", exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)