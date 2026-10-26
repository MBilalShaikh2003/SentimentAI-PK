
import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from preprocessing import preprocess_text


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sentiment_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "sentiment_model.joblib"


# 1. Load the dataset
df = pd.read_csv(DATA_PATH)

# 2. Basic validation
df = df.dropna(subset=["text", "sentiment"])
df["text"] = df["text"].astype(str)
df["sentiment"] = df["sentiment"].str.strip().str.lower()

# 3. Create a machine-learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            preprocessor=preprocess_text,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(max_iter=1000)
    )
])

# 4. Train on the available sample dataset
model.fit(df["text"], df["sentiment"])

# 5. Save the trained model
joblib.dump(model, MODEL_PATH)

print("Model trained successfully!")
print(f"Training examples: {len(df)}")
print(f"Labels: {sorted(df['sentiment'].unique())}")
print(f"Model saved at: {MODEL_PATH}")
print("\nNote: This tiny dataset is for learning only.")
