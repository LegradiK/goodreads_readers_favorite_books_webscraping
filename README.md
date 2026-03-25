# Goodreads Choice Awards Browser

A Flask web app that scrapes and displays Goodreads Readers Choice Award nominees across 5 genres from 2011 to 2025, complete with votes, ratings, and links back to each book's Goodreads page.

---

## Features

- Scrapes nominee data from the Goodreads Choice Awards pages (2011–2025)
- Fetches individual book ratings in parallel using `ThreadPoolExecutor`
- Caches all data locally to `books.json` — scraper only runs once
- Filter by genre and year, sort by rank, votes, title and author
- Control how many results are displayed (10, 20, 30, 50, 100, or All)
- Export currently visible results to a .csv file
- Clickable book titles linking directly to the Goodreads page
- Coffee-themed UI built with Flask and Jinja2

---

## Genres Covered

- Fiction
- Historical Fiction
- Mystery / Thriller
- Fantasy
- Science Fiction

---

## Project Structure

```
goodreads_readers_favorite_books_webscraping/
├── README.md
├── .gitignore
├── main.py                  # Scraper + Flask app
├── books.json               # Cached book data (auto-generated)
├── templates/
│   ├── base.html
│   ├── home.html
│   └── footer.html
└── static/
    ├── style.css
    └── script.js

```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/LegradiK/goodreads_readers_favorite_books_webscraping.git
cd goodreads_readers_favorite_books_webscraping
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install flask requests bs4
```

### 4. Run the app

```bash
python3 main.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## How It Works

### Phase 1 — Metadata scrape
The scraper loops through all 15 years × 5 genres (75 pages total), extracting each nominee's title, author, rank, vote count, and Goodreads URL.

### Phase 2 — Ratings (parallel)
Using `ThreadPoolExecutor` with 10 workers, the app fetches each book's individual Goodreads page to extract its community rating. This runs concurrently to keep total time reasonable.

### Caching
Once scraping completes, everything is saved to `books.json`. On every subsequent run the app loads from this file instantly — no re-scraping. To refresh the data, delete `books.json` and restart.

```bash
rm books.json
python3 main.py
```

---

## Filtering & Display
| Control | Options | Default |
|---|---|---|
| Genre | All Genres, Fiction, Historical Fiction, Mystery / Thriller, Fantasy, Science Fiction | All Genres |
| Year | All Years, 2011–2025 | All Years |
| Sort by | Votes, Rating, Title A–Z, Author A–Z | Votes |
| Show | All, 10, 20, 30, 50, 100 | All |
 
### Export to CSV
The **Export as CSV** button downloads a `.csv` file of whatever is currently visible in the table — respecting any active filters, sort order, and show limit. The file can be opened directly in Excel or Google Sheets.
 
---

## Notes

- Goodreads does not provide an official public API for this data
- The scraper uses a realistic `User-Agent` header to avoid being blocked
- URL format changed in 2024: pre-2024 pages use `choiceawards/best-*`, 2024+ use `choiceawards/readers-favorite-*` — both are handled automatically
- Scraping ~750 book pages for ratings takes several minutes on first run

---

## Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework |
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `concurrent.futures` | Parallel rating fetches (stdlib) |