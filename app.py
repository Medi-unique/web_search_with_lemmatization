import streamlit as st
import pandas as pd
from utils import vectorize_content, calculate_phrase_scores, rank_phrases
from processing import extract_file_content, extract_web_content, preprocess_text  # Updated import
# Configure page
st.set_page_config(
    page_title="Phrase-Level Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Search Settings")
    num_results = st.slider("Number of Results", 1, 20, 10)
    threshold = st.slider("Minimum Confidence", 0.0, 1.0, 0.15)
    st.markdown("---")
    st.info("Upload documents or enter website URLs to search through")

# Main interface
st.title("🔍 Phrase-Level Content Search")
st.markdown("---")

# Main search bar
query = st.text_input(
    "",
    placeholder="Enter your search query...",
    key="main_search",
    help="Search for specific phrases or concepts"
)

# File upload section
with st.expander("📤 Upload Documents", expanded=True):
    upload_col, title_col = st.columns([3, 1])
    with upload_col:
        uploaded_files = st.file_uploader(
            "Select PDF/DOCX files",
            accept_multiple_files=True,
            type=['pdf', 'docx'],
            label_visibility='collapsed'
        )
    with title_col:
        custom_titles = st.text_input(
            "Custom Titles (comma-separated)",
            help="Optional titles for uploaded files"
        )

# URL input section
with st.expander("🌐 Add Websites", expanded=False):
    website_links = st.text_area(
        "Enter website URLs (one per line)",
        height=100,
        placeholder="https://example.com\nhttps://another-site.org",
        label_visibility='collapsed'
    )

# Process inputs
if uploaded_files or website_links:
    # Process files
    titles = [t.strip() for t in custom_titles.split(',')] if custom_titles else []
    for idx, file in enumerate(uploaded_files):
        title = titles[idx] if idx < len(titles) else None
        doc = extract_file_content(file, title)
        if doc:
            st.session_state.documents.append(doc)

    # Process URLs
    if website_links:
        for url in website_links.strip().split('\n'):
            if url:
                doc = extract_web_content(url)
                if doc:
                    st.session_state.documents.append(doc)

# Search execution
if query and st.session_state.documents:
    # Vectorize content
    vectorizer, tfidf_matrix, meta_data = vectorize_content(st.session_state.documents)
    
    # Process query
    processed_query = ' '.join(preprocess_text(query).split())  # Use processing.py's preprocess_text
    query_vector = vectorizer.transform([processed_query])
    
    # Calculate scores
    scores = calculate_phrase_scores(query_vector, tfidf_matrix)
    
    # Get ranked results
    results = rank_phrases(scores, meta_data, num_results, threshold)
    
    # Display results
    st.subheader(f"🔢 Top {len(results)} Matching Phrases")
    for idx, (_, row) in enumerate(results.iterrows()):
        st.markdown(f"""
        ### {idx+1}. Score: `{row['score']:.2%}`
        **Source:** {'🌐 ' + row['url'] if row['source'] == 'web' else '📄 ' + row['title']}
        """)
        st.markdown(f"**Matched Phrase:** {row['sentence']}")
        st.markdown("---")
elif query:
    st.warning("No documents/websites uploaded yet!")
else:
    st.info("ⓘ Upload documents/websites and enter a query to start searching")
    
    
    