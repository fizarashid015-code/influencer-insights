import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv('data/comments_sentiment.csv')
df = df.dropna(subset=['clean_text', 'sentiment'])

vectorizer = TfidfVectorizer(max_features=500)
X = vectorizer.fit_transform(df['clean_text'])
le = LabelEncoder()
y = le.fit_transform(df['sentiment'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.set_experiment("influencer-insights")

with mlflow.start_run(run_name="best-model"):
    # Use best params from Optuna
    model = LogisticRegression(C=6.906, max_iter=182)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    
    mlflow.log_param("C", 6.906)
    mlflow.log_param("max_iter", 182)
    mlflow.log_metric("accuracy", acc)
    
    # Register model
    mlflow.sklearn.log_model(
        model, 
        name="sentiment-model",
        registered_model_name="InfluencerInsightsSentiment"
    )
    
    print(f"Accuracy: {acc:.3f}")
    print("Model registered in MLflow!")