from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

print("Loading AI model...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Model ready!")

@app.route('/')
def home():
    return jsonify({"message": "Influencer Insights API is running!"})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    comments = data.get('comments', [])
    if not comments:
        return jsonify({'error': 'No comments provided'}), 400
    results = sentiment_pipeline(comments, truncation=True, max_length=512)
    positive = sum(1 for r in results if r['label'] == 'POSITIVE')
    negative = sum(1 for r in results if r['label'] == 'NEGATIVE')
    neutral = len(results) - positive - negative
    return jsonify({
        'total': len(comments),
        'positive': positive,
        'negative': negative,
        'neutral': neutral
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)