from transformers import pipeline
import pandas as pd

print("Loading AI model... (first time takes 1-2 minutes)")

# Load free pre-trained sentiment model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

print("Model loaded successfully!")

# Load our comments
df = pd.read_csv('data/comments_clean.csv')

# Analyze each comment
print(f"\nAnalyzing {len(df)} comments...\n")

results = []
for text in df['text']:
    try:
        result = sentiment_pipeline(str(text)[:512])[0]
        results.append(result['label'])
    except:
        results.append('NEUTRAL')

df['sentiment'] = results

# Show results
print(df[['text', 'sentiment']].to_string())

# Summary
print(f"\n--- SUMMARY ---")
print(df['sentiment'].value_counts())

# Save
df.to_csv('data/comments_sentiment.csv', index=False)
print("\nSaved to data/comments_sentiment.csv!")