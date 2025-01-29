import re
import string
from PyPDF2 import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import requests
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

nltk.download(['stopwords', 'punkt', 'wordnet'], quiet=True)

# Initialize NLP components
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english') + [
    'please', 'thank', 'hello', 'hi', 'could', 'would', 'might'
])

def preprocess_text(text):
    """Full text cleaning pipeline"""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower().strip()
    tokens = text.split()
    return ' '.join([lemmatizer.lemmatize(token) for token in tokens if token not in stop_words])

def split_into_sentences(text):
    """Split text into sentences using spaCy"""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

def extract_file_content(file, custom_title=None):
    """Process uploaded files with sentence splitting"""
    try:
        if file.name.endswith('.pdf'):
            reader = PdfReader(file)
            raw_text = ' '.join([page.extract_text() for page in reader.pages])
        elif file.name.endswith('.docx'):
            doc = Document(file)
            raw_text = ' '.join([para.text for para in doc.paragraphs])
        else:
            return None

        sentences = split_into_sentences(raw_text)
        return {
            'title': custom_title or file.name,
            'content': raw_text,
            'sentences': [preprocess_text(sent) for sent in sentences],
            'original_sentences': sentences,
            'source': 'file'
        }
    except Exception as e:
        print(f"Error processing {file.name}: {str(e)}")
        return None

def extract_web_content(url):
    """Web extraction with sentence splitting"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')

        title = soup.find('title').text.strip() if soup.find('title') else url
        paragraphs = soup.find_all('p')
        raw_text = ' '.join([p.get_text().strip() for p in paragraphs])

        sentences = split_into_sentences(raw_text)
        return {
            'title': title,
            'content': raw_text,
            'sentences': [preprocess_text(sent) for sent in sentences],
            'original_sentences': sentences,
            'source': 'web',
            'url': url
        }
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None