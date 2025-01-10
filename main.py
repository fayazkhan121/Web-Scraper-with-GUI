import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import json
import os
import requests
import threading
import time
from scraper import scrape_website, get_selector_preview
from utils import export_to_csv, export_to_json, export_to_txt, load_config, save_config, configure_headers_and_proxies

# Global variable to store scraping results
scraped_results = []
progress_lock = threading.Lock()


# Function to handle the scrape button click
def scrape():
    url = url_entry.get().strip()
    title_selector = title_selector_entry.get().strip()
    link_selector = link_selector_entry.get().strip()
    pages = int(pages_entry.get().strip()) if pages_entry.get().strip() else 1
    headers = headers_entry.get().strip()
    proxies = proxies_entry.get().strip()

    if not url or not title_selector or not link_selector:
        messagebox.showerror("Error", "Please enter URL and both selectors.")
        return

    try:
        progress_bar.start()
        root.update()

        # Set headers and proxies if provided
        headers_dict = configure_headers_and_proxies(headers, proxies)

        # Create a separate thread for scraping to avoid blocking the main GUI thread
        threading.Thread(target=run_scraping, args=(url, title_selector, link_selector, pages, headers_dict)).start()

    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"An error occurred: {e}")


# Scraping function that runs in a separate thread
def run_scraping(url, title_selector, link_selector, pages, headers):
    try:
        global scraped_results
        scraped_results = scrape_website(url, title_selector, link_selector, pages, headers)

        progress_bar.stop()
        display_results(scraped_results)

    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"Scraping failed: {e}")


# Function to display the scraped results in the text box
def display_results(results):
    results_text.delete(1.0, tk.END)  # Clear previous results
    if results:
        for title, link in results:
            results_text.insert(tk.END, f"Title: {title}\nLink: {link}\n\n")
    else:
        results_text.insert(tk.END, "No results found.\n")


# Function to handle export button click
def export_results():
    if not scraped_results:
        messagebox.showerror("Error", "No results to export")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        if file_path.endswith(".csv"):
            export_to_csv(scraped_results, file_path)
        elif file_path.endswith(".json"):
            export_to_json(scraped_results, file_path)
        elif file_path.endswith(".txt"):
            export_to_txt(scraped_results, file_path)

        messagebox.showinfo("Success", f"Results exported to {file_path}")


# Load saved configurations
def load_saved_config():
    config = load_config()
    if config:
        url_entry.insert(0, config["url"])
        title_selector_entry.insert(0, config["title_selector"])
        link_selector_entry.insert(0, config["link_selector"])
        pages_entry.insert(0, str(config["pages"]))
        headers_entry.insert(0, config["headers"])
        proxies_entry.insert(0, config["proxies"])


# Function to preview selectors (live testing)
def test_selectors():
    url = url_entry.get().strip()
    title_selector = title_selector_entry.get().strip()
    link_selector = link_selector_entry.get().strip()

    if not url or not title_selector or not link_selector:
        messagebox.showerror("Error", "Please enter URL and selectors.")
        return

    preview = get_selector_preview(url, title_selector, link_selector)
    selector_preview_text.delete(1.0, tk.END)
    selector_preview_text.insert(tk.END, preview)


# Create the GUI application window
root = tk.Tk()
root.title("Advanced Web Scraper")
root.geometry("900x700")
root.configure(bg="#f5f5f5")

# Set the color scheme
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
BUTTON_COLOR = "#FFC107"
TEXT_COLOR = "#333333"

# Create and style the widgets
url_label = tk.Label(root, text="Enter URL:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
url_entry.pack(pady=5)

title_selector_label = tk.Label(root, text="Enter Title Selector:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
title_selector_label.pack(pady=10)

title_selector_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
title_selector_entry.pack(pady=5)

link_selector_label = tk.Label(root, text="Enter Link Selector:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
link_selector_label.pack(pady=10)

link_selector_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
link_selector_entry.pack(pady=5)

pages_label = tk.Label(root, text="Number of Pages to Scrape:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
pages_label.pack(pady=10)

pages_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
pages_entry.pack(pady=5)

headers_label = tk.Label(root, text="Custom Headers (Optional):", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
headers_label.pack(pady=10)

headers_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
headers_entry.pack(pady=5)

proxies_label = tk.Label(root, text="Custom Proxies (Optional):", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
proxies_label.pack(pady=10)

proxies_entry = tk.Entry(root, width=60, font=("Arial", 12), relief="solid", borderwidth=2)
proxies_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Scrape", command=scrape, bg=PRIMARY_COLOR, fg="white", font=("Arial", 12),
                          relief="solid")
scrape_button.pack(pady=15)

test_button = tk.Button(root, text="Test Selectors", command=test_selectors, bg=BUTTON_COLOR, fg="white",
                        font=("Arial", 12), relief="solid")
test_button.pack(pady=10)

export_button = tk.Button(root, text="Export Results", command=export_results, bg=BUTTON_COLOR, fg="white",
                          font=("Arial", 12), relief="solid")
export_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=15)

results_label = tk.Label(root, text="Results:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
results_label.pack(pady=10)

results_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10), wrap=tk.WORD)
results_text.pack(pady=5)

selector_preview_label = tk.Label(root, text="Selector Preview:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
selector_preview_label.pack(pady=10)

selector_preview_text = scrolledtext.ScrolledText(root, width=70, height=10, font=("Arial", 10), wrap=tk.WORD)
selector_preview_text.pack(pady=5)

# Load saved configurations on start
load_saved_config()

# Run the application
root.mainloop()
