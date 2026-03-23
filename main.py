import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.goodreads.com/choiceawards/"
GENRES = {
    "Fiction":"readers-favorite-fiction-books-2025",
    "Historical Fiction":"readers-favorite-historical-fiction-books-2025",
    "Mystery / Thriller":"readers-favorite-mystery-thriller-books-2025",
    "Fantasy":"readers-favorite-fantasy-books-2025",
    "Science Fiction":"readers-favorite-science-fiction-books-2025"
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

app = Flask(__name__)

def scrape_page_by_genre(genre_name):
    genre_url = GENRES[genre_name]
    url = f"{BASE_URL}{genre_url}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"    Failed ([response.status_code]): {url}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    # each book block: <strong>votes</strong> sits directly before <a><img></a>
    # find all <strong> tags whose text contains "votes"
    vote_blocks = soup.find_all("strong", string=lambda s: s and "votes" in s)

    books = []
    for rank, block in enumerate(vote_blocks, start=1):
        # votes text looks like "167,509\nvotes" — clean it up
        votes = block.get_text(strip=True).replace("votes", "").replace(",", "").strip()

        # the <img> is inside the next <a> sibling after the <strong>
        next_a = block.find_next("a")
        img = next_a.find("img") if next_a else None

        if not img or " by " not in img.get("alt", ""):
            continue

        alt    = img["alt"]
        parts  = alt.split(" by ", 1)
        title  = parts[0].strip()
        author = parts[1].strip()

        books.append({
            "rank":   rank,
            "genre":  genre_name,
            "title":  title,
            "author": author,
            "votes":  votes
        })

    print(books)

    return books

def scrape_all_genres():
    all_books = []

    for genre, genre_url in GENRES.items():
        url = f"{BASE_URL}{genre_url}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed ({response.status_code}): {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # each book block: <strong>votes</strong> sits directly before <a><img></a>
        # find all <strong> tags whose text contains "votes"
        vote_blocks = soup.find_all("strong", string=lambda s: s and "votes" in s)

        books = []
        for rank, block in enumerate(vote_blocks, start=1):
            # votes text looks like "167,509\nvotes" — clean it up
            votes = block.get_text(strip=True).replace("votes", "").replace(",", "").strip()

            # the <img> is inside the next <a> sibling after the <strong>
            next_a = block.find_next("a")
            img = next_a.find("img") if next_a else None

            if not img or " by " not in img.get("alt", ""):
                continue

            alt    = img["alt"]
            parts  = alt.split(" by ", 1)
            title  = parts[0].strip()
            author = parts[1].strip()

            books.append({
                "rank":   rank,
                "genre":  genre,
                "title":  title,
                "author": author,
                "votes":  votes
            })

        all_books.extend(books)
        # print(f"Scraped {len(books)} books from {genre}")
        time.sleep(2)

    return all_books

scrape_page_by_genre("Fantasy")
scrape_all_genres()
