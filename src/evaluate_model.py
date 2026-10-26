
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from preprocessing import preprocess_text


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sentiment_dataset.csv"


# 1. Load and validate the dataset
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=["text", "sentiment"]).copy()

df["text"] = df["text"].astype(str)
df["sentiment"] = df["sentiment"].astype(str).str.strip().str.lower()

# Keep only valid sentiment labels
valid_labels = ["negative", "neutral", "positive"]
df = df[df["sentiment"].isin(valid_labels)]

# 2. Separate input text and target labels
X = df["text"]
y = df["sentiment"]

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y,
)

print(f"Total examples: {len(df)}")
print(f"Training examples: {len(X_train)}")
print(f"Testing examples: {len(X_test)}")

# 4. Create a fresh model for evaluation
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            preprocessor=preprocess_text,
            ngram_range=(1, 2),
        ),
    ),
    (
        "classifier",
        LogisticRegression(max_iter=1000),
    ),
])

# 5. Train only on the training data
model.fit(X_train, y_train)

# 6. Predict unseen test examples
y_pred = model.predict(X_test)

# 7. Evaluate the predictions
print("\nAccuracy:")
print(f"{accuracy_score(y_test, y_pred) * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=valid_labels,
        zero_division=0,
    )
)

print("Confusion Matrix:")
print("Label order:", valid_labels)
print(confusion_matrix(y_test, y_pred, labels=valid_labels))

print("\nIndividual test predictions:")
for text, actual, predicted in zip(X_test, y_test, y_pred):
    print(f"\nComment: {text}")
    print(f"Actual: {actual} | Predicted: {predicted}")
