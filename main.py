import requests
import json
import os
from flask import Flask, render_template
from bs4 import BeautifulSoup
import time

# data is only available from 2011 - 2025
BASE_URL = "https://www.goodreads.com/"
# ~2023, webpage addresses were like e.g.'best-fiction-books-2023'
# 2024 ~, the addresses are now like e.g.'readers-favorite-fiction-books-2024'
PREFIX = ["choiceawards/best", "choiceawards/readers-favorite"]
# after genre slugs, the year needs to be inserted e.g.2025
GENRES = {
    "Fiction":"fiction-books",
    "Historical Fiction":"historical-fiction-books",
    "Mystery / Thriller":"mystery-thriller-books",
    "Fantasy":"fantasy-books",
    "Science Fiction":"science-fiction-books"
}
YEARS = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 
         2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

DATA_FILE = "books.json"

app = Flask(__name__)

def scrape_all_genres():
    books = []
    # go through the data by year from 2011 - 2025
    for year in YEARS:
        if year < 2024:
            prefix = PREFIX[0]
        else:
            prefix = PREFIX[1]

        for genre, genre_url in GENRES.items():
            full_url = f"{BASE_URL}{prefix}-{genre_url}-{year}"
            response = requests.get(full_url, headers=HEADERS)

            if response.status_code != 200:
                print(f"Failed ({response.status_code}): {full_url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # each book block: <strong>votes</strong> sits directly before <a><img></a>
            # find all <strong> tags whose text contains "votes"
            vote_blocks = soup.find_all("strong", string=lambda s: s and "votes" in s)

            for rank, block in enumerate(vote_blocks, start=1):
                # votes text looks like "167,509\nvotes" — clean it up
                votes = block.get_text(strip=True).replace("votes", "").replace(",", "").strip()

                # the <img> is inside the next <a> sibling after the <strong>
                next_a = block.find_next("a")

                url = next_a["href"]
                

                img = next_a.find("img") if next_a else None

                if not img or " by " not in img.get("alt", ""):
                    continue

                alt    = img["alt"]
                parts  = alt.split(" by ", 1)
                title  = parts[0].strip()
                author = parts[1].strip()

                books.append({
                    "rank":   rank,
                    "votes":  votes,
                    "genre":  genre,
                    "year": year,
                    "title":  title,
                    "author": author,
                    "book_url":  BASE_URL+url
                })
            # print(f"Scraped {len(books)} books from {genre}")
        time.sleep(1)
        print(f"Scraped {len(books)} books from {year}")
    return books

def load_or_scrape():
    if os.path.exists(DATA_FILE):
        print("Loading from the file")
        with open(DATA_FILE) as file:
            return json.load(file)
    data = scrape_all_genres()
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)
    print(f"Saved {len(data)} books to {DATA_FILE}")
    return data

BOOK_DATA = load_or_scrape()



@app.route("/")
def home():
    return render_template("home.html", data=BOOK_DATA)

if __name__ == "__main__":
    app.run(debug=True)