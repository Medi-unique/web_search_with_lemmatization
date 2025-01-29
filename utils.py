import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def vectorize_content(documents):
    """Vectorize all sentences from all documents"""
    all_sentences = []
    meta_data = []
    
    for doc in documents:
        for sent, original_sent in zip(doc['sentences'], doc['original_sentences']):
            all_sentences.append(sent)
            meta_data.append({
                'title': doc['title'],
                'original_sentence': original_sent,
                'source': doc['source'],
                'url': doc.get('url', '')
            })
    
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=15000,
        sublinear_tf=True,
        smooth_idf=True
    )
    tfidf_matrix = vectorizer.fit_transform(all_sentences)
    return vectorizer, tfidf_matrix, meta_data

def calculate_phrase_scores(query_vector, tfidf_matrix):
    """Calculate similarity scores for all phrases"""
    return cosine_similarity(query_vector, tfidf_matrix).flatten()

def rank_phrases(scores, meta_data, num_results=5, threshold=0.1):
    """Rank phrases with their metadata"""
    df = pd.DataFrame({
        'score': scores,
        'title': [m['title'] for m in meta_data],
        'sentence': [m['original_sentence'] for m in meta_data],
        'source': [m['source'] for m in meta_data],
        'url': [m['url'] for m in meta_data]
    })
    
    filtered = df[df['score'] >= threshold]
    return filtered.sort_values('score', ascending=False).head(num_results)