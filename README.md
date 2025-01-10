# Web Scraper - Extract Blog Titles and Links

## Overview
This web scraper allows you to extract blog titles and links from a given URL. You can specify CSS selectors for the title and link elements to precisely extract the data. The scraper also supports pagination, allowing you to scrape multiple pages.

## How to Use the Scraper

### **URL:**
- **What is the URL?**
  The **URL** is the web address of the blog or website you want to scrape. For example:
  - `https://realpython.com/`
  - `https://example-blog.com/`
  
  Paste the URL in the **Enter URL** field of the GUI.

### **Title Selector:**
- **What is a Title Selector?**
  The **Title Selector** is a CSS selector used to identify the HTML elements containing the article titles on the webpage.
  - For example, if the title is inside an `<h2>` element with the class `card-title`, the selector would be:
    ```css
    h2.card-title
    ```

- **How to find the title selector?**
  1. Open the webpage in a browser (e.g., Google Chrome).
  2. Right-click on the title of an article and select **Inspect**.
  3. Find the HTML element that wraps the title (e.g., `<h2 class="card-title">Article Title</h2>`).
  4. Use this element's tag (e.g., `h2`) and class (e.g., `.card-title`) as your selector.

### **Link Selector:**
- **What is a Link Selector?**
  The **Link Selector** is a CSS selector used to identify the HTML elements containing the links to the full articles.
  - For example, if the link is inside an anchor (`<a>`) tag inside the `h2` element, the selector would be:
    ```css
    h2.card-title a
    ```

- **How to find the link selector?**
  1. Right-click on the link to the article (e.g., the title text) and select **Inspect**.
  2. Find the `<a>` tag inside the title element (e.g., `<a href="article-link">Article Title</a>`).
  3. Use the anchor tag (`<a>`) as your selector.

### **Number of Pages to Scrape:**
- **What is this field for?**
  If the website uses pagination (i.e., content is spread across multiple pages), you can specify how many pages to scrape.
  - For example, if you want to scrape pages 1 through 5, enter `5` in the **Number of Pages to Scrape** field.
  - If you want to scrape just the first page, leave it as `1` (default value).

---

## Steps for Scraping the Data

### **Step 1: Enter the URL**
- Enter the web address of the page you want to scrape. Example: `https://realpython.com/`

### **Step 2: Enter the Title Selector**
- Enter the CSS selector for the title of each article. Example for `https://realpython.com/`: `h2.card-title`.

### **Step 3: Enter the Link Selector**
- Enter the CSS selector for the link to the article. Example for `https://realpython.com/`: `h2.card-title a`.

### **Step 4: Enter the Number of Pages to Scrape**
- Enter how many pages you want to scrape. For example, enter `1` for the first page, or `5` for the first five pages.

### **Step 5: Click on Scrape**
- Click the **Scrape** button. The scraper will begin extracting titles and links from the specified URL and pages.

### **Step 6: View Results**
- Once scraping is complete, the extracted results will be displayed in the **Results** area.

### **Step 7: Export Results**
- To save the results, click **Export Results**. You can export the data to CSV, JSON, or TXT files.

---

## **Configuration File (`config.json`)**

### Where is the `config.json` file?
- The `config.json` file stores the last used settings (URL, title selector, link selector, number of pages). This allows you to easily continue scraping without re-entering these values.
- If the file doesn’t exist, the program will create it with default values.

### Example `config.json` File:
```json
{
    "url": "https://realpython.com/",
    "title_selector": "h2.card-title",
    "link_selector": "h2.card-title a",
    "pages": 1
}
