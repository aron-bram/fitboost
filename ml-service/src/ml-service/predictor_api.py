import predictor
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
# allow CORS for all routes
CORS(app)


@app.route("/classify", methods=["POST"])
def classify_text():
    # Get text from request
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing text in request body"}), 400

    text = data["text"]
    text = predictor.preprocess_text(text)
    embedding = predictor.get_document_embedding(text, embedding_model)

    # Classify text using loaded model
    prediction = model.predict([embedding])[0]

    return jsonify({"text": text, "category": prediction})


if __name__ == "__main__":
    embedding_model = predictor.download_embedding_model()
    model = predictor.load()
    app.run(port=5001, debug=True)
