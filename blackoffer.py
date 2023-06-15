import os
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob
import syllables

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Perform stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    lemma_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Join tokens back into a string
    stemmed_text = ' '.join(stemmed_tokens)
    lemma_text = ' '.join(lemma_tokens)
    return stemmed_text, lemma_text

# Function to extract article content from a URL
def extract_article_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "XY"})
        response.raise_for_status()
        html_content = response.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract the article text
        article_text = ""
        article_elements = soup.select('article p')
        if article_elements:
            article_text = ' '.join([elem.get_text().strip() for elem in article_elements])
        return article_text
    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching the URL:", e)
        return ""

# Define the input and output filenames
input_filename = 'Input.xlsx'
output_filename = 'Output.xlsx'

# Load the input data
input_data = pd.read_excel(input_filename)

# Create empty lists to store the output data
output_data = []

for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    # Extract article content
    article_text = extract_article_content(url)
    
    # Preprocess text
    stemmed_text, lemmatized_text = preprocess_text(article_text)
    
    # Perform text analysis
    blob = TextBlob(article_text)
    
    # Compute variables
    positive_score = blob.sentiment.polarity
    negative_score = -blob.sentiment.polarity
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    
    sentences = nltk.sent_tokenize(article_text)
    if len(sentences) > 0:
        avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
        words = nltk.word_tokenize(article_text)
        word_count = len(words)
        avg_words_per_sentence = word_count / len(sentences)
    else:
        avg_sentence_length = 0
        avg_words_per_sentence = 0
    
    syllable_count = sum(syllables.estimate(word) for word in words)
    syllables_per_word = syllable_count / word_count if word_count != 0 else 0
    
    personal_pronoun_count = sum(1 for word in words if word.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'])
    
    avg_word_length = sum(len(word) for word in words) / word_count if word_count != 0 else 0
    
    # Compute other variables
    complex_words = [word for word in words if len(word) > 2 and syllables.estimate(word) > 2]
    percentage_complex_words = (len(complex_words) / word_count) * 100 if word_count != 0 else 0
    
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    # Append the output data to the list
    output_data.append([
        url_id, url, stemmed_text, lemmatized_text, positive_score, negative_score, polarity_score,
        subjectivity_score, avg_sentence_length, avg_words_per_sentence, word_count, syllable_count,
        syllables_per_word, personal_pronoun_count, len(complex_words)
    ])

# Create a dataframe from the output data
output_df = pd.DataFrame(output_data, columns=[
    'URL_ID', 'URL', 'Stemmed_Text', 'Lemmatized_Text', 'Positive_Score', 'Negative_Score', 'Polarity_Score',
    'Subjectivity_Score', 'Avg_Sentence_Length', 'Avg_Words_Per_Sentence', 'Word_Count', 'Syllable_Count',
    'Syllables_Per_Word', 'Personal_Pronoun_Count', 'Complex_Word_Count'
])

# Save the output dataframe to Excel
output_df.to_excel(output_filename, index=False)

print("Data analysis completed and saved to", output_filename)
