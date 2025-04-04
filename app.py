from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
DB_PATH = 'sds_data.db'

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Product metadata table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT,
                    product_number TEXT,
                    country TEXT,
                    language TEXT,
                    sds_number TEXT
                )''')

    # SDS file table
    c.execute('''CREATE TABLE IF NOT EXISTS sds_files (
                    sds_number TEXT PRIMARY KEY,
                    file_url TEXT
                )''')

    conn.commit()
    conn.close()

# Call DB setup on start
init_db()

# --- API Endpoint ---
@app.route('/get-sds', methods=['GET'])
def get_sds():
    product_name = request.args.get('product_name')
    product_number = request.args.get('product_number')
    country = request.args.get('country')
    language = request.args.get('language')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''SELECT sds_number FROM products
                 WHERE product_name=? AND product_number=? AND country=? AND language=?''',
              (product_name, product_number, country, language))
    result = c.fetchone()
    
    if not result:
        return jsonify({'error': 'No matching SDS found'}), 404

    sds_number = result[0]
    c.execute('SELECT file_url FROM sds_files WHERE sds_number=?', (sds_number,))
    file_result = c.fetchone()

    conn.close()

    if not file_result:
        return jsonify({'error': 'SDS file not found'}), 404

    return jsonify({'sds_url': file_result[0]}), 200

# --- UI Form ---
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
