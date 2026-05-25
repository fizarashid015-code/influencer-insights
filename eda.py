import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load cleaned data
df = pd.read_csv('data/comments_clean.csv')

print(f"Total comments: {len(df)}")
print(f"\nTop 5 comments:\n{df['text'].head()}")

# 1. Word Cloud
text = ' '.join(df['clean_text'].dropna())
wc = WordCloud(width=800, height=400, 
               background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wc)
plt.axis('off')
plt.title('Most Common Words in Comments')
plt.savefig('wordcloud.png')
plt.show()
print("Saved wordcloud.png!")

# 2. Comment Length Distribution
df['length'] = df['text'].apply(len)

plt.figure(figsize=(8, 4))
df['length'].hist(bins=20, color='steelblue')
plt.title('Comment Length Distribution')
plt.xlabel('Number of Characters')
plt.ylabel('Number of Comments')
plt.savefig('length_dist.png')
plt.show()
print("Saved length_dist.png!")

# 3. Basic Stats
print(f"\nAverage comment length: {df['length'].mean():.0f} characters")
print(f"Longest comment: {df['length'].max()} characters")
print(f"Shortest comment: {df['length'].min()} characters")