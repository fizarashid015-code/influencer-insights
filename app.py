from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

print("Loading AI model...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)
print("Model ready!")

LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL", 
    "LABEL_2": "POSITIVE"
}

@app.route('/')
def home():
    return jsonify({
        "message": "Influencer Insights API is running!",
        "usage": "POST /analyze with {'comments': ['comment1', 'comment2']}"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    comments = data.get('comments', [])
    
    if not comments:
        return jsonify({'error': 'No comments provided'}), 400
    
    results = sentiment_pipeline(
        comments, truncation=True, max_length=512
    )
    
    positive = sum(1 for r in results if r['label'] == 'LABEL_2')
    negative = sum(1 for r in results if r['label'] == 'LABEL_0')
    neutral  = len(results) - positive - negative
    
    details = [
        {"comment": c, "sentiment": LABEL_MAP[r['label']], "score": round(r['score'], 2)}
        for c, r in zip(comments, results)
    ]
    
    return jsonify({
        'total': len(comments),
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'details': details
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)