import csv
import json
import os
import requests

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
            return None
    return None


def save_config(url, title_selector, link_selector, pages, headers, proxies):
    config = {
        "url": url,
        "title_selector": title_selector,
        "link_selector": link_selector,
        "pages": pages,
        "headers": headers,
        "proxies": proxies
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def configure_headers_and_proxies(headers_str, proxies_str):
    headers = {}
    proxies = {}

    if headers_str:
        headers = dict(x.split(": ") for x in headers_str.split(","))

    if proxies_str:
        proxies = {"http": proxies_str, "https": proxies_str}

    return headers, proxies
