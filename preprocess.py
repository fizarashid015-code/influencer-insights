import re
import nltk
import pandas as pd

# Download required nltk data
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

def clean_comment(text):
    text = str(text)
    text = re.sub(r'<.*?>', '', text)        # Remove HTML tags
    text = re.sub(r'http\S+', '', text)      # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove special chars
    text = text.lower().strip()              # Lowercase
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)

# Load comments
df = pd.read_csv('data/comments.csv')

print(f"Total comments: {len(df)}")
print(f"Sample before cleaning:\n{df['text'][0]}\n")

# Clean all comments
df['clean_text'] = df['text'].apply(clean_comment)

print(f"Sample after cleaning:\n{df['clean_text'][0]}\n")

# Save cleaned data
df.to_csv('data/comments_clean.csv', index=False)
print("Saved cleaned comments to data/comments_clean.csv!")