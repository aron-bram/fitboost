import numpy as np
import gensim.downloader

# print(list(gensim.downloader.info()['models'].keys())) # print available models
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import pickle


# Load pre-trained word2vec model
def download_embedding_model():
    # Load pre-trained model
    print("Downloading model...")
    return gensim.downloader.load("word2vec-google-news-300")


# Function to load CSV and format data
def load_csv_data(folder_path="ml-service/dataset"):
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        # Check if it's a CSV file
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            # Load data from the CSV
            try:
                # Read CSV with pandas
                data = pd.read_csv(filepath, sep=";")
                # Assuming your desired format is a list of dictionaries
                formatted_data = data.to_dict(orient="records")
            except FileNotFoundError:
                print(f"Error: File not found at {filepath}")

            # Process or print the formatted data as needed
            if formatted_data:
                print(f"Data from {filename}:")
                print(formatted_data)
                print("\n")

    return formatted_data


# Function to preprocess text (lowercase and remove punctuation and symbols)
def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text


def preprocess_data(data, embedding_model):
    # Preprocess text data
    return [
        {
            "Text": get_document_embedding(
                preprocess_text(datapoint["Text"]), embedding_model
            ),
            "Category": datapoint["Category"],
        }
        for datapoint in data
    ]


# Function to generate document embedding (average word vectors)
def get_document_embedding(text, embedding_model):
    word_vectors = []
    for word in text.split():
        if word in embedding_model.key_to_index:  # Check if word exists in vocabulary
            word_vectors.append(
                embedding_model.vectors[embedding_model.key_to_index[word]]
            )
    if word_vectors:  # Check if any words found
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(embedding_model.vector_size)  # Return zero vector for OOV words


def define_splits(data):
    texts = [d["Text"] for d in data]
    labels = [d["Category"] for d in data]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2)
    return X_train, X_test, y_train, y_test


def train(X_train, y_train):
    # Train Logistic Regression model
    classifier = LogisticRegression(multi_class="multinomial", solver="lbfgs")
    classifier.fit(X_train, y_train)
    return classifier


def test(classifier, X_test, y_test):
    # Evaluate model performance on test set (optional)
    predictions = classifier.predict(X_test)
    from sklearn.metrics import accuracy_score

    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy:", accuracy)
    return accuracy


def predict(model, embedding_model, text="Tennis club"):
    # Classify a new text sample
    data = [{"Text": text, "Category": "?"}]
    embedding = preprocess_data(data, embedding_model)[0]["Text"]
    predicted_category = model.predict([embedding])[0]
    print("Predicted category:", predicted_category)
    return predicted_category


def write(model, path="ml-service/model/classifier.pkl"):
    # Write out model to disc
    with open(path, "wb") as f:
        pickle.dump(model, f)


def load(path="ml-service/model/classifier.pkl"):
    # Load model from disc
    with open(path, "rb") as f:
        return pickle.load(f)
