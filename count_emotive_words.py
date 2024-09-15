import sqlite3
import re

# Lista med känslomässigt laddade ord att söka efter med regex
emotive_words = [
    r'\bmassak\w{0,8}',
    r'\bmassmord\w{0,3}',
    r'\bmassmörd\w{0,5}',
    r'\bmörda\w{0,5}', 
    r'\bmord\w{0,3}',
    r'\bslakt\w{0,5}',
    r'\bblod\w{0,4}',
    r'\bbrutal\w{0,4}',
    r'\bavrätt\w{0,6}',
    r'\burskillningslös\w{0,1}',
    r'\bfolkmord\w{0,2}',
    r'\butplåna\w{0,3}'
]

# Funktion för att hitta känslomässigt laddade ord i bias_sentences och spara dem i emotive_words_count
def find_and_store_emotive_word_matches():
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Hämta alla rader från bias_sentences
    cursor.execute("SELECT article_id, text, target_group FROM bias_sentences WHERE matched_type = 'Dödade'")
    sentences = cursor.fetchall()

    # För varje mening, hitta matchande känslomässiga ord och spara i emotive_words_count
    for article_id, sentence, target_group in sentences:
        for word in emotive_words:
            # Använd regex för att söka efter ord i meningen, med flaggan re.IGNORECASE för att ignorera skiftläge
            match = re.search(word, sentence, re.IGNORECASE)
            if match:
                matched_word = match.group()

                # Spara matchningen i tabellen emotive_words_count
                cursor.execute('''INSERT INTO emotive_words_count 
                    (article_id, sentence, matched_word, target_group)
                    VALUES (?, ?, ?, ?)''',
                    (article_id, sentence, matched_word, target_group))

                # Bryt loopen efter första matchning
                # break

    # Spara ändringar och stäng anslutningen
    conn.commit()
    conn.close()

# Kör funktionerna
find_and_store_emotive_word_matches()  # Hitta känslomässiga matchningar och spara dem
