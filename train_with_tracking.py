import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load sentiment data
df = pd.read_csv('data/comments_sentiment.csv')
df = df.dropna(subset=['clean_text', 'sentiment'])

# Prepare data
vectorizer = TfidfVectorizer(max_features=500)
X = vectorizer.fit_transform(df['clean_text'])

le = LabelEncoder()
y = le.fit_transform(df['sentiment'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Track with MLflow
mlflow.set_experiment("influencer-insights")

with mlflow.start_run():
    # Train model
    model = LogisticRegression(C=1.0, max_iter=200)
    model.fit(X_train, y_train)

    # Evaluate
    acc = accuracy_score(y_test, model.predict(X_test))

    # Log to MLflow
    mlflow.log_param("C", 1.0)
    mlflow.log_param("max_iter", 200)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    print(f"Accuracy: {acc:.2f}")
    print("Logged to MLflow!")

print("\nTo view dashboard run: mlflow ui")