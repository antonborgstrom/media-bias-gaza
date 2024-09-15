import sqlite3

# Step 1: Create SQLite database and the articles table with unique index
def create_articles_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the table with the necessary columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processed BOOLEAN DEFAULT 0,
            source TEXT,
            date TEXT,
            page TEXT,
            sektion TEXT,
            headline TEXT,
            body TEXT,
            url TEXT
        )
    ''')
    
    # Create a unique index on source, headline, and date
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_article
        ON articles (source, headline, date)
    ''')
    
    conn.commit()
    conn.close()

# Funktion för att skapa tabellen bias_sentences
def create_bias_sentences_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Skapa tabellen om den inte finns
    cursor.execute('''CREATE TABLE IF NOT EXISTS bias_sentences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        text TEXT,
        matched_type TEXT,
        matched_word TEXT,
        target_group TEXT,
        bias_score INTEGER,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )''')
    
    conn.commit()
    conn.close()

# Funktion för att skapa tabellen words_count
def create_words_count_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Skapa tabellen om den inte finns
    cursor.execute('''CREATE TABLE IF NOT EXISTS words_count (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        sentence TEXT,
        matched_word TEXT,
        target_group TEXT,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )''')
    
    conn.commit()
    conn.close()

# Funktion för att skapa tabellen emotive_words_count
def create_emotive_words_count_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Skapa tabellen om den inte finns
    cursor.execute('''CREATE TABLE IF NOT EXISTS emotive_words_count (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        sentence TEXT,
        matched_word TEXT,
        target_group TEXT,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )''')
    
    conn.commit()
    conn.close()

create_articles_table('articles.db')
create_bias_sentences_table('articles.db')
create_emotive_words_count_table('articles.db')
