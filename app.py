import os
from flask import Flask, request, jsonify, render_template
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Initialize Flask App
app = Flask(__name__)

# Get Azure AI Language credentials from environment variables
# We will set these in Azure App Service configuration later
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# Authenticate the client
text_analytics_client = TextAnalyticsClient(
    endpoint=language_endpoint,
    credential=AzureKeyCredential(language_key)
)

@app.route('/')
def index():
    """Renders the frontend HTML page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyzes the text using Azure AI Language."""
    try:
        data = request.get_json()
        text_to_analyze = data.get('text')

        if not text_to_analyze:
            return jsonify({"error": "No text provided"}), 400

        documents = [text_to_analyze]

        # 1. Analyze Sentiment
        sentiment_result = text_analytics_client.analyze_sentiment(documents=documents)[0]
        sentiment = {
            "overall": sentiment_result.sentiment,
            "scores": {
                "positive": f"{sentiment_result.confidence_scores.positive:.2f}",
                "neutral": f"{sentiment_result.confidence_scores.neutral:.2f}",
                "negative": f"{sentiment_result.confidence_scores.negative:.2f}",
            }
        }

        # 2. Extract Key Phrases
        key_phrases_result = text_analytics_client.extract_key_phrases(documents=documents)[0]
        key_phrases = key_phrases_result.key_phrases if not key_phrases_result.is_error else []

        # 3. Recognize Entities
        entities_result = text_analytics_client.recognize_entities(documents=documents)[0]
        entities = [{"text": entity.text, "category": entity.category} for entity in entities_result.entities]

        # Simple Summary (First Sentence)
        summary = text_to_analyze.split('.')[0] + '.'

        # Combine all results
        response_data = {
            "summary": summary,
            "sentiment": sentiment,
            "key_phrases": key_phrases,
            "entities": entities
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)