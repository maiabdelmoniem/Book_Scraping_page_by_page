# 📚 Book Scraping (Page-by-Page)

A beginner-friendly Python project that scrapes book data (title, price, stock...) from [Books to Scrape](http://books.toscrape.com), going through each page one by one.

---

## 🔍 Features

- **Page-by-page scraping** of book listings using the file individual_bookscraping.py
- Extracts:
  - **Title**
  - **Price**
  - **Stock availability**
  - **Author**
  - **Price incl. tax**
  - **Price excl. tax**
  - **Star Rating**
  - **Description**
  - **Book Page**



- Saves the data in three formats:
  - `books_data.json`
  - `books_data.csv`
  - `books_data.xlsx`

---

## 🛠️ Requirements

- Python 3.7+
- `pandas`
- `requests`
- `beautifulsoup4`


## Transformation

Data is then cleaned and transformed into an SQLite Database (databasebooks.db) with a star schema using the file erdtransformsql.py

## Loading 

Data is then Loaded into the database using the file table_populating.py
