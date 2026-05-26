from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def home():
    return "Influencer Insights API is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    comments = data.get('comments', [])
    if not comments:
        return {"error": "No comments provided"}, 400

    positive, negative, neutral = 0, 0, 0
    details = []
    for comment in comments:
        score = TextBlob(comment).sentiment.polarity
        if score > 0.1:
            sentiment = "POSITIVE"
            positive += 1
        elif score < -0.1:
            sentiment = "NEGATIVE"
            negative += 1
        else:
            sentiment = "NEUTRAL"
            neutral += 1
        details.append({"comment": comment, "sentiment": sentiment})

    return {"total": len(comments), "positive": positive,
            "negative": negative, "neutral": neutral, "details": details}

if __name__ == '__main__':
    app.run(debug=True, port=5000)