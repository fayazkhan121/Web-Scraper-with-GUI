import csv
import json
import os

CONFIG_FILE = "config.json"

def export_to_csv(data, file_path):
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link"])
        writer.writerows(data)

def export_to_json(data, file_path):
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def export_to_txt(data, file_path):
    with open(file_path, mode="w", encoding="utf-8") as file:
        for title, link in data:
            file.write(f"Title: {title}\nLink: {link}\n\n")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the config file is empty or malformed
            print("Error: The config file is empty or invalid.")
            return None
    return None

def save_config(url, title_selector, link_selector, pages):
    config = {
        "url": url,
        "title_selector": title_selector,
        "link_selector": link_selector,
        "pages": pages
    }

    if not os.path.exists(CONFIG_FILE):
        # If the config file doesn't exist, create it with default values
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
    else:
        # Otherwise, update the existing config file
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
