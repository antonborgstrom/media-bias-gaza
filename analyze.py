import os
import sqlite3
from openai import OpenAI
from pydantic import BaseModel
from textwrap3 import dedent
from enum import Enum
from dotenv import load_dotenv

class TargetGroup(str, Enum):
    palestinian = "Palestinian"
    israeli = "Israeli"

class MatchedType(str, Enum):
    dödade = "Dödade"
    kidnappade = "Kidnappade"
    hat = "Hat"

class ArticleSummary(BaseModel):
    class Sentence(BaseModel, use_enum_values=True):
        sentence: str
        matched_word: str
        matched_type: MatchedType
        target_group: TargetGroup
        bias_score: int

    centences: list[Sentence]

# Funktion för att hämta artiklar
def fetch_articles(db):
    cursor = db.cursor()
    
    # Hämta alla artiklar
    cursor.execute("SELECT id, body FROM articles WHERE id IN (SELECT id FROM articles ORDER BY RANDOM() LIMIT 500) AND processed != 1")
    articles = cursor.fetchall()
    
    return articles

# Funktion för att analysera artikel med instruktioner till OpenAI
def analyze_article(text: str, ai_client):

    summarization_prompt = '''
        Du är en expert på att analysera mediepartiskhet.
        Du kommer att få en nyhetsartikel om konflikten mellan Israel och Palestina.
        Identifiera alla meningar i artikeln som:
        1. Refererar till palestinier/gazabor eller israeler som dödats, mördats, slaktats, massakrerats, massmördats, etc.
        2. Refererar till palestinier/gazabor eller israeler som kidnappats.
        3. Refererar till antisemitism/judehat eller islamofobi/muslimhat.
        Målet är att återge alla sådana meningar enligt den bifogade strukturen och identifiera om meningen refererar till palestinier/gazabor eller israeler, respektive antisemetism eller islamofobi.
        Här är en beskrivning av alla prametrar:
        - sentence: Meningen som identifierats.
        - matched_type: Vilken av de tre kategorierna ovan som identifierats (dödade, kidnappade eller hat)
        - matched_word: Ord som används i meningen för att beskriva dödsfallen, kidnappningen eller hatet (t.ex. dödade, mördade, slaktade, kidnappade, gisslan, antisemitism, islamofobi, etc.).
        - target_group: Gruppen som åsyftas i meningen (palestinier eller israeler).
        - bias_score: En partiskhetsbedömning från 1 till 10 som representerar hur känsloladdad eller partisk meningen är, där 1 är krasst beskrivande utan laddning eller värderande tonfall och 10 är emotionellt och värderingsmässigt laddat.
    '''

    completion = ai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        temperature=0.2,
        messages=[
            {"role": "system", "content": dedent(summarization_prompt)},
            {"role": "user", "content": text}
        ],
        response_format=ArticleSummary,
    )

    return completion.choices[0].message.parsed

# Spara mening i databastabellen bias_sentences
def store_sentence(db, article_id, sentence: ArticleSummary):

    cursor = db.cursor()

    cursor.execute('''INSERT INTO bias_sentences 
        (article_id, text, matched_type, matched_word, target_group, bias_score) 
        VALUES (?, ?, ?, ?, ?, ?)''', 
        (article_id, sentence.sentence, sentence.matched_type, sentence.matched_word, sentence.target_group, sentence.bias_score))

    # Update the processed column to 1 to avoid rerun 
    cursor.execute(f"UPDATE articles SET processed = 1 WHERE id = ?", (article_id,))

    db.commit()

    print(f"Sentence: {sentence.sentence}\n")
    print(f"Matched type: {sentence.matched_type}\n")
    print(f"Matched word: {sentence.matched_word}\n")
    print(f"Target: {sentence.target_group}\n")
    print(f"Bias: {sentence.bias_score}\n")
    print(f"-------------------------\n")

# Huvudfunktion för att köra analysen
def analyze_articles():

    db = sqlite3.connect('articles.db')

    articles = fetch_articles(db)

    # Ladda miljövariabler från .env-filen
    load_dotenv()

    # Hämta OpenAI API-nyckeln från miljövariabeln
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    if client.api_key is None:
        raise ValueError("OpenAI API-nyckel hittades inte. Se till att ställa in OPENAI_API_KEY i din .env-fil.")

    for article_id, body in articles:
        returned_sentences = analyze_article(body, client)
        print(f"\nARTICLE {article_id}\n")

        for sentence in returned_sentences.centences:
            store_sentence(db, article_id, sentence)
    
    db.close()

# Kör programmet
analyze_articles()
