import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import json
import os
from scraper import scrape_website
from utils import export_to_csv, export_to_json, export_to_txt, load_config, save_config


# Function to handle the scrape button click
def scrape():
    url = url_entry.get().strip()
    title_selector = title_selector_entry.get().strip()
    link_selector = link_selector_entry.get().strip()
    pages = int(pages_entry.get().strip()) if pages_entry.get().strip() else 1

    if not url or not title_selector or not link_selector:
        messagebox.showerror("Error", "Please enter URL and both selectors.")
        return

    try:
        progress_bar.start()
        root.update()

        # Scrape the website with the given selectors
        results = scrape_website(url, title_selector, link_selector, pages)

        progress_bar.stop()

        if results:
            results_text.delete(1.0, tk.END)  # Clear previous results
            for title, link in results:
                results_text.insert(tk.END, f"Title: {title}\nLink: {link}\n\n")
        else:
            results_text.insert(tk.END, "No results found.\n")

        global scraped_results
        scraped_results = results

        # Save the scraping configuration
        save_config(url, title_selector, link_selector, pages)

    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"An error occurred: {e}")


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


# Function to load saved configuration for last session
def load_saved_config():
    config = load_config()
    if config:
        url_entry.insert(0, config["url"])
        title_selector_entry.insert(0, config["title_selector"])
        link_selector_entry.insert(0, config["link_selector"])
        pages_entry.insert(0, str(config["pages"]))


# Create the GUI application window
root = tk.Tk()
root.title("Advanced Web Scraper")
root.geometry("800x600")  # Set the window size
root.configure(bg="#f5f5f5")  # Set background color

# Set the color scheme
PRIMARY_COLOR = "#4CAF50"  # Green for primary elements
SECONDARY_COLOR = "#2196F3"  # Blue for secondary elements
BUTTON_COLOR = "#FFC107"  # Yellow for buttons
TEXT_COLOR = "#333333"  # Dark text color

# Scraped results storage
scraped_results = []

# Create and style the widgets
url_label = tk.Label(root, text="Enter URL:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50, font=("Arial", 12), relief="solid", borderwidth=2)
url_entry.pack(pady=5)

title_selector_label = tk.Label(root, text="Enter Title Selector:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
title_selector_label.pack(pady=10)

title_selector_entry = tk.Entry(root, width=50, font=("Arial", 12), relief="solid", borderwidth=2)
title_selector_entry.pack(pady=5)

link_selector_label = tk.Label(root, text="Enter Link Selector:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
link_selector_label.pack(pady=10)

link_selector_entry = tk.Entry(root, width=50, font=("Arial", 12), relief="solid", borderwidth=2)
link_selector_entry.pack(pady=5)

pages_label = tk.Label(root, text="Number of Pages to Scrape:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
pages_label.pack(pady=10)

pages_entry = tk.Entry(root, width=50, font=("Arial", 12), relief="solid", borderwidth=2)
pages_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Scrape", command=scrape, bg=PRIMARY_COLOR, fg="white", font=("Arial", 12),
                          relief="solid")
scrape_button.pack(pady=15)

export_button = tk.Button(root, text="Export Results", command=export_results, bg=BUTTON_COLOR, fg="white",
                          font=("Arial", 12), relief="solid")
export_button.pack(pady=10)

# Progress bar setup
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=15)

results_label = tk.Label(root, text="Results:", bg="#f5f5f5", fg=TEXT_COLOR, font=("Arial", 12))
results_label.pack(pady=10)

# ScrolledText widget for displaying results
results_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10), wrap=tk.WORD)
results_text.pack(pady=5)

# Load saved configurations on start
load_saved_config()

# Run the application
root.mainloop()
