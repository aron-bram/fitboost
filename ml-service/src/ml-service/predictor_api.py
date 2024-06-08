import numpy as np
import gensim.downloader
print(list(gensim.downloader.info()['models'].keys()))
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import os

# Load pre-trained word2vec model (replace with your preferred model path)
model = gensim.downloader.load("word2vec-google-news-300")  # Load pre-trained model

# Sample data (replace with your actual data)
# Specify the folder path (replace with your actual folder path)
folder_path = "ml-service/dataset"

# Function to load CSV and format data
def load_csv_data(filepath):
  try:
    # Read CSV with pandas
    data = pd.read_csv(filepath, sep=";")
    # Assuming your desired format is a list of dictionaries
    formatted_data = data.to_dict(orient='records')
    return formatted_data
  except FileNotFoundError:
    print(f"Error: File not found at {filepath}")

# Iterate through files in the folder
for filename in os.listdir(folder_path):
  # Check if it's a CSV file
  if filename.endswith(".csv"):
    filepath = os.path.join(folder_path, filename)
    # Load data from the CSV
    formatted_data = load_csv_data(filepath)
    
    # Process or print the formatted data as needed
    if formatted_data:
      print(f"Data from {filename}:")
      print(formatted_data)
      print("\n")


# Function to preprocess text (lowercase and remove punctuation and symbols)
def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text

# Preprocess text data
texts = [preprocess_text(datapoint["Text"]) for datapoint in formatted_data]
labels = [datapoint["Category"] for datapoint in formatted_data]

# Function to generate document embedding (average word vectors)
def get_document_embedding(text, model):
    word_vectors = []
    for word in text.split():
        if word in model.key_to_index:  # Check if word exists in vocabulary
            word_vectors.append(model.vectors[model.key_to_index[word]])
    if word_vectors:  # Check if any words found
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)  # Return zero vector for OOV words

# Generate document embeddings
embeddings = [get_document_embedding(text, model) for text in texts]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2)

# Train Logistic Regression model
classifier = LogisticRegression(multi_class="multinomial", solver="lbfgs")
classifier.fit(X_train, y_train)

# Evaluate model performance on test set (optional)
predictions = classifier.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# Classify a new text sample (optional)
new_text = "Tennis club"
new_embedding = get_document_embedding(new_text, model)
predicted_category = classifier.predict([new_embedding])[0]
print("Predicted category:", predicted_category)
