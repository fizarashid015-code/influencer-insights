import optuna
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
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

def objective(trial):
    C = trial.suggest_float('C', 0.01, 10.0, log=True)
    max_iter = trial.suggest_int('max_iter', 100, 500)
    
    model = LogisticRegression(C=C, max_iter=max_iter)
    score = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20)

print(f"\nBest trial:")
print(f"  Accuracy: {study.best_value:.3f}")
print(f"  Params: {study.best_params}")