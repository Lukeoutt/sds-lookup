import sqlite3

DB_PATH = 'sds_data.db'

sample_products = [
    ('CleanerX', 'CX-123', 'USA', 'English', 'SDS001'),
    ('DegreaserPro', 'DP-456', 'Canada', 'French', 'SDS002'),
    ('ShinySurface', 'SS-789', 'USA', 'Spanish', 'SDS003'),
    ('CleanerX', 'CX-999', 'USA', 'English', 'SDS004'),
    ('WipeItAll', 'WI-101', '', '', 'SDS005')  # No country/language
]

sample_sds_files = [
    ('SDS001', 'https://example.com/sds001.pdf'),
    ('SDS002', 'https://example.com/sds002.pdf'),
    ('SDS003', 'https://example.com/sds003.pdf'),
    ('SDS004', 'https://example.com/sds004.pdf'),
    ('SDS005', 'https://example.com/sds005.pdf')
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for p in sample_products:
    c.execute('INSERT INTO products (product_name, product_number, country, language, sds_number) VALUES (?, ?, ?, ?, ?)', p)

for f in sample_sds_files:
    c.execute('INSERT INTO sds_files (sds_number, file_url) VALUES (?, ?)', f)

conn.commit()
conn.close()

print("Sample data inserted successfully.")
