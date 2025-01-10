import requests
from bs4 import BeautifulSoup
import time

def scrape_website(url, title_selector, link_selector, pages):
    results = []
    current_page = 1

    while current_page <= pages:
        try:
            # Construct the page URL (assumes pagination works via ?page=...)
            page_url = f"{url}?page={current_page}" if current_page > 1 else url
            response = requests.get(page_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.select(title_selector)
            links = soup.select(link_selector)

            if not titles or not links:
                raise ValueError("Invalid CSS selectors. Could not find titles or links.")

            for title, link in zip(titles, links):
                results.append((title.get_text().strip(), link.get('href')))

            current_page += 1
            time.sleep(1)  # Respectful pause between requests
        except requests.exceptions.RequestException as e:
            print(f"Request error on page {current_page}: {e}")
            break
        except ValueError as e:
            print(f"Error: {e}")
            break
        except Exception as e:
            print(f"Error scraping page {current_page}: {e}")
            break

    return results
