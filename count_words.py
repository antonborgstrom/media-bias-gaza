import sqlite3
import re

# Lista med ord att söka efter med regex
words = [
    r'\bdödades?', r'\bdödats?', 
    r'\bmörda\w{0,3}', r'\bmord\w{0,2}',
    r'\bmassak\w{0,8}',
    r'\bmassmord\w{0,2}',
    r'\bavrätt\w{0,6}',
    r'\bslakt\w{0,5}',
    r'\bskjut\w{0,2}', r'\bsköt\w{0,1}',
    r'\bmassmörd\w{0,6}', r'\bdöds\w{1,15}', 
    r'\boffer',
    r'\bomkom\w{0,3}',
    r'\bavlid\w{0,2}',
    r'sätta livet till',
    r'\bstupa\w{0,2}',
    r'\bdöda', r'\bdör', r'\bdog'
]

# Funktion för att hitta ord i bias_sentences och spara dem i words_count
def find_and_store_word_matches():
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Hämta alla rader från bias_sentences
    cursor.execute("SELECT article_id, text, target_group FROM bias_sentences WHERE matched_type = 'Dödade'")
    sentences = cursor.fetchall()

    # För varje mening, hitta matchande ord och spara i words_count
    for article_id, sentence, target_group in sentences:
        for word in words:
            # Använd regex för att söka efter ord i meningen
            match = re.search(word, sentence, re.IGNORECASE)
            if match:
                matched_word = match.group()

                # Spara matchningen i tabellen words_count
                cursor.execute('''INSERT INTO words_count 
                    (article_id, sentence, matched_word, target_group)
                    VALUES (?, ?, ?, ?)''',
                    (article_id, sentence, matched_word, target_group))

                # Bryt loopen efter första matchning
                # break

    # Spara ändringar och stäng anslutningen
    conn.commit()
    conn.close()

# Kör funktionerna
find_and_store_word_matches()  # Hitta matchningar och spara dem
