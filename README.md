# Medi-Unique Web Search with Lemmatization

## Overview
Medi-Unique Web Search with Lemmatization is an advanced content search application built using Streamlit. It allows users to upload documents (PDF, DOCX) or enter website URLs to search through. The application preprocesses the text content, vectorizes it using TF-IDF, and calculates cosine similarities to rank search results based on user queries.

## Features
- **Upload Documents**: Supports PDF and DOCX file uploads.
- **Web Content Search**: Allows users to enter website URLs for content extraction.
- **Advanced Search Settings**: Customize the number of results and minimum confidence threshold.
- **Text Preprocessing**: Cleans and preprocesses text using lemmatization.
- **Vectorization**: Uses TF-IDF vectorizer to convert text into numerical vectors.
- **Similarity Calculation**: Calculates cosine similarity between query and document vectors.
- **Result Ranking**: Ranks documents based on relevance to the search query.

## Demo
Watch the demo video to see how the Medi-Unique Web Search application works in action.

[Demo Video](#) *https://www.youtube.com/watch?v=P-FsBJVhxuk*


## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/medi-unique-web-search-with-lemmatization.git
    cd medi-unique-web-search-with-lemmatization
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/Scripts/activate  # On Windows
    source .venv/bin/activate      # On macOS/Linux
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## Usage
1. **Upload Documents**: Click on the "Browse files" button to upload PDF or DOCX files.
2. **Enter Website URLs**: Enter the URLs of the websites you want to search through.
3. **Set Search Parameters**: Use the sliders to set the number of results and minimum confidence threshold.
4. **Enter Search Query**: Type your search query in the main search bar.
5. **View Results**: The application will display the most relevant results based on your query.

## Technical Details

### Text Preprocessing
The text preprocessing step involves cleaning and normalizing the text data. This includes:
- Removing non-ASCII characters, numbers, and punctuation.
- Converting text to lowercase.
- Removing stopwords.
- Lemmatization: Reducing words to their base or root form using the spaCy library.

### Vectorization
The TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer is used to convert the text into numerical vectors. This helps in representing the importance of words in the documents relative to the entire corpus.

### Cosine Similarity
Cosine similarity is used to measure the similarity between the query vector and document vectors. It calculates the cosine of the angle between two vectors, providing a similarity score between 0 and 1.

### Result Ranking
The documents are ranked based on their cosine similarity scores. The results are filtered based on the minimum confidence threshold set by the user and displayed in descending order of relevance.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Streamlit
- scikit-learn
- spaCy
