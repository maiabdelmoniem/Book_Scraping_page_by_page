import sqlite3
import pandas as pd

conn = sqlite3.connect('databasebooks.db')
cur = conn.cursor()

# Load CSV into DataFrame
df = pd.read_csv('cleaned_data.csv')
# print(df.columns)

# Populate dim_product_type
product_types = df['Category'].dropna().unique()
for pt in product_types:
    cur.execute("INSERT OR IGNORE INTO dim_product_type (category) VALUES (?)", (pt,))
    #print(pt)

# Populate dim_availability
availabilities = df['Availability'].dropna().unique()
for av in availabilities:
    cur.execute("INSERT OR IGNORE INTO dim_availability (availability) VALUES (?)", (int(av),))


# Populate dim_book
books = df[[ 'Title', 'Description', 'UPC', 'Product Page URL']].drop_duplicates(subset=['UPC'])
for _, row in books.iterrows():
    cur.execute("""
        INSERT OR IGNORE INTO dim_book (title, description, upc, product_page) 
        VALUES (?, ?, ?, ?)
    """, ( row['Title'], row['Description'], row['UPC'], row['Product Page URL']))
conn.commit()

# Populate fact_book_sales
for _, row in df.iterrows():
    cur.execute("SELECT book_id FROM dim_book WHERE upc = ?", (row['UPC'],))
    book_id = cur.fetchone()
    if not book_id:
        continue
    book_id = book_id[0]

    cur.execute("SELECT product_type_id FROM dim_product_type WHERE category = ?", (row['Category'],))
    product_type_id = cur.fetchone()
    product_type_id = product_type_id[0] if product_type_id else None

    cur.execute("SELECT availability_id FROM dim_availability WHERE availability = ?", (row['Availability'],))
    availability_id = cur.fetchone()
    availability_id = availability_id[0] if availability_id else None

    cur.execute("""
        INSERT INTO fact_book_sales (
            book_id, product_type_id, availability_id,
            price_excl_tax, price_incl_tax, tax,
            stock_quantity, number_of_reviews, star_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id, product_type_id, availability_id,
        row['Price (excl. tax)'], row['Price (incl. tax)'], row['Tax'],
        row['Stock (Scraped)'], row['Number of Reviews'], row['Star Rating']
    ))

conn.commit()
conn.close()


