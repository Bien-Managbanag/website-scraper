# Books Web Scraper

A Python web scraping project built with **Scrapy** and **MongoDB**. It collects book information from [Books to Scrape](https://books.toscrape.com/), follows pagination links across the catalogue, and stores the results in a local MongoDB database.

The project is designed to practise web scraping, data extraction, database integration, duplicate detection, and automated testing.

## Features

- Extracts each book's **title**, **price**, and **URL**.
- Follows pagination links to scrape the full catalogue (50 pages and approximately 1,000 books).
- Stores scraped data in MongoDB using a Scrapy item pipeline.
- Generates a SHA-256 identifier from each book URL and rejects duplicate records.
- Supports configurable Scrapy logging.
- Includes three unit tests for book extraction and pagination.

## Technologies

- Python
- Scrapy
- MongoDB
- PyMongo
- Python `unittest`

## Project Structure

```text
books/
├── scrapy.cfg
└── books/
    ├── __init__.py
    ├── items.py
    ├── pipelines.py
    ├── settings.py
    ├── spiders/
    │   ├── __init__.py
    │   └── book.py
    └── tests/
        ├── test_book.py
        └── sample.html
```

## Getting Started

### Prerequisites

- Python and `pip`
- MongoDB Community Server running locally
- A MongoDB shell or client (optional, for inspecting saved records)

### 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
```

Navigate to the directory containing `scrapy.cfg` before running Scrapy commands.

### 2. Install dependencies

```bash
python -m pip install scrapy pymongo
```

### 3. Configure MongoDB

Make sure your local MongoDB server is running. The scraper uses these settings in `books/settings.py`:

```python
MONGO_URI = "mongodb://localhost:27017"
MONGO_DATABASE = "books_db"

ITEM_PIPELINES = {
    "books.pipelines.MongoPipeline": 300,
}
```

The pipeline writes to the `books` collection in the `books_db` database.

### 4. Run the scraper

From the directory containing `scrapy.cfg`:

```bash
scrapy crawl book
```

The spider follows catalogue pagination automatically. A successful full crawl can scrape **1,000 book entries**.

> **Note:** The pipeline rejects books already present in MongoDB. If you run the scraper again without clearing the collection, previously saved books will be reported as duplicates rather than inserted again.

## Data Stored

Each book document contains the following fields:

| Field | Description |
| --- | --- |
| `_id` | SHA-256 hash generated from the scraped URL |
| `url` | Book link extracted from the catalogue (currently a relative URL) |
| `title` | Book title |
| `price` | Displayed price, stored as a string (e.g. `£51.77`) |

Example document:

```json
{
  "_id": "<SHA-256-HASH>",
  "url": "catalogue/a-light-in-the-attic_1000/index.html",
  "title": "A Light in the Attic",
  "price": "£51.77"
}
```

## Viewing the Results in MongoDB

Open MongoDB Shell:

```bash
mongosh
```

Select the database and count the stored books:

```javascript
use books_db
db.books.countDocuments({})
```

View five books with only their titles and prices:

```javascript
db.books.find({}, { title: 1, price: 1, _id: 0 }).limit(5)
```

## Running Unit Tests

The project uses Python's built-in `unittest` framework and a local `sample.html` fixture. The tests do not need a live website connection or MongoDB server.

From the directory containing `scrapy.cfg`, run:

```bash
python -m unittest books.tests.test_book -v
```

The three tests check that:

1. The spider extracts two books and one pagination request from the sample HTML.
2. Book titles, prices, and URLs match the expected values.
3. The pagination request points to the expected next page.

**Current result:** All three tests pass.

## Logging

Scrapy logging can be configured in `books/settings.py`:

```python
LOG_LEVEL = "WARNING"
LOG_FILE = "book_scraper.log"
```

With these settings, Scrapy writes warning-level and more severe messages to the log file instead of showing routine crawl information in the terminal. For more detailed progress output, use `LOG_LEVEL = "INFO"` and remove or comment out `LOG_FILE`.

## Potential Improvements

- Convert relative book links into absolute URLs.
- Extract additional fields such as availability and star rating.
- Store prices as numeric values for filtering and analysis.
- Add automated tests for the MongoDB pipeline and duplicate handling.
- Export the collected data to CSV or JSON.

## Acknowledgements

Data is sourced from [Books to Scrape](https://books.toscrape.com/), a demonstration website intended for web scraping practice.
