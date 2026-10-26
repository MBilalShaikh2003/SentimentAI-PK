
import pandas as pd

from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

from preprocessing import preprocess_text


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sentiment_dataset.csv"


# 1. Load the dataset
df = pd.read_csv(DATA_PATH)

# 2. Clean and validate the data
df = df.dropna(subset=["text", "sentiment"]).copy()

df["text"] = df["text"].astype(str).str.strip()
df["sentiment"] = df["sentiment"].astype(str).str.strip().str.lower()

valid_labels = ["negative", "neutral", "positive"]
df = df[df["sentiment"].isin(valid_labels)]

# Remove exact duplicate texts
df = df.drop_duplicates(subset=["text"], keep="first")

X = df["text"]
y = df["sentiment"]


# 3. Create the model pipeline
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


# 4. Set up 5-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)


# 5. Evaluate the model using multiple metrics
scoring = {
    "accuracy": "accuracy",
    "precision_macro": make_scorer(
        precision_score,
        average="macro",
        zero_division=0,
    ),
    "recall_macro": make_scorer(
        recall_score,
        average="macro",
        zero_division=0,
    ),
    "f1_macro": make_scorer(
        f1_score,
        average="macro",
        zero_division=0,
    ),
}

results = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring=scoring,
)


# 6. Display the results
print("5-Fold Cross-Validation Results")
print("-" * 40)
print("Total examples:", len(df))
print("Number of folds:", cv.n_splits)

for metric in scoring:
    scores = results[f"test_{metric}"]

    print(f"\n{metric.replace('_', ' ').title()}:")
    print("Fold scores:", [round(score * 100, 2) for score in scores])
    print(f"Mean: {scores.mean() * 100:.2f}%")
    print(f"Standard deviation: {scores.std() * 100:.2f}%")
