import sqlite3
import re
import argparse
import json

# Step 2: Parse the text file and extract articles
def parse_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position of the first occurrence of "Nyheter:"
    nyheter_pos = content.find("Nyheter:")
    
    if nyheter_pos == -1:
        print("No 'Nyheter:' section found in the file.")
        return []

    # Extract everything after "Nyheter:"
    articles_section = content[nyheter_pos + len("Nyheter:"):].strip()
    
    # Split the articles section by the separator for each article
    articles = articles_section.split("==============================================================================")
    
    parsed_articles = []
    
    for article in articles:
        # Extract source and date (found on the first line)
        header_match = re.search(r'^(.*?), (\d{4}-\d{2}-\d{2})$', article.strip(), re.MULTILINE)
        if not header_match:
            continue

        source = header_match.group(1).strip()
        date = header_match.group(2).strip()
        
        # Extract the page number(s)
        page_match = re.search(r'^Sida\s([\d, ]+)$', article.strip(), re.MULTILINE)
        if page_match:
            page_numbers = [int(num) for num in page_match.group(1).replace(' ', '').split(',')]
            page_json = json.dumps(page_numbers)
        else:
            page_json = json.dumps([])  # Empty JSON array if page numbers are not found

        # Extract the headline (first line of the article)
        headline_match = re.search(r'^(.*?)$', article.strip(), re.MULTILINE)
        headline = headline_match.group(1).strip() if headline_match else ""
        
        # Extract the body: between "Publicerat i print." and the last occurrence of "©"
        body_start_pos = article.find("Publicerat i print.")
        body_end_pos = article.rfind("©")
        
        if body_start_pos != -1 and body_end_pos != -1 and body_start_pos < body_end_pos:
            body_content = article[body_start_pos + len("Publicerat i print."):body_end_pos].strip()
        else:
            body_content = ""  # If the pattern isn't found correctly, body remains empty

        # Remove line breaks from the body
        body = body_content.replace('\n', ' ').strip()

        # Extract the URL (last occurrence in the article)
        url_match = re.search(r'(http[s]?://\S+)', article)
        url = url_match.group(1).strip() if url_match else ""
        
        parsed_articles.append((source, date, headline, body, url, page_json))
    
    return parsed_articles

# Step 3: Insert articles into the database and print headlines of successful insertions
def insert_articles_to_db(articles):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    
    for article in articles:
        try:
            cursor.execute('''
                INSERT INTO articles (source, date, headline, body, url, page)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', article)
            # Print the headline of the inserted article
            print(f"Inserted article: {article[2]}")
        except sqlite3.IntegrityError:
            # Handle the case where the unique constraint is violated
            print(f"Article already exists in the database: {article[2]}")
    
    conn.commit()
    conn.close()

# Step 4: Run the script
def main():
    # Setup argument parser to accept filename from the command line
    parser = argparse.ArgumentParser(description='Process and store articles from a text file into an SQLite database.')
    parser.add_argument('filename', type=str, help='The path to the input text file with articles')
    args = parser.parse_args()

    articles = parse_articles(args.filename)
    insert_articles_to_db(articles)
    print(f"Processed {len(articles)} articles.")

# Run the script
if __name__ == "__main__":
    main()
