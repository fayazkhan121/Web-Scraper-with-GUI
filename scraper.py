import requests
from bs4 import BeautifulSoup


def scrape_website(url, title_selector, link_selector, pages, headers=None):
    results = []
    current_page = 1

    while current_page <= pages:
        try:
            page_url = f"{url}?page={current_page}" if current_page > 1 else url
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.select(title_selector)
            links = soup.select(link_selector)

            for title, link in zip(titles, links):
                results.append((title.get_text().strip(), link.get('href')))

            current_page += 1
        except Exception as e:
            print(f"Error scraping page {current_page}: {e}")
            break

    return results


def get_selector_preview(url, title_selector, link_selector):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.select(title_selector)
        links = soup.select(link_selector)

        preview = ""
        for title, link in zip(titles, links):
            preview += f"Title: {title.get_text().strip()}\nLink: {link.get('href')}\n\n"

        return preview if preview else "No results found for the given selectors."
    except Exception as e:
        return f"Error previewing selectors: {e}"
